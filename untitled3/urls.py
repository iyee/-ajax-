"""untitled3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from django.contrib import admin
from app01 import  views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', views.login),
    url(r'^index/$', views.index),
    url(r'^get_vaildCode_img/$', views.get_vaildCode_img),
    url(r'^log_out/$', views.log_out),
    url(r'^list-(?P<nid>.+)/$', views.list),
    url(r'^list_post-(?P<nid>.+)/$', views.list_post),
    url(r'^conntect/$', views.conntect),
    url(r'^conntect/list_post-(?P<nid>.+)/$', views.list_post),
    url(r'^release-(?P<nid>.+)/$', views.release),
    url(r'^rest/$', views.test),

]