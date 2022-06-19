# author: Mr. Ma
# datetime :2022/6/19
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from ..models import Author
from rest_framework import serializers
# =======================================基于GenericViewSet+ListCreateAPIView...的接口实线================================

# 主要是在viewSet的基础上不用自己再去写实现代码
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin, RetrieveModelMixin, \
    DestroyModelMixin
from rest_framework.viewsets import GenericViewSet


class AuthorSerializers(serializers.ModelSerializer):
    class Meta:
        model = Author

        fields = '__all__'


class AuthorView(GenericViewSet, ListModelMixin, CreateModelMixin, RetrieveModelMixin, DestroyModelMixin,
                 UpdateModelMixin):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializers
