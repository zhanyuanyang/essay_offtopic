# coding:utf-8
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.login, name='login_page'),
    url(r'^register_action/$', views.register_action, name='register_action'),
    url(r'^login/$', views.exit, name='exit'),
    url(r'^essayRelease/$', views.essayRelease, name='essayRelease'),
    url(r'^main/$', views.main, name='main'),
]