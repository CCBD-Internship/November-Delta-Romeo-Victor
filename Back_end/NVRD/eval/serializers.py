from rest_framework import serializers
from .models import *
from django.db import models

class Student_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('srn','first_name','last_name','email','phone','dept')
    def create(self,validated_data):
        user = Student.objects.create(
            srn=validated_data.data.get("srn"),
            first_name=validated_data.data.get("first_name"),
            last_name=validated_data.data.get('last_name'),
            email=validated_data.data.get('email'),
            phone=validated_data.data.get('phone'),
            dept = Department.objects.get(dept='computer science')
        )
        return user