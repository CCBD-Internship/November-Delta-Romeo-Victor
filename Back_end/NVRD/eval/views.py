from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework_jwt.utils import jwt_decode_handler
from django.contrib.auth.models import User
from rest_framework import authentication, exceptions
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView)
from django.utils import timezone
# from django.core import serializers
from .models import *
from .serializers import *
import json
# Create your views here.

# from django_cron import CronJobBase, Schedule

# class MyCronJob(CronJobBase):
#     RUN_EVERY_MINS = 120 # every 2 hours

#     schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
#     code = 'my_app.my_cron_job'    # a unique code

#     def do(self):
#         pass    # do your thing here

def add_one_panel(panel_year_code):
    largest = Panel.objects.filter(
        panel_year_code=panel_year_code).order_by('panel_id').last()
    if not largest:
        return str(1).zfill(10)
    return str(int(largest.panel_id) + 1).zfill(10)


def add_one_team(team_year_code):
    largest = Team.objects.filter(
        team_year_code=team_year_code).order_by('team_id').last()
    if not largest:
        return str(1).zfill(10)
    return str(int(largest.team_id) + 1).zfill(10)


class Dept_List(APIView):

    parser_classes = [JSONParser]

    def get(self, request, year):
        try:
            dept_as_object = Department.objects.all()
            content = Department_Serializer(dept_as_object, many=True)
            return Response(content.data)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        response_list = []
        for i in request.data:
            serial = Department_Serializer(data=i)
            if not serial.is_valid():
                response_list.append({"value": i, "detail": serial.errors})
        if(response_list == []):
            for i in request.data:
                if serial.is_valid():
                    serial.save()
            return Response({"detail": "insert successful"}, status=status.HTTP_201_CREATED)
        else:
            return Response(response_list, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        serial = Department_Serializer(Department.objects.get(
            dept=request.data.get("dept")), data=request.data)
        try:
            if(serial.is_valid()):
                serial.save()
                return Response({"detail": "update successful"}, status=status.HTTP_202_ACCEPTED)
            else:
                return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        serial = Department_Serializer(Department.objects.get(
            dept=request.data.get("dept")), data=request.data)
        try:
            if serial.is_valid():
                Department.objects.get(dept=serial.data.get("dept")).delete()
                return Response({"detail": "delete successful"}, status=status.HTTP_200_OK)
            else:
                return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)


class Faculty_List(APIView):

    parser_classes = [JSONParser]

    def get(self, request):
        try:
            Faculty_as_object = Faculty.objects.filter(
                fac_id=request.GET.__getitem__('fac_id'))
            content = Faculty_Serializer(Faculty_as_object, many=True)
            return Response(content.data)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        response_list = []
        for i in request.data:
            serial = Faculty_Serializer(data=i)
            if not serial.is_valid():
                response_list.append({"value": i, "detail": serial.errors})
        if(response_list == []):
            for i in request.data:
                serial = Faculty_Serializer(data=i)
                if serial.is_valid():
                    serial.save()
            return Response({"detail": "insert successful"}, status=status.HTTP_201_CREATED)
        else:
            return Response(response_list, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        serial = Faculty_Serializer(Faculty.objects.get(
            fac_id=request.data.get("fac_id")), data=request.data)
        try:
            if(serial.is_valid()):
                serial.save()
                return Response({"detail": "update successful"}, status=status.HTTP_202_ACCEPTED)
            else:
                return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        serial = Faculty_Serializer(Faculty.objects.get(
            fac_id=request.data.get("fac_id")), data=request.data)
        try:
            if serial.is_valid():
                Faculty.objects.get(fac_id=serial.data.get("fac_id")).delete()
                return Response({"detail": "delete successful"}, status=status.HTTP_200_OK)
            else:
                return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)


class FacultyPanel_List(APIView):

    parser_classes = [JSONParser]

    def get(self, request, user, panel_year_code=None, panel_id=None):
        try:
            if(user == User.objects.get(id=jwt_decode_handler(request.META["HTTP_AUTHORIZATION"].split()[1])["user_id"]).get_username()):
                if(panel_id == None and panel_year_code == None and Faculty.objects.get(fac_id=user).is_admin == True):
                    facultypanel_as_object = FacultyPanel.objects.all()
                    if 'fac_id' in request.GET:
                        facultypanel_as_object = facultypanel_as_object.filter(
                            fac_id__startswith=request.GET['fac_id'])
                    if 'panel_year_code' in request.GET:
                        facultypanel_as_object = facultypanel_as_object.filter(
                            panel_id__in=Panel.objects.filter(year_code__startswith=request.GET['panel_year_code']))
                    if 'panel_id' in request.GET:
                        facultypanel_as_object = facultypanel_as_object.filter(
                            panel_id__in=Panel.objects.filter(panel_id__startswith=request.GET['panel_id']))
                    content = FacultyPanel_Serializer(
                        facultypanel_as_object, many=True)
                    response_list = []
                    for i in content.data:
                        f = Faculty.objects.get(fac_id=i["fac_id"])
                        p = Panel.objects.get(id=i["panel_id"])
                        l = {"fac_id": f.fac_id, "name": f.name, "email": f.email, "phone": f.phone, "panel_year_code": p.panel_year_code,
                             "panel_id": p.panel_id, "panel_name": p.panel_name, "is_coordinator": i["is_coordinator"]}
                        response_list.append(l)
                    return Response(response_list, status=status.HTTP_200_OK)
                elif(FacultyPanel.objects.filter(fac_id=user, panel_id=Panel.objects.filter(panel_year_code=panel_year_code, panel_id=panel_id).first()).exists()):
                    facultypanel_as_object = facultypanel_as_object = FacultyPanel.objects.filter(
                        fac_id=user, panel_id=Panel.objects.filter(panel_year_code=panel_year_code, panel_id=panel_id).first())
                    if 'fac_id' in request.GET:
                        facultypanel_as_object = facultypanel_as_object.filter(
                            fac_id__startswith=request.GET['fac_id'])
                    content = FacultyPanel_Serializer(
                        facultypanel_as_object, many=True)
                    response_list = []
                    for i in content.data:
                        f = Faculty.objects.get(fac_id=i["fac_id"])
                        p = Panel.objects.get(id=i["panel_id"])
                        l = {"fac_id": f.fac_id, "name": f.name, "email": f.email, "phone": f.phone, "panel_year_code": p.panel_year_code,
                             "panel_id": p.panel_id, "panel_name": p.panel_name, "is_coordinator": i["is_coordinator"]}
                        response_list.append(l)
                    return Response(response_list, status=status.HTTP_200_OK)
                else:
                    return Response(status=status.HTTP_403_FORBIDDEN)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, user, panel_year_code=None, panel_id=None):
        try:
            if(user == User.objects.get(id=jwt_decode_handler(request.META["HTTP_AUTHORIZATION"].split()[1])["user_id"]).get_username()):
                if(panel_id == None and panel_year_code == None and Faculty.objects.get(fac_id=user).is_admin == True):
                    serial_list = []
                    response_list = []
                    for i in request.data:
                        if("panel_year_code" in i and "panel_id" in i and "fac_id" in i):
                            if(Panel.objects.filter(panel_year_code=i["panel_year_code"], panel_id=i["panel_id"]).exists()):
                                p = Panel.objects.filter(
                                    panel_year_code=i["panel_year_code"], panel_id=i["panel_id"]).first()
                                d = {"panel_id": p.id, "fac_id": i["fac_id"]}
                                if("is_coordinator" in i):
                                    d.update(
                                        {"is_coordinator": i["is_coordinator"]})
                                serial = FacultyPanel_Serializer(
                                    data=d, partial=True)
                                if not serial.is_valid():
                                    response_list.append(
                                        {"value": i, "detail": serial.errors})
                                else:
                                    serial_list.append(serial)
                            else:
                                response_list.append(
                                    {"value": i, "detail": "panel does not exist"})
                        else:
                            response_list.append(
                                {"value": i, "detail": "attribute error"})
                    if(response_list == []):
                        for i in serial_list:
                            i.save()
                        return Response({"detail": "insert successful"}, status=status.HTTP_201_CREATED)
                    else:
                        return Response(response_list, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(status=status.HTTP_403_FORBIDDEN)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, user, panel_year_code=None, panel_id=None):
        try:
            if(user == User.objects.get(id=jwt_decode_handler(request.META["HTTP_AUTHORIZATION"].split()[1])["user_id"]).get_username()):
                if(panel_id == None and panel_year_code == None and Faculty.objects.get(fac_id=user).is_admin == True):
                    serial_list = []
                    response_list = []
                    for i in request.data:
                        if("panel_year_code" in i and "panel_id" in i and "fac_id" in i):
                            if(Panel.objects.filter(panel_year_code=i["panel_year_code"], panel_id=i["panel_id"]).exists()):
                                p = Panel.objects.filter(
                                    panel_year_code=i["panel_year_code"], panel_id=i["panel_id"]).first()
                                if(FacultyPanel.objects.filter(panel_id=p, fac_id=i["fac_id"]).exists()):
                                    f = FacultyPanel.objects.filter(
                                        panel_id=p, fac_id=i["fac_id"]).first()
                                    d = {"panel_id": p.id,
                                         "fac_id": i["fac_id"]}

                                    if("is_coordinator" in i):
                                        d.update(
                                            {"is_coordinator": i["is_coordinator"]})
                                    serial = FacultyPanel_Serializer(f,
                                                                     data=d, partial=True)
                                    if not serial.is_valid():
                                        response_list.append(
                                            {"value": i, "detail": serial.errors})
                                    else:
                                        serial_list.append(serial)
                                else:
                                    response_list.append(
                                        {"value": i, "detail": "faculty does not belong to the panel"})
                            else:
                                response_list.append(
                                    {"value": i, "detail": "panel does not exist"})
                        else:
                            response_list.append(
                                {"value": i, "detail": "attribute error"})
                    if(response_list == []):
                        for i in serial_list:
                            i.save()
                        return Response({"detail": "update successful"}, status=status.HTTP_201_CREATED)
                    else:
                        return Response(response_list, status=status.HTTP_400_BAD_REQUEST)
                elif(FacultyPanel.objects.filter(fac_id=user, is_coordinator=True, panel_id=Panel.objects.filter(panel_year_code=panel_year_code, panel_id=panel_id).first()).exists()):
                    response_list = []
                    serial_list = []
                    p = Panel.objects.filter(
                        panel_year_code=panel_year_code, panel_id=panel_id).first()
                    for i in request.data:
                        if("fac_id" in i):
                            if(FacultyPanel.objects.filter(panel_id=p, fac_id=i["fac_id"]).exists()):
                                f = FacultyPanel.objects.filter(
                                    panel_id=p, fac_id=i["fac_id"]).first()
                                d = {"panel_id": p.id, "fac_id": i["fac_id"]}
                                if("is_coordinator" in i):
                                    d.update(
                                        {"is_coordinator": i["is_coordinator"]})
                                serial = FacultyPanel_Serializer(f,
                                                                 data=d, partial=True)
                                print(serial)
                                if not serial.is_valid():
                                    response_list.append(
                                        {"value": i, "detail": serial.errors})
                                else:
                                    serial_list.append(serial)
                            else:
                                response_list.append(
                                    {"value": i, "detail": "faculty does not belong to the panel"})
                        else:
                            response_list.append(
                                {"value": i, "detail": "attribute error"})
                    if(response_list == []):
                        for i in serial_list:
                            i.save()
                        return Response({"detail": "update successful"}, status=status.HTTP_201_CREATED)
                else:
                    return Response(status=status.HTTP_403_FORBIDDEN)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user, panel_year_code=None, panel_id=None):
        try:
            if(user == User.objects.get(id=jwt_decode_handler(request.META["HTTP_AUTHORIZATION"].split()[1])["user_id"]).get_username()):
                if(panel_id == None and panel_year_code == None and Faculty.objects.get(fac_id=user).is_admin == True):
                    response_list = []
                    for i in request.data:
                        if("panel_year_code" in i and "panel_id" in i and "fac_id" in i):
                            if(Panel.objects.filter(panel_year_code=i["panel_year_code"], panel_id=i["panel_id"]).exists()):
                                p = Panel.objects.filter(
                                    panel_year_code=i["panel_year_code"], panel_id=i["panel_id"]).first()
                                f = FacultyPanel.objects.filter(
                                    panel_id=p, fac_id=i["fac_id"]).first()
                                d = {"panel_id": p.id, "fac_id": i["fac_id"]}
                                if("is_coordinator" in i):
                                    d.update(
                                        {"is_coordinator": i["is_coordinator"]})
                                serial = FacultyPanel_Serializer(f,
                                                                 data=d, partial=True)
                                if not serial.is_valid():
                                    response_list.append(
                                        {"value": i, "detail": serial.errors})
                            else:
                                response_list.append(
                                    {"value": i, "detail": "panel does not exist"})
                        else:
                            response_list.append(
                                {"value": i, "detail": "attribute error"})
                    if(response_list == []):
                        for i in request.data:
                            p = Panel.objects.filter(
                                panel_year_code=i["panel_year_code"], panel_id=i["panel_id"]).first()
                            f = FacultyPanel.objects.filter(
                                panel_id=p, fac_id=i["fac_id"]).first().delete()
                        return Response({"detail": "delete successful"}, status=status.HTTP_201_CREATED)
                    else:
                        return Response(response_list, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(status=status.HTTP_403_FORBIDDEN)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class Panel_List(APIView):

    parser_classes = [JSONParser]

    def get(self, request):
        try:
            Panel_as_object = Panel.objects.filter(
                panel_id=request.GET.__getitem__('panel_id'))
            content = Panel_Serializer(Panel_as_object, many=True)
            return Response(content.data)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        response_list = []
        for i in request.data:
            serial = Panel_Serializer(data=i)
            if not serial.is_valid():
                response_list.append({"value": i, "detail": serial.errors})
        if(response_list == []):
            for i in request.data:
                serial = Panel_Serializer(data=i)
                if serial.is_valid():
                    serial.save()
            return Response({"detail": "insert successful"}, status=status.HTTP_201_CREATED)
        else:
            return Response(response_list, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        serial = Panel_Serializer(Panel.objects.get(
            panel_id=request.data.get("panel_id")), data=request.data)
        try:
            if(serial.is_valid()):
                serial.save()
                return Response({"detail": "update successful"}, status=status.HTTP_202_ACCEPTED)
            else:
                return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        serial = Panel_Serializer(Panel.objects.get(
            panel_id=request.data.get("panel_id")), data=request.data)
        try:
            if serial.is_valid():
                Panel.objects.get(
                    panel_id=serial.data.get("panel_id")).delete()
                return Response({"detail": "delete successful"}, status=status.HTTP_200_OK)
            else:
                return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)


class PanelReview_List(APIView):

    parser_classes = [JSONParser]

    def get(self, request):
        try:
            PanelReview_as_object = PanelReview.objects.filter(
                panel=request.GET.__getitem__('panel'))
            content = PanelReview_Serializer(PanelReview_as_object, many=True)
            return Response(content.data)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        response_list = []
        for i in request.data:
            serial = PanelReview_Serializer(data=i)
            if not serial.is_valid():
                response_list.append({"value": i, "detail": serial.errors})
        if(response_list == []):
            for i in request.data:
                serial = PanelReview_Serializer(data=i)
                if serial.is_valid():
                    serial.save()
            return Response({"detail": "insert successful"}, status=status.HTTP_201_CREATED)
        else:
            return Response(response_list, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        serial = PanelReview_Serializer(PanelReview.objects.get(panel=request.data.get(
            "panel"), review_number=request.data.get("review_number")), data=request.data)
        try:
            if(serial.is_valid()):
                serial.save()
                return Response({"detail": "update successful"}, status=status.HTTP_202_ACCEPTED)
            else:
                return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        serial = PanelReview_Serializer(PanelReview.objects.get(panel=request.data.get(
            "panel"), review_number=request.data.get("review_number")), data=request.data)
        try:
            if serial.is_valid():
                PanelReview.objects.get(panel=request.data.get(
                    "panel"), review_number=request.data.get("review_number")).delete()
                return Response({"detail": "delete successful"}, status=status.HTTP_200_OK)
            else:
                return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)


class Review1_List(APIView):
    parser_classes = [JSONParser]

    def get(self, request):
        try:
            if 'srn' in request.GET:
                Review1_as_object = Review1.objects.filter(
                    srn__startswith=request.GET.__getitem__('srn'))
            else:
                Review1_as_object = Review1.objects.all()
            content = Review1_Serializer(Review1_as_object, many=True)
            return Response(content.data)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        response_list = []
        for i in request.data:
            serial = Review1_Serializer(data=i)
            if not serial.is_valid():
                response_list.append({"value": i, "detail": serial.errors})
        if(response_list == []):
            for i in request.data:
                serial = Review1_Serializer(data=i)
                if serial.is_valid():
                    serial.save()
            return Response({"detail": "insert successful"}, status=status.HTTP_201_CREATED)
        else:
            return Response(response_list, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        serial = Review1_Serializer(Review1.objects.get(srn=request.data.get(
            "srn"), fac=request.data.get('fac')), data=request.data)
        try:
            if(serial.is_valid()):
                serial.save()
                return Response({"detail": "update successful"}, status=status.HTTP_202_ACCEPTED)
            else:
                return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        serial = Review1_Serializer(Review1.objects.get(srn=request.data.get(
            "srn"), fac=request.data.get('fac')), data=request.data)
        try:
            if serial.is_valid():
                Review1.objects.get(srn=request.data.get(
                    "srn"), fac=request.data.get('fac')).delete()
                return Response({"detail": "delete successful"}, status=status.HTTP_200_OK)
            else:
                return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)


class Review2_List(APIView):
    parser_classes = [JSONParser]

    def get(self, request):
        try:
            if 'srn' in request.GET:
                Review2_as_object = Review2.objects.filter(
                    srn__startswith=request.GET.__getitem__('srn'))
            else:
                Review2_as_object = Review2.objects.all()
            content = Review2_Serializer(Review2_as_object, many=True)
            return Response(content.data)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        response_list = []
        for i in request.data:
            serial = Review2_Serializer(data=i)
            if not serial.is_valid():
                response_list.append({"value": i, "detail": serial.errors})
        if(response_list == []):
            for i in request.data:
                serial = Review2_Serializer(data=i)
                if serial.is_valid():
                    serial.save()
            return Response({"detail": "insert successful"}, status=status.HTTP_201_CREATED)
        else:
            return Response(response_list, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        serial = Review2_Serializer(Review2.objects.get(srn=request.data.get(
            "srn"), fac=request.data.get('fac')), data=request.data)
        try:
            if(serial.is_valid()):
                serial.save()
                return Response({"detail": "update successful"}, status=status.HTTP_202_ACCEPTED)
            else:
                return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        serial = Review2_Serializer(Review2.objects.get(srn=request.data.get(
            "srn"), fac=request.data.get('fac')), data=request.data)
        try:
            if serial.is_valid():
                Review2.objects.get(srn=request.data.get(
                    "srn"), fac=request.data.get('fac')).delete()
                return Response({"detail": "delete successful"}, status=status.HTTP_200_OK)
            else:
                return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)


class Review3_List(APIView):
    parser_classes = [JSONParser]

    def get(self, request):
        try:
            if 'srn' in request.GET:
                Review3_as_object = Review3.objects.filter(
                    srn__startswith=request.GET.__getitem__('srn'))
            else:
                Review3_as_object = Review3.objects.all()
            content = Review3_Serializer(Review3_as_object, many=True)
            return Response(content.data)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        response_list = []
        for i in request.data:
            serial = Review3_Serializer(data=i)
            if not serial.is_valid():
                response_list.append({"value": i, "detail": serial.errors})
        if(response_list == []):
            for i in request.data:
                serial = Review3_Serializer(data=i)
                if serial.is_valid():
                    serial.save()
            return Response({"detail": "insert successful"}, status=status.HTTP_201_CREATED)
        else:
            return Response(response_list, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        serial = Review3_Serializer(Review3.objects.get(srn=request.data.get(
            "srn"), fac=request.data.get('fac')), data=request.data)
        try:
            if(serial.is_valid()):
                serial.save()
                return Response({"detail": "update successful"}, status=status.HTTP_202_ACCEPTED)
            else:
                return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        serial = Review3_Serializer(Review3.objects.get(srn=request.data.get(
            "srn"), fac=request.data.get('fac')), data=request.data)
        try:
            if serial.is_valid():
                Review3.objects.get(srn=request.data.get(
                    "srn"), fac=request.data.get('fac')).delete()
                return Response({"detail": "delete successful"}, status=status.HTTP_200_OK)
            else:
                return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)


class Review4_List(APIView):
    parser_classes = [JSONParser]

    def get(self, request):
        try:
            if 'srn' in request.GET:
                Review4_as_object = Review4.objects.filter(
                    srn__startswith=request.GET.__getitem__('srn'))
            else:
                Review4_as_object = Review4.objects.all()
            content = Review4_Serializer(Review4_as_object, many=True)
            return Response(content.data)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        response_list = []
        for i in request.data:
            serial = Review4_Serializer(data=i)
            if not serial.is_valid():
                response_list.append({"value": i, "detail": serial.errors})
        if(response_list == []):
            for i in request.data:
                serial = Review4_Serializer(data=i)
                if serial.is_valid():
                    serial.save()
            return Response({"detail": "insert successful"}, status=status.HTTP_201_CREATED)
        else:
            return Response(response_list, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        serial = Review4_Serializer(Review4.objects.get(srn=request.data.get(
            "srn"), fac=request.data.get('fac')), data=request.data)
        try:
            if(serial.is_valid()):
                serial.save()
                return Response({"detail": "update successful"}, status=status.HTTP_202_ACCEPTED)
            else:
                return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        serial = Review4_Serializer(Review4.objects.get(srn=request.data.get(
            "srn"), fac=request.data.get('fac')), data=request.data)
        try:
            if serial.is_valid():
                Review4.objects.get(srn=request.data.get(
                    "srn"), fac=request.data.get('fac')).delete()
                return Response({"detail": "delete successful"}, status=status.HTTP_200_OK)
            else:
                return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)


class Review5_List(APIView):
    parser_classes = [JSONParser]

    def get(self, request):
        try:
            if 'srn' in request.GET:
                Review5_as_object = Review5.objects.filter(
                    srn__startswith=request.GET.__getitem__('srn'))
            else:
                Review5_as_object = Review5.objects.all()
            content = Review5_Serializer(Review5_as_object, many=True)
            return Response(content.data)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        response_list = []
        for i in request.data:
            serial = Review5_Serializer(data=i)
            if not serial.is_valid():
                response_list.append({"value": i, "detail": serial.errors})
        if(response_list == []):
            for i in request.data:
                serial = Review5_Serializer(data=i)
                if serial.is_valid():
                    serial.save()
            return Response({"detail": "insert successful"}, status=status.HTTP_201_CREATED)
        else:
            return Response(response_list, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        serial = Review5_Serializer(Review5.objects.get(srn=request.data.get(
            "srn"), fac=request.data.get('fac')), data=request.data)
        try:
            if(serial.is_valid()):
                serial.save()
                return Response({"detail": "update successful"}, status=status.HTTP_202_ACCEPTED)
            else:
                return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        serial = Review5_Serializer(Review5.objects.get(srn=request.data.get(
            "srn"), fac=request.data.get('fac')), data=request.data)
        try:
            if serial.is_valid():
                Review5.objects.get(srn=request.data.get(
                    "srn"), fac=request.data.get('fac')).delete()
                return Response({"detail": "delete successful"}, status=status.HTTP_200_OK)
            else:
                return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)


class Student_List(APIView):
    parser_classes = [JSONParser]
    permission_classes = [IsAuthenticated]

    def get(self, request, user, panel_year_code=None, panel_id=None, review_number=None):
        try:
            if(user == User.objects.get(id=jwt_decode_handler(request.META["HTTP_AUTHORIZATION"].split()[1])["user_id"]).get_username()):
                student_as_object = Student.objects.all().order_by('-srn')
                if(panel_id == None and panel_year_code == None and Faculty.objects.get(fac_id=user).is_admin == True):
                    pass                    
                elif(FacultyPanel.objects.filter(fac_id=user, panel_id=Panel.objects.filter(panel_year_code=panel_year_code, panel_id=panel_id).first()).exists()):
                    id = Panel.objects.filter(
                        panel_year_code=panel_year_code, panel_id=panel_id).first().id
                    if(review_number == None):
                        student_as_object = student_as_object.filter(team_id__in=Team.objects.filter(
                            panel_id=id))
                    else:
                        student_as_object = student_as_object.filter(team_id__in=TeamFacultyReview.objects.filter(team_id__in=Team.objects.filter(panel_id=id),
                                                                                                                  fac_id=user, review_number=review_number).values('team_id'))
                else:
                    return Response(status=status.HTTP_403_FORBIDDEN)
                if 'srn' in request.GET:
                        student_as_object = student_as_object.filter(
                            srn__startswith=request.GET['srn'])
                if 'name' in request.GET:
                    student_as_object = student_as_object.filter(
                        name__startswith=request.GET['name'])
                d = list(student_as_object.values())
                for i in d:
                    if "team_id_id" in i and i["team_id_id"] != None:
                        t = Team.objects.get(id=i.pop("team_id_id"))
                        i["team_year_code"] = t.team_year_code
                        i["team_id"] = t.team_id
                    else:
                        i.pop("team_id_id")
                        i["team_year_code"] = None
                        i["team_id"] = None
                    if("dept_id" in i):
                        i["dept"] = i.pop("dept_id")
                return Response(d, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, user, panel_year_code=None, panel_id=None):
        try:
            if(user == User.objects.get(id=jwt_decode_handler(request.META["HTTP_AUTHORIZATION"].split()[1])["user_id"]).get_username()):
                if(panel_id == None and panel_year_code == None and Faculty.objects.get(fac_id=user).is_admin == True):
                    response_list = []
                    serial_list = []
                    for i in request.data:
                        if("team_id" in i and i["team_id"] != None and "team_year_code" in i and i["team_year_code"] != None):
                            t = Team.objects.filter(
                                team_id=i["team_id"], team_year_code=i["team_year_code"])
                            i.pop("team_year_code")
                            if(t.exists()):
                                i["team_id"] = t.first().id
                            else:
                                i["team_id"] = None
                        else:
                            i.pop("team_year_code")
                            i["team_id"] = None
                        serial = Student_Serializer(data=i)
                        if not serial.is_valid():
                            response_list.append(
                                {"value": i, "detail": serial.errors})
                        else:
                            serial_list.append(serial)
                    if(response_list == []):
                        for i in serial_list:
                            i.save()
                        return Response({"detail": "insert successful"}, status=status.HTTP_201_CREATED)
                    else:
                        return Response(response_list, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"detail": "only project administrator can insert"}, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, user, panel_year_code=None, panel_id=None):
        try:
            if(user == User.objects.get(id=jwt_decode_handler(request.META["HTTP_AUTHORIZATION"].split()[1])["user_id"]).get_username()):
                if(panel_id == None and panel_year_code == None and Faculty.objects.get(fac_id=user).is_admin == True):
                    response_list = []
                    serial_list = []
                    for i in request.data:
                        if("team_id" in i and i["team_id"] != None and "team_year_code" in i and i["team_year_code"] != None):
                            t = Team.objects.filter(
                                team_id=i["team_id"], team_year_code=i["team_year_code"])
                            i.pop("team_year_code")
                            if(t.exists()):
                                i["team_id"] = t.first().id
                            else:
                                i["team_id"] = None
                        else:
                            i.pop("team_year_code")
                            i["team_id"] = None
                        if(Student.objects.filter(srn=i["srn"]).exists()):
                            serial = Student_Serializer(Student.objects.get(
                                srn=i["srn"]), data=i)
                            if not serial.is_valid():
                                response_list.append(
                                    {"value": i, "detail": serial.errors})
                            else:
                                serial_list.append(serial)
                        else:
                            response_list.append(
                                {"value": i, "detail": "student does not exist"})
                    if(response_list == []):
                        for i in serial_list:
                            i.save()
                        return Response({"detail": "update successful"}, status=status.HTTP_202_ACCEPTED)
                    else:
                        return Response(response_list, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"detail": "only project administrator can update"}, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user, panel_year_code=None, panel_id=None):
        try:
            if(user == User.objects.get(id=jwt_decode_handler(request.META["HTTP_AUTHORIZATION"].split()[1])["user_id"]).get_username()):
                if(panel_id == None and panel_year_code == None and Faculty.objects.get(fac_id=user).is_admin == True):
                    response_list = []
                    serial_list = []
                    for i in request.data:
                        if("team_id" in i and i["team_id"] != None and "team_year_code" in i and i["team_year_code"] != None):
                            t = Team.objects.filter(
                                team_id=i["team_id"], team_year_code=i["team_year_code"])
                            i.pop("team_year_code")
                            if(t.exists()):
                                i["team_id"] = t.first().id
                            else:
                                i["team_id"] = None
                        else:
                            i.pop("team_year_code")
                            i["team_id"] = None
                        if(Student.objects.filter(srn=i["srn"]).exists()):
                            serial = Student_Serializer(Student.objects.get(
                                srn=i["srn"]), data=i)
                            if not serial.is_valid():
                                response_list.append(
                                    {"value": i, "detail": serial.errors})
                            else:
                                serial_list.append(serial)
                        else:
                            response_list.append(
                                {"value": i, "detail": "student does not exist"})
                    if(response_list == []):
                        for i in request.data:
                            Student.objects.get(srn=i["srn"]).delete()
                        return Response({"detail": "delete successful"}, status=status.HTTP_202_ACCEPTED)
                    else:
                        return Response(response_list, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"detail": "only project administrator can delete"}, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class Team_List(APIView):
    parser_classes = [JSONParser]
    permission_classes = [IsAuthenticated]

    def get(self, request, user, panel_year_code=None, panel_id=None, review_number=None):
        try:
            if(user == User.objects.get(id=jwt_decode_handler(request.META["HTTP_AUTHORIZATION"].split()[1])["user_id"]).get_username()):
                team_as_object = Team.objects.all().order_by("-team_year_code","team_id")
                if(panel_id == None and panel_year_code == None and Faculty.objects.get(fac_id=user).is_admin == True):
                    if 'panel_year_code' in request.GET:
                        team_as_object = team_as_object.filter(
                            panel_id__in=Panel.objects.filter(panel_year_code__starteswith=request.GET['panel_year_code']))
                    if 'panel_id' in request.GET:
                        team_as_object = team_as_object.filter(
                            panel_id__in=Panel.objects.filter(panel_id__starteswith=request.GET['panel_id']))
                elif(FacultyPanel.objects.filter(fac_id=user, panel_id=Panel.objects.filter(panel_year_code=panel_year_code, panel_id=panel_id).first()).exists()):
                    id = Panel.objects.filter(
                        panel_year_code=panel_year_code, panel_id=panel_id).first().id
                    if(review_number == None):
                        team_as_object = Team.objects.filter(panel_id=id)
                    else:
                        team_as_object = TeamFacultyReview.objects.filter(team_id__in=Team.objects.filter(panel_id=id),
                                                                          fac_id=user, review_number=review_number).values('team_id')
                else:
                    return Response(status=status.HTTP_403_FORBIDDEN)
                if 'team_id' in request.GET:
                    team_as_object = team_as_object.filter(
                        team_id__startswith=request.GET['team_id'])
                if 'team_year_code' in request.GET:
                    team_as_object = team_as_object.filter(
                        team_year_code__startswith=request.GET['team_year_code'])
                if 'team_name' in request.GET:
                    team_as_object = team_as_object.filter(
                        team_name__startswith=request.GET['team_name'])
                
                d = list(team_as_object.values())
                for i in d:
                    i.pop("id")
                    if "panel_id_id" in i and i["panel_id_id"] != None:
                        p = Panel.objects.get(id=i.pop("panel_id_id"))
                        i["panel_year_code"] = p.panel_year_code
                        i["panel_id"] = p.panel_id
                    else:
                        if("panel_id_id" in i):
                            i.pop("panel_id_id")
                        i["panel_year_code"] = None
                        i["panel_id"] = None
                    if("guide_id" in i):
                        i["guide"] = i.pop("guide_id")
                return Response(d, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, user, panel_year_code=None, panel_id=None):
        try:
            if(user == User.objects.get(id=jwt_decode_handler(request.META["HTTP_AUTHORIZATION"].split()[1])["user_id"]).get_username()):
                if(panel_id == None and panel_year_code == None and Faculty.objects.get(fac_id=user).is_admin == True):
                    response_list = []
                    serial_list = []
                    for i in request.data:
                        i["team_id"]=add_one_team(i["team_year_code"])
                        if("panel_id" in i and i["panel_id"] != None and "panel_year_code" in i and i["panel_year_code"] != None):
                            p = Panel.objects.filter(
                                panel_id=i["panel_id"], panel_year_code=i["panel_year_code"])
                            i.pop("panel_year_code")
                            if(p.exists()):
                                i["panel_id"] = p.first().id
                            else:
                                i["panel_id"] = None
                        else:
                            i.pop("panel_year_code")
                            i["panel_id"] = None
                        serial = Team_Serializer(data=i)
                        if not serial.is_valid():
                            response_list.append(
                                {"value": i, "detail": serial.errors})
                        else:
                            serial_list.append(serial)
                    if(response_list == []):
                        for i in serial_list:
                            i.save()
                        return Response({"detail": "insert successful"}, status=status.HTTP_201_CREATED)
                    else:
                        return Response(response_list, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"detail": "only project administrator can insert"}, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, user, panel_year_code=None, panel_id=None):
        try:
            if(user == User.objects.get(id=jwt_decode_handler(request.META["HTTP_AUTHORIZATION"].split()[1])["user_id"]).get_username()):
                if(panel_id == None and panel_year_code == None and Faculty.objects.get(fac_id=user).is_admin == True):
                    response_list = []
                    serial_list = []
                    for i in request.data:
                        if("panel_id" in i and i["panel_id"] != None and "panel_year_code" in i and i["panel_year_code"] != None):
                            p = Panel.objects.filter(
                                panel_id=i["panel_id"], panel_year_code=i["panel_year_code"])
                            i.pop("panel_year_code")
                            if(p.exists()):
                                i["panel_id"] = p.first().id
                            else:
                                i["panel_id"] = None
                        else:
                            i.pop("panel_year_code")
                            i["panel_id"] = None
                        if(Team.objects.filter(team_id=i["team_id"], team_year_code=i["team_year_code"]).exists()):
                            serial = Team_Serializer(Team.objects.filter(
                                team_id=i["team_id"], team_year_code=i["team_year_code"]).first(), data=i)
                            if not serial.is_valid():
                                response_list.append(
                                    {"value": i, "detail": serial.errors})
                            else:
                                serial_list.append(serial)
                        else:
                            response_list.append(
                                {"value": i, "detail": "Team does not exist"})
                    if(response_list == []):
                        for i in serial_list:
                            i.save()
                        return Response({"detail": "update successful"}, status=status.HTTP_202_ACCEPTED)
                    else:
                        return Response(response_list, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"detail": "only project administrator can update"}, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user, panel_year_code=None, panel_id=None):
        try:
            if(user == User.objects.get(id=jwt_decode_handler(request.META["HTTP_AUTHORIZATION"].split()[1])["user_id"]).get_username()):
                if(panel_id == None and panel_year_code == None and Faculty.objects.get(fac_id=user).is_admin == True):
                    response_list = []
                    serial_list = []
                    for i in request.data:
                        if("panel_id" in i and i["panel_id"] != None and "panel_year_code" in i and i["panel_year_code"] != None):
                            p = Panel.objects.filter(
                                panel_id=i["panel_id"], panel_year_code=i["panel_year_code"])
                            i.pop("panel_year_code")
                            if(p.exists()):
                                i["panel_id"] = p.first().id
                            else:
                                i["panel_id"] = None
                        else:
                            i.pop("panel_year_code")
                            i["panel_id"] = None
                        if(Team.objects.filter(team_id=i["team_id"], team_year_code=i["team_year_code"]).exists()):
                            serial = Team_Serializer(Team.objects.filter(
                                team_id=i["team_id"], team_year_code=i["team_year_code"]).first(), data=i)
                            if not serial.is_valid():
                                response_list.append(
                                    {"value": i, "detail": serial.errors})
                            else:
                                serial_list.append(serial)
                        else:
                            response_list.append(
                                {"value": i, "detail": "Team does not exist"})
                    if(response_list == []):
                        for i in request.data:
                            Student.objects.get(srn=i["srn"]).delete()
                        return Response({"detail": "delete successful"}, status=status.HTTP_202_ACCEPTED)
                    else:
                        return Response(response_list, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"detail": "only project administrator can delete"}, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class TeamFacultyReview_List(APIView):
    parser_classes = [JSONParser]

    def get(self, request):
        try:
            TeamFacultyReview_as_object = TeamFacultyReview.objects.all()
            content = TeamFacultyReview_Serializer(
                TeamFacultyReview_as_object, many=True)
            return Response(content.data)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        response_list = []
        for i in request.data:
            serial = TeamFacultyReview_Serializer(data=i)
            if not serial.is_valid():
                response_list.append({"value": i, "detail": serial.errors})
        if(response_list == []):
            for i in request.data:
                serial = TeamFacultyReview_Serializer(data=i)
                if serial.is_valid():
                    serial.save()
            return Response({"detail": "insert successful"}, status=status.HTTP_201_CREATED)
        else:
            return Response(response_list, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        serial = TeamFacultyReview_Serializer(TeamFacultyReview.objects.get(team=request.data.get(
            "team"), fac=request.data.get('fac'), review_number=request.data.get('review_number')), data=request.data)
        try:
            if(serial.is_valid()):
                serial.save()
                return Response({"detail": "update successful"}, status=status.HTTP_202_ACCEPTED)
            else:
                return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        serial = TeamFacultyReview_Serializer(TeamFacultyReview.objects.get(team=request.data.get(
            "team"), fac=request.data.get('fac'), review_number=request.data.get('review_number')), data=request.data)
        try:
            if serial.is_valid():
                TeamFacultyReview.objects.get(team=request.data.get("team"), fac=request.data.get(
                    'fac'), review_number=request.data.get('review_number')).delete()
                return Response({"detail": "delete successful"}, status=status.HTTP_200_OK)
            else:
                return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)


