"""DjangoBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from app01 import views, main_func

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/', views.index),
    url(r'^login/', views.login),
    url(r'^check_code/', views.check_code),
    url(r'^register/', views.register),
    url(r'^blog_mainpage/(?P<aid>\d+)', main_func.blog_mainpage),
    url(r'^my_blog/(?P<subtitle>\w+)', main_func.my_blog),
    url(r'^add_tags_category/(?P<subtitle>\w+)', main_func.add_tags_category),
    url(r'^edit_tag/', main_func.edit_tag),
    url(r'^edit_category/', main_func.edit_category),
    url(r'^delete_tag/', main_func.delete_tag),
    url(r'^delete_category/', main_func.delete_category),
    url(r'^add_article/(?P<subtitle>\w+)', main_func.add_article),
    url(r'^article_page/(?P<aid>\d+)', main_func.article_page),
    url(r'^edite_article/(?P<aid>\d+)', main_func.edite_article),
    url(r'^delete_article/(?P<aid>\d+)', main_func.delete_article),
    url(r'^(?P<subtitle>\w+)/(?P<key>((tag)|(date)|(category)))/(?P<val>\w+-*\w*)/', main_func.filter),
    url(r'^search-(?P<article_type_id>\d+)-(?P<category_id>\d+)-(?P<articles2tag__tag_id>\d+)', main_func.search),
    url(r'^reset_profile/(?P<subtitle>\w+)', main_func.reset_profile),
    url(r'^like/(?P<subtitle>\w+)', main_func.like),
    url(r'^show_comment/', main_func.show_comment),
    url(r'^add_comment/', main_func.add_comment),
    url(r'^logout/', main_func.logout),
    url(r'^', main_func.blog_mainpage),

]
