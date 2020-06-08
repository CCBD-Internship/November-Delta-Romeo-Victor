from rest_framework import serializers
from .models import *
from django.db import models

class Student_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('srn','name','email','phone','dept','team_id')
    # def create(self,validated_data):
    #     stud = Student(
    #         srn=validated_data.data.get("srn"),
    #         first_name=validated_data.data.get("first_name"),
    #         last_name=validated_data.data.get('last_name'),
    #         email=validated_data.data.get('email'),
    #         phone=validated_data.data.get('phone'),
    #         dept = Department.objects.get(dept='computer science')
    #     )
    #     stud.save()
    #     return stud
class Team_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('srn','name','email','phone','dept','team_id')
