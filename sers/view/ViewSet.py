# author: Mr. Ma
# datetime :2022/6/19
from rest_framework.views import APIView
from ..models import Author
from rest_framework import serializers
# 用于将数据（有序字典的格式）转化成json数据,需要在setting注册rest_framework
from rest_framework.response import Response

# =======================================基于ViewSet的接口实现（将crud封装）==================================
from rest_framework.viewsets import ViewSet


# ViewSet：重写了分发机制，用户在url中自定义各类型对应的处理函数

class AuthorSerializers(serializers.ModelSerializer):
    class Meta:
        model = Author

        fields = '__all__'


class AuthorView(ViewSet):
    def get_all(self, request):
        return Response("查看所有")

    def add_object(self, request):
        return Response("添加资源")

    def get_object(self, request, pk):
        return Response("查看一个资源")

    def update_object(self, request, pk):
        return Response("更新资源")

    def delete_object(self, request, pk):
        return Response("删除单一资源")
