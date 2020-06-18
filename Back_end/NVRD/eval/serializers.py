from rest_framework import serializers
from .models import *
from django.db import models

class Department_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ("dept",)

class Faculty_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        # fields = ('fac_id','name','email','phone','dept','is_active')
        fields = '__all__'

class Panel_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Panel
        # fields = ('label','is_active','panel_id','ctime')
        fields = '__all__'

class FacultyPanel_Serializer(serializers.ModelSerializer):
    class Meta:
        model = FacultyPanel
        fields = '__all__'

class PanelReview_Serializer(serializers.ModelSerializer):
    class Meta:
        model = PanelReview
        fields = ('review number','panel','o_time','c_time')

class Review1_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Review1
        fields = ('fac','project_work','quality_of_demo','project_report','viva_voce','comments')

class Review2_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Review2
        fields = ('fac','project_work','quality_of_demo','project_report','viva_voce','comments')

class Review3_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Review3
        fields = ('fac','project_work','quality_of_demo','project_report','viva_voce','comments')

class Review4_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Review4
        fields = ('fac','project_work','quality_of_demo','project_report','viva_voce','comments')

class Review5_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Review5
        fields = ('fac','project_work','quality_of_demo','project_report','viva_voce','comments')

class Student_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        # fields = ('srn','name','email','phone','dept')
        fields = '__all__'

class Team_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'
        
class TeamFacultyReview_Serializer(serializers.ModelSerializer):
    class Meta:
        model = TeamFacultyReview
        fields = ('team','fac','review','remark')

