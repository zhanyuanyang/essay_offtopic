# coding:utf-8
from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^$', views.login, name='login_page'),
    url(r'^register_action/$', views.register_action, name='register_action'),
    url(r'^main/$', views.main, name='main'),
    url(r'^setting_avatar/$', views.setting_avatar, name='setting_avatar'),
    url(r'^score/', views.score, name='score'),
    url(r'^detect/', views.detect, name='detect'),
    # url(r'^$', views.home, name='home'),
    # url(r'update_time/',views.update_time),
    url(r'^write/', views.write_offtopic, name='write'),
    url(r'^save1/', views.saveUnsuperviesd, name='save_unsupervised'),
    url(r'^history_result/', views.history_result, name='history_result'),
    url(r'^save2/', views.saveEssay, name='save_supervised'),
    url(r'^history/', views.show_history, name='history'),
    url(r'^write_historyEssay/', views.write_historyEssay, name='write_historyEssay'),
    # 参数化url显示结果
    url(r'^calendar_result/', views.calendar_result, name='calendar_result'),
    url(r'^intermediateResults/', views.intermediateResults, name='intermediateResults'),
    url(r'^detect2/', views.detect2, name='detect2'),
    # url(r'^calendar_cat/', views.display, name='calendar_display'),
    url(r'^login/$', views.exit, name='logout')

]