class Team_Student_CSV(APIView):

    parser_classes = [JSONParser]

    def post(self, request):

        response_list = []
        for i in request.data:
            team_data = {"name": i["team_name"], "description": i["description"],
                         "guide": i["guide"], "panel": i["panel"], "team_id": i["team_id"]}
            team_serial = Team_Serializer(data=team_data)
            if team_serial.is_valid():
                team_serial.save()
            else:
                response_list.append(
                    {"value": i, "detail": team_serial.errors})
            if(len(i["srn"]) == len(i["name"]) and len(i["name"]) == len(i["email"]) and len(i["email"]) == len(i["phone"]) and len(i["phone"]) == len(i["dept"])):
                student_data = [{"srn": i["srn"][j], "name":i["name"][j], "email":i["email"][j],
                                 "phone":i["phone"][j], "dept":i["dept"][j]} for j in range(len(i["srn"]))]
                for k in student_data:
                    student_serial = Student_Serializer(data=k)
                    if student_serial.is_valid():
                        student_serial.save()

                    else:
                        response_list.append(
                            {"value": i, "detail": student_serial.errors})
            else:
                response_list.append({"values": i, "detail": "mismatch data"})
        if(response_list == []):
            return Response({"detail": "insert successful"}, status=status.HTTP_201_CREATED)
        else:
            return Response(response_list, status=status.HTTP_400_BAD_REQUEST)


