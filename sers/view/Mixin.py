# author: Mr. Ma
# datetime :2022/6/19
# ===================================================基于Mixin...的接口实现=======================================
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin, RetrieveModelMixin, \
    DestroyModelMixin
from ..models import Author
from rest_framework import serializers
from rest_framework.generics import GenericAPIView


# RetrieveModelMixin：用于单条查询
# DestroyModelMixin：用于删除操作
# Mixin主要的特点是基于GenericAPIView将crud进行了封装，让用户继承工具类后，可以直接调用api来实现功能

class AuthorSerializers(serializers.ModelSerializer):
    class Meta:
        model = Author

        fields = '__all__'


class AuthorView(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializers

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)


class AuthorDetailView(RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin, GenericAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializers

    def get(self, request, pk):
        return self.retrieve(request, pk)

    def put(self, request, pk):
        return self.update(request, pk)

    def delete(self, request, pk):
        return self.destroy(request, pk)
