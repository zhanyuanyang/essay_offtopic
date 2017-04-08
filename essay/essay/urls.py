"""essay URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import url,include
from django.contrib import admin
from apps import main
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^main/', include('apps.main.urls', namespace='login')),
    # url(r'^score/',views.score),
    # url(r'detect/',views.detect),
    # url(r'^$', views.home, name='home'),
    # url(r'update_time/',views.update_time),
    # url(r'^write/',views.write_offtopic,name='write'),
    # url(r'^save/',views.saveEssay,name='saveessay'),
]
