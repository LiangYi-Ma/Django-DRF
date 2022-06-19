"""DRF URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from sers import views
from sers.view import APIView, GenericAPIView, ListCreateAPIView, Mixin, ViewSet, GenericViewSetListCreateAPIView, \
    ModelViewSet

# rest_framework路由组件
"""
    from rest_framework import routers
    
    router = routers.DefaultRouter()
    router.register('publish', views.PublishView)
    相当于生成了这两条路由：
        path('sers/publish/',....),
        re_path('sers/publish/(?P<pk>\d+)', ...)
    urlpatterns = []
    urlpatterns+=router.urls
"""

urlpatterns = [
    path('admin/', admin.site.urls),

    path('sers/book/', APIView.BookView.as_view()),
    re_path('sers/book/(\d+)', APIView.BookDetailView.as_view()),  # (\d+)主键标识,正则表达式

    path('sers/publish/', GenericAPIView.PublishView.as_view()),
    re_path('sers/publish/(?P<pk>\d+)', GenericAPIView.PublishDetailView.as_view()),

    path('sers/author_Mixin/', Mixin.AuthorView.as_view()),
    re_path('sers/author_Mixin/(?P<pk>\d+)', Mixin.AuthorDetailView.as_view()),

    path('sers/author_ListCreateAPIView/', ListCreateAPIView.AuthorView.as_view()),
    re_path('sers/author_ListCreateAPIView/(?P<pk>\d+)', ListCreateAPIView.AuthorDetailView.as_view()),

    # viewset方法需要在url中指定请求类型对应的方法
    path('sers/author/', ViewSet.AuthorView.as_view({'get': "get_all", "post": "add_object"})),
    re_path('sers/author/(?P<pk>\d+)',
            ViewSet.AuthorView.as_view({'get': "get_object", "put": "update_object", "delete": "delete_object"})),

    # GenericViewSetListCreateAPIView组合方法需要在url中指定请求类型对应的方法(但是指定的方法是继承工具类中自带的,不用自己再次重新写)
    path('sers/authorgl/', GenericViewSetListCreateAPIView.AuthorView.as_view({"get": "list", "post": "create"})),
    re_path('sers/authorgl/(?P<pk>\d+)',
            GenericViewSetListCreateAPIView.AuthorView.as_view(
                {'get': "retrieve", "put": "update", "delete": "destroy"})),

    # viewset方法需要在url中指定请求类型对应的方法(但是指定的方法是继承工具类中自带的，自动继承)
    path('sers/authormvs/', ModelViewSet.AuthorView.as_view({"get": "list", "post": "create"})),
    re_path('sers/authormvs/(?P<pk>\d+)',
            ModelViewSet.AuthorView.as_view({'get': "retrieve", "put": "update", "delete": "destroy"}))
]
