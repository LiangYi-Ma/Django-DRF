from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.mixins import CreateModelMixin
from rest_framework.views import APIView
from .models import Book, Publish, Author
from rest_framework import serializers
# 用于将数据（有序字典的格式）转化成json数据,需要在setting注册rest_framework
from rest_framework.response import Response


# =============================================本文件将view文件夹下类容进行了汇总===========================================

# ===================================================基于APIView的接口实现================================================

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


# 自动根据模型生成序列化器，并且重新重写好了update和create
class BookSerializers(serializers.ModelSerializer):
    data = serializers.DateField(source="pub_date")

    class Meta:
        model = Book

        # fields = '__all__'
        # fields = ['title', 'price', 'data']
        exclude = ['pub_date']


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


# ===================================================基于GenericAPIView的接口实现=======================================
from rest_framework.generics import GenericAPIView, ListCreateAPIView


#
#
# GenericAPIView继承的APIView

class PublishSerializers(serializers.ModelSerializer):
    class Meta:
        model = Publish

        fields = '__all__'


class PublishView(GenericAPIView):
    queryset = Publish.objects.all()
    serializer_class = PublishSerializers

    def get(self, request):
        # self.get_queryset()，获取所有的书,由GenericAPIView提供
        # self.get_serializer_class()获取序列化器，因为序列化器是个方法，所有需要带括号
        """
        这两种的作用一模一样：
            serializer = self.get_serializer_class()(instance=self.get_queryset(), many=True)
            serializer = self.get_serializer(instance=self.get_queryset(), many=True)
        """
        # serializer = self.get_serializer_class()(instance=self.get_queryset(), many=True)
        serializer = self.get_serializer(instance=self.get_queryset(), many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        # 序列化
        serializer = self.get_serializer(data=data)
        # 校验数据
        ser = serializer.is_valid()
        if ser:
            new_book = serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class PublishDetailView(GenericAPIView):
    queryset = Publish.objects.all()
    serializer_class = PublishSerializers

    def get(self, request, pk):
        # pk相当于变量的名称（有名传参），会自动识别self.get_object()
        serializer = self.get_serializer(instance=self.get_object(), many=False)
        return Response(serializer.data)

    def put(self, request, pk):
        data = request.data
        serializer = self.get_serializer(instance=self.get_object(), data=data)
        bool = serializer.is_valid()
        if bool:
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        self.get_object().delete()
        return Response()


# ===================================================基于Mixin的接口实现=======================================
# from rest_framework.generics import GenericAPIView
# from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin, RetrieveModelMixin, \
#     DestroyModelMixin
#
#
# # RetrieveModelMixin：用于单条查询
# # DestroyModelMixin：用于删除操作
#
#
# class AuthorSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = Author
#
#         fields = '__all__'
#
#
# class AuthorView(ListModelMixin, CreateModelMixin, GenericAPIView):
#     queryset = Author.objects.all()
#     serializer_class = AuthorSerializers
#
#     def get(self, request):
#         return self.list(request)
#
#     def post(self, request):
#         return self.create(request)
#
#
# class AuthorDetailView(RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin, GenericAPIView):
#     queryset = Author.objects.all()
#     serializer_class = AuthorSerializers
#
#     def get(self, request, pk):
#         return self.retrieve(request, pk)
#
#     def put(self, request, pk):
#         return self.update(request, pk)
#
#     def delete(self, request, pk):
#         return self.destroy(request, pk)

# =======================================基于ListCreateAPIView....的接口实现（将crud封装）==================================
# from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
#
#
# # ListCreateAPIView：将查找所有和新增数据封装
# # RetrieveUpdateDestroyAPIView：用于单条查询，删除操作，更新操作封装
# # 根据实际的需求可以随意组合
#
#
# class AuthorSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = Author
#
#         fields = '__all__'
#
#
# class AuthorView(ListCreateAPIView):
#     queryset = Author.objects.all()
#     serializer_class = AuthorSerializers
#
#
# class AuthorDetailView(RetrieveUpdateDestroyAPIView):
#     queryset = Author.objects.all()
#     serializer_class = AuthorSerializers


# =======================================基于ViewSet的接口实现（将crud封装）==================================
# from rest_framework.viewsets import ViewSet
#
#
# # ViewSet：重写了分发机制
#
# class AuthorSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = Author
#
#         fields = '__all__'
#
#
# class AuthorView(ViewSet):
#     def get_all(self,request):
#         return Response("查看所有")
#
#     def add_object(self,request):
#         return Response("添加资源")
#
#     def get_object(self, request, pk):
#         return Response("查看一个资源")
#
#     def update_object(self, request, pk):
#         return Response("更新资源")
#
#     def delete_object(self, request, pk):
#         return Response("删除单一资源")


# =======================================基于GenericViewSet+ListCreateAPIView...的接口实线================================

# 主要是在viewSet的基础上不用自己再去写实现代码
# from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin, RetrieveModelMixin, \
#     DestroyModelMixin
# from rest_framework.viewsets import GenericViewSet
#
#
# class AuthorSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = Author
#
#         fields = '__all__'
#
#
# class AuthorView(GenericViewSet, ListModelMixin, CreateModelMixin, RetrieveModelMixin, DestroyModelMixin,
#                  UpdateModelMixin):
#     queryset = Author.objects.all()
#     serializer_class = AuthorSerializers


# =======================================基于ModelViewSet的接口实线================================

# 主要是在viewSet的基础上不用自己再去写实现代码,ModelViewSet直接相当于自动把Mixin全部继承了
from rest_framework.viewsets import ModelViewSet


class AuthorSerializers(serializers.ModelSerializer):
    class Meta:
        model = Author

        fields = '__all__'


class AuthorView(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializers
