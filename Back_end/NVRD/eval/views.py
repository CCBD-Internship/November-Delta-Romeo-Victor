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
            if 'srn' in request.GET:
                student_as_object = Student.objects.filter(
                    srn__startswith=request.GET.__getitem__('srn'))
            else:
                student_as_object = Student.objects.all()
            content = Student_Serializer(student_as_object, many=True)
            return Response(content.data)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        response_list=[]
        for i in request.data:
            student_data=
            team_data=
            serial = Student_Serializer(data=i)
            if serial.is_valid():
                serial.save()
            else:
                response_list.append({"value":i,"detail":serial.errors})
        if(response_list==[]):
            return Response({"detail":"insert successful"}, status=status.HTTP_201_CREATED)
        else:
            return Response(response_list,status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        serial = Student_Serializer(Student.objects.get(srn=request.data.get("srn")),data=request.data)
        try:
            if(serial.is_valid()):
                serial.save()
                return Response({"detail":"update successful"}, status=status.HTTP_202_ACCEPTED)
            else:
                return Response(serial.errors,status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(serial.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        serial = Student_Serializer(Student.objects.get(srn=request.data.get("srn")),data=request.data)
        try:
            if serial.is_valid():
                Student.objects.get(srn=serial.data.get("srn")).delete()
                return Response({"detail":"delete successful"}, status=status.HTTP_200_OK)
            else:
                return Response(serial.errors,status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(serial.errors,status=status.HTTP_400_BAD_REQUEST)

class panel(APIView):

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
        if(type(request.data)==list):
            response_list=[]
            for i in request.data:
                serial = Student_Serializer(data=i)
                if serial.is_valid():
                    serial.save()
                else:
                    response_list.append({"value":i,"detail":serial.errors})
            if(response_list==[]):
                return Response({"detail":"insert successful"}, status=status.HTTP_201_CREATED)
            else:
                return Response(response_list,status=status.HTTP_400_BAD_REQUEST)
        else:
            serial = Student_Serializer(data=request.data)
            if serial.is_valid():
                serial.save()
                return Response(serial.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serial.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        serial = Student_Serializer(Student.objects.get(srn=request.data.get("srn")),data=request.data)
        try:
            if(serial.is_valid()):
                serial.save()
                return Response({"detail":"update successful"}, status=status.HTTP_202_ACCEPTED)
            else:
                return Response(serial.errors,status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(serial.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        serial = Student_Serializer(Student.objects.get(srn=request.data.get("srn")),data=request.data)
        try:
            if serial.is_valid():
                Student.objects.get(srn=serial.data.get("srn")).delete()
                return Response({"detail":"delete successful"}, status=status.HTTP_200_OK)
            else:
                return Response(serial.errors,status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(serial.errors,status=status.HTTP_400_BAD_REQUEST)

class facpan(APIView):

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
        if(type(request.data)==list):
            response_list=[]
            for i in request.data:
                serial = Student_Serializer(data=i)
                if serial.is_valid():
                    serial.save()
                else:
                    response_list.append({"value":i,"detail":serial.errors})
            if(response_list==[]):
                return Response({"detail":"insert successful"}, status=status.HTTP_201_CREATED)
            else:
                return Response(response_list,status=status.HTTP_400_BAD_REQUEST)
        else:
            serial = Student_Serializer(data=request.data)
            if serial.is_valid():
                serial.save()
                return Response(serial.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serial.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        serial = Student_Serializer(Student.objects.get(srn=request.data.get("srn")),data=request.data)
        try:
            if(serial.is_valid()):
                serial.save()
                return Response({"detail":"update successful"}, status=status.HTTP_202_ACCEPTED)
            else:
                return Response(serial.errors,status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(serial.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        serial = Student_Serializer(Student.objects.get(srn=request.data.get("srn")),data=request.data)
        try:
            if serial.is_valid():
                Student.objects.get(srn=serial.data.get("srn")).delete()
                return Response({"detail":"delete successful"}, status=status.HTTP_200_OK)
            else:
                return Response(serial.errors,status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(serial.errors,status=status.HTTP_400_BAD_REQUEST)

class marks(APIView):

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
        if(type(request.data)==list):
            response_list=[]
            for i in request.data:
                serial = Student_Serializer(data=i)
                if serial.is_valid():
                    serial.save()
                else:
                    response_list.append({"value":i,"detail":serial.errors})
            if(response_list==[]):
                return Response({"detail":"insert successful"}, status=status.HTTP_201_CREATED)
            else:
                return Response(response_list,status=status.HTTP_400_BAD_REQUEST)
        else:
            serial = Student_Serializer(data=request.data)
            if serial.is_valid():
                serial.save()
                return Response(serial.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serial.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        serial = Student_Serializer(Student.objects.get(srn=request.data.get("srn")),data=request.data)
        try:
            if(serial.is_valid()):
                serial.save()
                return Response({"detail":"update successful"}, status=status.HTTP_202_ACCEPTED)
            else:
                return Response(serial.errors,status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(serial.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        serial = Student_Serializer(Student.objects.get(srn=request.data.get("srn")),data=request.data)
        try:
            if serial.is_valid():
                Student.objects.get(srn=serial.data.get("srn")).delete()
                return Response({"detail":"delete successful"}, status=status.HTTP_200_OK)
            else:
                return Response(serial.errors,status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(serial.errors,status=status.HTTP_400_BAD_REQUEST)
