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


class Profile_Photo_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Profile_Photo
        # fields = ('label','is_active','panel_id','ctime')
        fields = '__all__'


class FacultyPanel_Serializer(serializers.ModelSerializer):
    class Meta:
        model = FacultyPanel
        fields = '__all__'


class PanelReview_Serializer(serializers.ModelSerializer):
    class Meta:
        model = PanelReview
        fields = '__all__'


class Review1_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Review1
        fields = '__all__'


class Review2_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Review2
        fields = '__all__'


class Review3_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Review3
        fields = '__all__'


class Review4_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Review4
        fields = '__all__'


class Review5_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Review5
        fields = '__all__'


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
        fields = '__all__'
