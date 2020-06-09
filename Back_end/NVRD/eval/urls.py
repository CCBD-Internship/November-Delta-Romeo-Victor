"""NVRD URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from . import views
from django.conf.urls import url
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('student/', views.Student_List.as_view(),name='index'),    
    path('panel/', views.Panel_List.as_view(),name='index'),
    path('faculty/', views.Faculty_List.as_view(),name='index'),          
    path('marks/', views.marks.as_view(),name='index'),
    path('department/',views.Dept_List.as_view(),name='index'),
    path('team/',views.Team_List.as_view(),name='index')
]