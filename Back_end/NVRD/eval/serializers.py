from rest_framework import serializers
from .models import *

class Student_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('srn','first_name','last_name','email')