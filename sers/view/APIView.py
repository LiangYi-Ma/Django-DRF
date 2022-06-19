# author: Mr. Ma
# datetime :2022/6/19
from rest_framework.views import APIView
from ..models import Book, Publish, Author
from rest_framework import serializers
# 用于将数据（有序字典的格式）转化成json数据,需要在setting注册rest_framework
from rest_framework.response import Response


# ===================================================基于APIView的接口实现================================================

# ======================================(1)使用serializers.Serializer编写序列化器==========================================
# class BookSerializers(serializers.Serializer):
#     title = serializers.CharField(max_length=32)
#     price = serializers.IntegerField()
#     # pub_date = serializers.DateField()
#     # 如果想该这个变量的名字不对应相应的字段名，则在后边加source="pub_date"指明对应的字段名
#     data = serializers.DateField(source="pub_date")
#
#     # 如果要使用序列化器的Sava方法就需要在这里重写create方法
#     def create(self, validated_data):
#         # 添加数据逻辑
#         new_book = Book.objects.create(**self.validated_data)
#         return new_book
#
#     def update(self, instance, validated_data):
#         book_new = Book.objects.filter(pk=instance.pk).update(**validated_data)
#         updated_book = Book.objects.get(pk=instance.pk)
#         # 这里相当于将序列化后的数据给替换成新更新后的数据，序列化后的数据存在instance中,但如果重写了update方法就不需要了
#         # serializer.instance = updated_book
#         # 直接返回数据
#         return updated_book

# ======================================(2)使用serializers.ModelSerializer编写序列化器====================================
# 自动根据模型生成序列化器，并且自动重新重写好了update和create
class BookSerializers(serializers.ModelSerializer):
    data = serializers.DateField(source="pub_date")

    class Meta:
        model = Book

        # fields = '__all__'
        # fields = ['title', 'price', 'data']
        exclude = ['pub_date']


# ====================================================具体业务===========================================================

class BookView(APIView):
    def get(self, request):
        book_list = Book.objects.all()
        """
            BookSerializers(instance=, data=)
            instance：序列化器，data：反序列化器
            many=True：表示序列化多个对象
        """
        serializer = BookSerializers(instance=book_list, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
            此时的request是经过rest_framework重写过的request
            此时可以直接通过request.data获取请求体中的数据
            通过request.query_params获取get请求是放在url中的数据
        """
        try:
            data = request.data
            """
                构建反序列化对象:
                    数据校验：serializer.is_valid()
                    存校验通过数据：serializer.validated_data
                    存未校验通过的数据：serializer.errors
            """
            serializer = BookSerializers(data=data)
            # 校验数据
            ser = serializer.is_valid()
            if ser:
                # new_book = Book.objects.create(**serializer.validated_data)
                # 此处的save相当于调用序列化器中重写的create方法
                new_book = serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        except Exception as e:
            print(e)
        return Response()


class BookDetailView(APIView):
    def get(self, request, id):
        book = Book.objects.get(pk=id)
        seris = BookSerializers(instance=book)
        return Response(seris.data)

    def put(self, request, id):
        data = request.data
        update_book = Book.objects.get(pk=id)
        serializer = BookSerializers(instance=update_book, data=data)
        bool = serializer.is_valid()
        if bool:
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request, id):
        Book.objects.filter(pk=id).delete()
        return Response()
