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
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView)

urlpatterns = [
    path('api/token',TokenObtainPairView.as_view()),
    path('api/token/refresh',TokenRefreshView.as_view()),
    path('api/<str:user>/<int:panel>/<str:type>/student/',
         views.Student_List.as_view(), name='index'),
    path('api/<str:user>/student/', views.Student_List.as_view(), name='index')

#     path('api/<str:user>/<int:panel>/<str:type>/team/',
#          views.Team_List.as_view(), name='index'),
#     path('api/<str:user>/team/', views.Team_List.as_view(), name='index'),

#     path('api/panel/', views.Panel_List.as_view(), name='index'),
#     path('api/faculty/', views.Faculty_List.as_view(), name='index'),
#     path('api/marks/', views.marks.as_view(), name='index'),
#     path('api/department/', views.Dept_List.as_view(), name='index'),
]