# (TokenObtainPairView,TokenRefreshView)

class TokenBlackList(APIView):

    parser_classes = [JSONParser]
    #permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        if(User.objects.filter(username=request.data["username"]).exists()):
            user = User.objects.get(username=request.data["username"])
            if(user.check_password(request.data["password"])):
                token = RefreshToken.for_user(user)
                return Response({'refresh': str(token), 'access': str(token.access_token), 'user': request.data["username"], 'name': str(user.get_full_name())}, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "incorrect password"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"detail": "username does not exist"}, status=status.HTTP_400_BAD_REQUEST)


class RefreshView(APIView):
    parser_classes = [JSONParser]
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        try:
            if("refresh" in request.data):
                token = RefreshToken(request.data["refresh"])
                if(not token.check_exp(claim='exp', current_time=timezone.now())):
                    return Response({"access": str(token.access_token)}, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "token invalid or expired, re-login to proceed"}, status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response({"detail": "token invalid or expired, re-login to proceed"}, status=status.HTTP_400_BAD_REQUEST)


class ChangePassword(APIView):
    parser_classes = [JSONParser]

    def post(self, request, user):
        try:
            if(user == User.objects.get(id=jwt_decode_handler(request.META["HTTP_AUTHORIZATION"].split()[1])["user_id"]).get_username()):
                U = User.objects.get(id=jwt_decode_handler(
                    request.META["HTTP_AUTHORIZATION"].split()[1])["user_id"])
                if("new_password" in request.data and "confirm_password" in request.data and "old_password" in request.data):
                    if(U.check_password(request.data["old_password"])):
                        if((request.data["new_password"] == request.data["confirm_password"]) and (request.data["new_password"] != "") and (request.data["new_password"] != "")):
                            U.set_password(request.data["new_password"])
                            U.save()
                            return Response({"detail": "password change successful"}, status=status.HTTP_200_OK)
                        else:
                            return Response({"detail": "passwords not matching or blank"}, status=status.HTTP_406_NOT_ACCEPTABLE)
                    else:
                        return Response({"detail": "previous password not valid"}, status=status.HTTP_403_FORBIDDEN)
                else:
                    return Response({"detail": "attributes not sufficient"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"detail": "user credentials do not match"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"detail": "change password unsuccessful"}, status=status.HTTP_400_BAD_REQUEST)
