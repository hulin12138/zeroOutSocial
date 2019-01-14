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

]
