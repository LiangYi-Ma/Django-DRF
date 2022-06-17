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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sers/book/', views.BookView.as_view()),
    re_path('sers/book/(\d+)', views.BookDetailView.as_view()),  # (\d+)主键标识,正则表达式
    path('sers/publish/', views.PublishView.as_view()),
    re_path('sers/publish/(?P<pk>\d+)', views.PublishDetailView.as_view()),
    # path('sers/author/', views.AuthorView.as_view()),
    # re_path('sers/author/(?P<pk>\d+)', views.AuthorDetailView.as_view())
    # viewset方法需要在url中指定请求类型对应的方法
    path('sers/author/', views.AuthorView.as_view({'get': "get_all", "post": "add_object"})),
    re_path('sers/author/(?P<pk>\d+)',
            views.AuthorView.as_view({'get': "get_object", "put": "update_object", "delete": "delete_object"}))
]
