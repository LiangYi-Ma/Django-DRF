# author: Mr. Ma
# datetime :2022/6/19
from rest_framework.views import APIView
from ..models import Book, Publish, Author
from rest_framework import serializers
# 用于将数据（有序字典的格式）转化成json数据,需要在setting注册rest_framework
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView


# ===================================================基于GenericAPIView的接口实现=======================================


# ======================================使用serializers.ModelSerializer编写序列化器====================================
# GenericAPIView继承的APIView

class PublishSerializers(serializers.ModelSerializer):
    class Meta:
        model = Publish

        fields = '__all__'


# ====================================================具体业务===========================================================

class PublishView(GenericAPIView):
    # 将查询所有的数据和序列化器名称提出成变量，下次只需要改一下这两个变量就好
    queryset = Publish.objects.all()
    serializer_class = PublishSerializers

    def get(self, request):
        # self.get_queryset()，获取所有的书,由GenericAPIView提供
        # self.get_serializer_class()获取序列化器，因为序列化器是个方法，所有需要带括号
        """
        这两种的作用一模一样：
            serializer = self.get_serializer_class()(instance=self.get_queryset(), many=True)
            serializer = self.get_serializer(instance=self.get_queryset(), many=True)
            self.get_serializer  相当于 self.get_serializer_class()
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
