from django.shortcuts import render
from django.http import HttpResponse, Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
# from django.core import serializers
from .models import *
from .serializers import *
import json
#from talk.forms import PostForm
# Create your views here.


class Student_List(APIView):

    parser_classes = [JSONParser]

    def get(self, request):
        try:
            student_as_object = Student.objects.filter(
                first_name=request.GET.__getitem__('name'))
            content = Student_Serializer(student_as_object, many=True)
            return Response(content.data)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        serial = Student_Serializer(data=request.data)
        if serial.is_valid():
            Student_Serializer().create(serial)
            return Response(serial.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
