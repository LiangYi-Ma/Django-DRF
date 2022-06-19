# author: Mr. Ma
# datetime :2022/6/19
from ..models import Author
from rest_framework import serializers

# =======================================基于ViewSet的接口实现（将crud封装）==================================
# 主要是在viewSet的基础上不用自己再去写实现代码,ModelViewSet直接相当于自动把Mixin全部继承了
from rest_framework.viewsets import ModelViewSet


class AuthorSerializers(serializers.ModelSerializer):
    class Meta:
        model = Author

        fields = '__all__'


class AuthorView(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializers
