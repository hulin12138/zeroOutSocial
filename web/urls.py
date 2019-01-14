"""zeroOutSocial URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path
import sys
sys.path.append('./web')
import views
import control

app_name = 'zeroOut'
urlpatterns = [
    path('', views.index, name='index'),
    path('login', control.login, name='login'),
    path('check_register', control.check_register, name='check_register'),
    path('register', views.register, name='register'),
    path('login.html', views.index, name='index'),
    path('register.html', views.register, name='register'),
    path('get_home', control.get_home, name='get_home'),
    path('usermain.html', control.get_home, name='get_home'),
    path('get_my_follow_user',views.get_my_follow_user, name='get_my_follow_user')
    path('delete_follow_user',views.get_my_follow_user, name='delete_follow_user')
    path('get_my_fan',views.get_my_fan, name='get_my_fan')
    path('delete_fan',views.delete_fan, name='delete_fan')
    path('send_weibo', views.send_weibo, name="send_weibo"),
    path('delete_weibo', views.delete_weibo, name="delete_weibo")
    path('get_my_weibo', views.get_my_weibo, name="get_my_weibo"),
    path('get_my_follow_weibo', views.get_my_follow_weibo, name="get_my_follow_weibo"),

]
