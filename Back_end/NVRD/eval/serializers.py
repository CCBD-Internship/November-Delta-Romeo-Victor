from rest_framework import serializers
from .models import *
from django.db import models

class Department_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('dept')

class Faculty_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = ('fac_id','name','email','phone','dept','is_active')

class FacultyPanel_Serializer(serializers.ModelSerializer):
    class Meta:
        model=FacultyPanel
        fields=('fac','panel','is_coordinator')

class Panel_Serializer(serializers.ModelSerializer):
    class Meta:
        model=Panel
        fields=('label','is_active','panel_id','ctime')

class PanelReview_Serializer(serializers.ModelSerializer):
    class Meta:
        model=PanelReview
        fields=('review_number','panel','open_time','close_time')

class Review_Serializer(serializers.ModelSerializer):
    class Meta:
        model=Review1
        fields=('srn','fac','project_work','quality_of_demo','project_report','viva_voce','comments') 

class Student_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('srn','name','email','phone','dept','team')

class Team_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('team_name','description','guide','panel','team_id')

class TeamFacultyReview_Serializer(serializers.ModelSerializer):
    class Meta:
        model=TeamFacultyReview
        fields=('team','fac','review_number','remark') 
