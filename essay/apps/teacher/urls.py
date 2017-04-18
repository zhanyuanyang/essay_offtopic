# coding:utf-8
from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'^test/$', views.test, name='test'),
    url(r'^login/$', views.exit, name='exit'),
    url(r'^essayRelease/$', views.essayRelease, name='essayRelease'),
    url(r'^main/$', views.main, name='main'),
]