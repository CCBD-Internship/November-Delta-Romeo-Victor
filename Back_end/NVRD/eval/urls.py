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
    path('api/token/', views.LoginView.as_view()),
    path('api/<str:user>/changepassword/', views.ChangePassword.as_view()),
    path('api/token/refresh/', views.RefreshView.as_view()),
    path('api/<str:user>/<str:panel_year_code>-<str:panel_id>/student/',
         views.Student_List.as_view(), name='index'),
    path('api/<str:user>/<str:panel_year_code>-<str:panel_id>/<int:review_number>/student/',
         views.Student_List.as_view(), name='index'),
    path('api/<str:user>/student/', views.Student_List.as_view(), name='index'),
    path('api/<str:user>/<str:panel_year_code>-<str:panel_id>/team/',
         views.Team_List.as_view(), name='index'),
    path('api/<str:user>/<str:panel_year_code>-<str:panel_id>/<int:review_number>/team/',
         views.Team_List.as_view(), name='index'),
    path('api/<str:user>/team/', views.Team_List.as_view(), name='index'),
    path('api/<str:user>/<str:panel_year_code>-<str:panel_id>/faculty-panel/',
         views.FacultyPanel_List.as_view()),
    path('api/<str:user>/faculty-panel/', views.FacultyPanel_List.as_view()),
    path('api/<str:user>/<str:panel_year_code>-<str:panel_id>/panel-review/',
         views.PanelReview_List.as_view(), name='index'),
    path('api/<str:user>/faculty/', views.Faculty_List.as_view(), name='index'),
    path('api/<str:user>/<str:panel_year_code>-<str:panel_id>/panel/',
         views.Panel_List.as_view(), name='index'),
    path('api/<str:user>/panel/', views.Panel_List.as_view(), name='index'),
    path('api/<str:user>/marks-view/', views.GeneralMarksView.as_view()),
    path('api/<str:user>/<str:panel_year_code>-<str:panel_id>/<int:review_number>/<str:team_year_code>-<str:team_id>/marks-view/',
         views.EvaluatorMarksView.as_view()),
    path('api/<str:user>/faculty/', views.Faculty_List.as_view()),
    path('api/<str:user>/team-bulk/', views.Team_Student_CSV.as_view()),
    path('api/<str:user>/department/', views.Dept_List.as_view(), name='index'),
    path('api/<str:user>/aboutme/', views.AboutMe_List.as_view()),
    path('api/<str:user>/<str:panel_year_code>-<str:panel_id>/team-faculty-review/',
         views.TeamFacultyReview_List.as_view()),
    path('<str:user>/home/', views.home),
    path('api/<str:user>/generate-faculty-panel/',
         views.GenerateFacultyPanel.as_view()),
    path('', views.loginpage),
    path('logout/', views.logoutUser, name="logout"),
    #     path('api/<str:user>/<int:panel>/<str:type>/team/',
    #          views.Team_List.as_view(), name='index'),
    #     path('api/<str:user>/team/', views.Team_List.as_view(), name='index'),

    #     path('api/panel/', views.Panel_List.as_view(), name='index'),
    #     path('api/faculty/', views.Faculty_List.as_view(), name='index'),
    #     path('api/marks/', views.marks.as_view(), name='index'),
    # path('api/Blacklist/', views.TokenBlackList.as_view())

]

# frontend HTML
urlpatterns += [
    path('<str:user>/home/', views.indexpage),
    path('<str:user>/home/admin/student/HTML/', views.admin_studentHTML),
]

# frontend JS
urlpatterns += [
    path('<str:user>/home/admin/student/JS/', views.admin_studentJS),
    path('<str:user>/home/main.js/', views.indexJS),
]
