# coding:utf-8
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.login, name='login_page'),
    url(r'^register_action/$', views.register_action, name='register_action'),
    url(r'^login/$', views.exit, name='exit'),
    url(r'^essayRelease/$', views.essayRelease, name='essayRelease'),
    url(r'^main/$', views.main, name='main'),
    url(r'^detail/$', views.view, name='view_detail'),
    url(r'^student_result/$', views.student_result, name='student_result'),
    url(r'^std_manage/$', views.std_manage, name='std_manage'),
    url(r'^student_essay/$', views.student_essay, name='student_essay'),
]
