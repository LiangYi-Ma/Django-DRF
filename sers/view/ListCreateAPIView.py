# author: Mr. Ma
# datetime :2022/6/19

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from ..models import Author
from rest_framework import serializers


# =======================================基于ListCreateAPIView....的接口实现（将crud封装）==================================

# 特点是将crud进行了更进一步的封装，继承工具类后，不需要调用api会自动处理crud的各项功能，继承的工具类crud统一的封装了，需要了可以自由组合

# ListCreateAPIView：将查找所有和新增数据封装
# RetrieveUpdateDestroyAPIView：用于单条查询，删除操作，更新操作封装
# 根据实际的需求可以随意组合


class AuthorSerializers(serializers.ModelSerializer):
    class Meta:
        model = Author

        fields = '__all__'


class AuthorView(ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializers


class AuthorDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializers
