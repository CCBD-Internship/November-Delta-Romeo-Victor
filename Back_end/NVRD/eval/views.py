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
import datetime
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
    permission_classes = (AllowAny,)

    def get(self, request, user):
        try:
            dept_as_object = Department.objects.all()
            content = Department_Serializer(dept_as_object, many=True)
            return Response(content.data)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class Faculty_List(APIView):

    parser_classes = [JSONParser]

    def get(self, request, user):
        try:
            fid = User.objects.get(id=jwt_decode_handler(
                request.META["HTTP_AUTHORIZATION"].split()[1])["user_id"]).get_username()
            prof = Faculty.objects.get(fac_id=fid)
            if(prof.is_admin and prof.fac_id == user):
                faculty_as_object = Faculty.objects.filter(is_active=True)
                if "fac_id" in request.GET:
                    faculty_as_object = faculty_as_object(
                        fac_id=request.GET.__getitem__('fac_id'))
                content = Faculty_Serializer(faculty_as_object, many=True)
                return Response(content.data)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, user):
        try:
            if(user == User.objects.get(id=jwt_decode_handler(request.META["HTTP_AUTHORIZATION"].split()[1])["user_id"]).get_username()):
                if(Faculty.objects.filter(fac_id=user).first().is_admin == True):
                    valid_list = []
                    response_list = []
                    for i in request.data:
                        serial = Faculty_Serializer(data=i)
                        if not serial.is_valid():
                            response_list.append(
                                {"value": i, "detail": serial.errors})
                        else:
                            valid_list.append(serial)
                    if(response_list == []):
                        for i in valid_list:
                            if i.is_valid():
                                i.save()
                                User.objects.create_user(
                                    last_name=i["name"].value, username=i["fac_id"].value, password=i["fac_id"].value, email=i["email"].value)
                        return Response({"detail": "insert successful"}, status=status.HTTP_201_CREATED)
                    else:
                        return Response(response_list, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"detail": "only project administrator can insert"}, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({"details": "invalid user"}, status=status.HTTP_403_FORBIDDEN)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, user):
        try:
            if(user == User.objects.get(id=jwt_decode_handler(request.META["HTTP_AUTHORIZATION"].split()[1])["user_id"]).get_username()):
                if(Faculty.objects.get(fac_id=user).is_admin == True):
                    valid_list = []
                    response_list = []
                    for i in request.data:
                        if(Faculty.objects.filter(fac_id=i["fac_id"]).exists()):
                            serial = Faculty_Serializer(Faculty.objects.filter(
                                fac_id=i.get("fac_id")).first(), data=i)
                            if "email" in i:
                                u = User.objects.get(id=user)
                                u.email = i["email"]
                                u.save(

                                )
                            if not serial.is_valid():
                                response_list.append(
                                    {"value": i, "detail": serial.errors})
                            else:
                                valid_list.append(serial)
                        else:
                            response_list.append(
                                {"value": i, "detail": "faculty does not exist"})
                    if(response_list == []):
                        for i in valid_list:
                            if i.is_valid():
                                i.save()
                        return Response({"detail": "update successful"}, status=status.HTTP_201_CREATED)
                    else:
                        return Response(response_list, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"detail": "only project administrator can update"}, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({"details": "invalid token"}, status=status.HTTP_403_FORBIDDEN)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


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
                elif(panel_id != None and panel_year_code != None and FacultyPanel.objects.filter(fac_id=user, panel_id=Panel.objects.filter(panel_year_code=panel_year_code, panel_id=panel_id).first()).exists()):
                    facultypanel_as_object = FacultyPanel.objects.filter(
                        panel_id=Panel.objects.filter(panel_year_code=panel_year_code, panel_id=panel_id).first())
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
                            teams = Team.objects.filter(
                                panel_id=None, guide=i["fac_id"].value)
                            for t in teams:
                                t.panel_id = i["panel_id"].value
                                t.save()
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

    def get(self, request, user, panel_id=None, panel_year_code=None):
        try:
            if(user == User.objects.get(id=jwt_decode_handler(request.META["HTTP_AUTHORIZATION"].split()[1])["user_id"]).get_username()):
                # admin
                if(Faculty.objects.get(fac_id=user).is_admin == True):
                    if(panel_id == None and panel_year_code == None):
                        panel_as_object = Panel.objects.all()
                    else:
                        panel_as_object = Panel.objects.filter(
                            panel_id=panel_id, panel_year_code=panel_year_code)
                    if 'time' in request.GET:
                        panel_as_object = panel_as_object.filter(
                            fac_id__gte=request.GET['time'])
                    if 'active' in request.GET:
                        panel_as_object = panel_as_object.filter(
                            is_active=request.GET['active'])
                        print(panel_as_object)
                    if 'cord' in request.GET:
                        if(FacultyPanel.objects.get(fac_id=user).is_coordinator == True):
                            pp = [i.panel_id.panel_id for i in FacultyPanel.objects.filter(
                                fac_id=user, is_coordinator=True)]
                            panel_as_object = panel_as_object.filter(
                                panel_id__in=pp)
                        else:
                            return Response(status=status.HTTP_403_FORBIDDEN)
                    content = Panel_Serializer(panel_as_object, many=True)
                    response_list = []
                    print(content.data)
                    for i in content.data:
                        response_list.append(i)
                    return Response(response_list, status=status.HTTP_200_OK)
                elif(Faculty.objects.get(fac_id=user).is_admin == False and Faculty.objects.get(fac_id=user).exists()):
                    panel_as_object = FacultyPanel.objects.filter(fac_id=user)
                    if 'time' in request.GET:
                        panel_as_object = panel_as_object.filter(
                            fac_id__gte=request.GET['time'])
                    if 'active' in request.GET:
                        panel_as_object = panel_as_object.filter(
                            panel_id__in=Panel.objects.filter(is_active=request.GET['active']))
                    if 'cord' in request.GET:
                        panel_as_object = panel_as_object.filter(
                            panel_id__in=FacultyPanel.objects.filter(fac_id=user, is_coordinator=True))
                    else:
                        return Response(status=status.HTTP_403_FORBIDDEN)
                    content = Panel_Serializer(panel_as_object, many=True)
                    response_list = []
                    for i in content.data:
                        response_list.append(i)
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
                    response_list = []
                    serial_list = []
                    for i in request.data:
                        i["panel_id"] = add_one_panel(i["panel_year_code"])
                        serial = Panel_Serializer(data=i)
                        if not serial.is_valid():
                            response_list.append(
                                {"value": i, "detail": serial.errors})
                        else:
                            serial_list.append(serial)
                    if(response_list == []):
                        for i in serial_list:
                            i.save()
                            p = Panel.objects.filter(
                                panel_id=i["panel_id"].value, panel_year_code=i["panel_year_code"].value).first()
                            for k in range(1, 6):
                                PanelReview(review_number=k, panel_id=p, open_time=timezone.now(), close_time=timezone.make_aware(datetime.datetime.now(
                                )+datetime.timedelta(days=365), timezone.get_default_timezone()), id=i["panel_year_code"].value+'_'+i["panel_id"].value+'_'+str(k)).save()
                        return Response({"detail": "insert successful"}, status=status.HTTP_201_CREATED)
                    else:
                        return Response(response_list, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"detail": "only project administrator can insert"}, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, user, panel_id=None, panel_year_code=None):
        try:
            if(user == User.objects.get(id=jwt_decode_handler(request.META["HTTP_AUTHORIZATION"].split()[1])["user_id"]).get_username()):
                if((Faculty.objects.get(fac_id=user).is_admin == True)):
                    response_list = []
                    valid_list = []
                    for i in request.data:
                        if(Panel.objects.filter(panel_id=i["panel_id"], panel_year_code=i["panel_year_code"]).exists()):
                            serial = Panel_Serializer(Panel.objects.filter(panel_id=i.get(
                                "panel_id"), panel_year_code=i.get("panel_year_code")).first(), data=i)
                            if not serial.is_valid():
                                response_list.append(
                                    {"value": i, "detail": serial.errors})
                            else:
                                valid_list.append(serial)
                        else:
                            response_list.append(
                                {"value": i, "detail": "panel does not exist"})
                    if(response_list == []):
                        for i in valid_list:
                            if i.is_valid():
                                i.save()
                        return Response({"detail": "update successful"}, status=status.HTTP_202_ACCEPTED)
                    else:
                        return Response(response_list, status=status.HTTP_400_BAD_REQUEST)
                else:
                    valid_list = []
                    response_list = []
                    for i in request.data:
                        if(Panel.objects.filter(panel_id=i["panel_id"], panel_year_code=i["panel_year_code"]).exists()):
                            p = Panel.objects.filter(
                                panel_id=i["panel_id"], panel_year_code=i["panel_year_code"]).first()
                            if FacultyPanel.objects.filter(fac_id=user, panel_id=p).exists():
                                f = FacultyPanel.objects.filter(
                                    fac_id=user, panel_id=p).first()
                                if not f.is_coordinator:
                                    response_list.append(
                                        {"value": i, "detail": "user not co-ordinator of given panel"})
                            else:
                                response_list.append(
                                    {"value": i, "detail": "user does not belong to given panel"})
                    if(response_list == []):
                        for i in request.data:
                            i.pop('id', 'ctime')
                        if(Panel.objects.filter(panel_id=i["panel_id"], panel_year_code=i["panel_year_code"]).exists()):
                            serial = Panel_Serializer(Panel.objects.filter(panel_id=i.get(
                                "panel_id"), panel_year_code=i.get("panel_year_code")).first(), data=i)
                            if not serial.is_valid():
                                response_list.append(
                                    {"value": i, "detail": serial.errors})
                            else:
                                valid_list.append(serial)
                        else:
                            response_list.append(
                                {"value": i, "detail": "panel does not exist"})
                        if(response_list == []):
                            for i in valid_list:
                                if i.is_valid():
                                    i.save()
                            return Response({"detail": "update successful"}, status=status.HTTP_202_ACCEPTED)
                        else:
                            return Response(response_list, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response(response_list, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"details": "invalid user"}, status=status.HTTP_403_FORBIDDEN)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user):
        try:
            if(user == User.objects.get(id=jwt_decode_handler(request.META["HTTP_AUTHORIZATION"].split()[1])["user_id"]).get_username()):
                if(Faculty.objects.get(fac_id=user).is_admin == True):
                    valid_list = []
                    response_list = []
                    for i in request.data:
                        serial = Panel_Serializer(Panel.objects.filter(
                            panel_id=i["panel_id"], panel_year_code=i["panel_year_code"]).first(), data=i)
                        if not serial.is_valid():
                            response_list.append(
                                {"value": i, "detail": serial.errors})
                        else:
                            valid_list.append(serial)
                    if(response_list == []):
                        for i in request.data:
                            Panel.objects.filter(
                                panel_id=i["panel_id"], panel_year_code=i["panel_year_code"]).first().delete()
                        return Response({"detail": "delete successful"}, status=status.HTTP_202_ACCEPTED)
                    else:
                        return Response(response_list, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"detail": "only project administrator can delete"}, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({"detail": "invalid token"}, status=status.HTTP_403_FORBIDDEN)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class PanelReview_List(APIView):

    parser_classes = [JSONParser]

    def get(self, request, user, panel_year_code, panel_id):
        try:
            if(user == User.objects.get(id=jwt_decode_handler(request.META["HTTP_AUTHORIZATION"].split()[1])["user_id"]).get_username()):
                p = Panel.objects.filter(
                    panel_id=panel_id, panel_year_code=panel_year_code).first()
                if(FacultyPanel.objects.filter(fac_id=user, panel_id=p, is_coordinator=True).exists()):
                    PanelReview_as_object = PanelReview.objects.filter(
                        panel_id=p, fac_id=user)
                    content = PanelReview_Serializer(
                        PanelReview_as_object, many=True)
                    return Response(content.data, status=status.HTTP_200_OK)
                else:
                    return Response({"detail": "only panel coordinator can access"}, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, user, panel_year_code, panel_id, review_number):
        p_id = Panel.objects.get(
            panel_id=panel_id, panel_year_code=panel_year_code).id
        c2 = FacultyPanel.objects.filter(
            fac_id=user, id=p_id).first().is_coordinator
        if(user == User.objects.get(id=jwt_decode_handler(request.META["HTTP_AUTHORIZATION"].split()[1])["user_id"]).get_username() and c2 == True):
            valid_list = []
            response_list = []
            if(PanelReview.objects.filter(id=p_id, review_number=review_number).exists()):
                p = PanelReview.objects.get(
                    id=p_id, review_number=review_number)
            else:
                return Response({"value": panel_id, "detail": "panel does no exist"}, status=status.HTTP_400_BAD_REQUEST)
            for i in request.data:
                if(panel_id == i["panel_id"] and panel_year_code == i["panel_year_code"]):
                    serial = PanelReview_Serializer(PanelReview.objects.filter(panel_id=i.get("panel_id"),
                                                                               panel_year_code=i.get("panel_year_code"), review_number=i.get("review_number")), data=i)
                    if not serial.is_valid():
                        response_list.append(
                            {"value": i, "detail": serial.errors})
                    else:
                        valid_list.append(serial)
                else:
                    response_list.append(
                        {"value": i, "detail": "panel does not match"})
            if(response_list == []):
                for i in valid_list:
                    if i.is_valid():
                        i.save()
                return Response({"detail": "update successful"}, status=status.HTTP_202_ACCEPTED)
            else:
                return Response(response_list, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


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
                team_as_object = Team.objects.all().order_by("-team_year_code", "team_id")
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
                    null_set_list = []
                    for i in request.data:
                        i["team_id"] = add_one_team(i["team_year_code"])
                        if("panel_id" in i and i["panel_id"] != None and "panel_year_code" in i and i["panel_year_code"] != None):
                            p = Panel.objects.filter(
                                panel_id=i["panel_id"], panel_year_code=i["panel_year_code"], is_active=True)
                            i.pop("panel_year_code")
                            if(p.exists() and "guide" in i and FacultyPanel.objects.filter(fac_id=i["guide"], panel_id=p.id).exists()):
                                i["panel_id"] = p.first().id
                            else:
                                i["panel_id"] = None
                                null_set_list.append(
                                    {"value": i, "detail": "panel set to NULL,either panel does not or guide does not exist in panel"})
                        else:
                            i.pop("panel_year_code")
                            i["panel_id"] = None
                            null_set_list.append(
                                {"value": i, "detail": "panel set to NULL,either panel does not or guide does not exist in panel"})
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
                        response_list.extend(null_set_list)
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
                    null_set_list = []
                    for i in request.data:
                        if("panel_id" in i and i["panel_id"] != None and "panel_year_code" in i and i["panel_year_code"] != None):
                            p = Panel.objects.filter(
                                panel_id=i["panel_id"], panel_year_code=i["panel_year_code"])
                            i.pop("panel_year_code")
                            if(p.exists() and "guide" in i and FacultyPanel.objects.filter(fac_id=i["guide"], panel_id=p.id).exists()):
                                i["panel_id"] = p.first().id
                            else:
                                i["panel_id"] = None
                                null_set_list.append(
                                    {"value": i, "detail": "panel set to NULL,either panel does not or guide does not exist in panel"})
                        else:
                            i.pop("panel_year_code")
                            i["panel_id"] = None
                            null_set_list.append(
                                {"value": i, "detail": "panel set to NULL,either panel does not or guide does not exist in panel"})
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
                        response_list.extend(null_set_list)
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
                            Team.objects.filter(
                                team_id=i["team_id"], team_year_code=i["team_year_code"]).first().delete()
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

    def post(self, request, user, panel_year_code, panel_id):
        try:
            if(user == User.objects.get(id=jwt_decode_handler(request.META["HTTP_AUTHORIZATION"].split()[1])["user_id"]).get_username()):
                accept = []
                fail = []
                for i in request.data:
                    if(panel_id == i["panel_id"] and panel_year_code == i["panel_year_code"]):
                        p_id = Panel.objects.filter(
                            panel_id=panel_id, panel_year_code=panel_year_code).first().id
                        if FacultyPanel.objects.filter(fac_id=user, id=p_id).first().is_coordinator == True:
                            if Team.filter(team_year_code=i["team_year_code"], team_id=i["team_id"]).first().guide.fac_id in i["fac"]:
                                for teach in i["fac"]:
                                    row = TeamFacultyReview_Serializer(team_year_code=i["team_year_code"], team_id=i["team_id"], fac_id=teach, review_number=i["review_number"],
                                                                       review="Unreviewed", id=str(i["team_year_code"])+'_'+str(i["team_id"])+'_'+str(teach)+'_'+str(i["review_number"]))
                                    if row.is_valid():
                                        accept.append(row)
                                    else:
                                        fail.append(
                                            {"value": i, "detail": row.errors})
                            else:
                                return Response({"detail": "guide aint here man"}, status=status.HTTP_400_BAD_REQUEST)

                        else:
                            return Response({"detail": "you aint a coord for thiss panel bruv"}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response({"detail": "he aint in this panel dude"}, status=status.HTTP_400_BAD_REQUEST)
                if fail == []:
                    for i in accept:
                        if i.is_valid:
                            i.save()
                            if i["review_number"].value == 1:
                                team_pk = Team.objects.filter(
                                    team_year_code=i["team_year_code"].value, team_id=i["team_id"].value).first().id
                                students = Student.objects.filter(
                                    team_id=team_pk)
                                for studs in students:
                                    Review1(srn=studs.srn, fac_id=i["fac_id"].value, concept_of_the_work=0, methodology_proposed=0, literature_survey=0, knowledge_on_the_project=0,
                                            comments="not yet scored", id=str(studs.srn)+'_'+i["fac_id"].value+'_'+str(i["review_number"].value)).save()
                            elif i["review_number"].value == 2:
                                team_pk = Team.objects.filter(
                                    team_year_code=i["team_year_code"].value, team_id=i["team_id"].value).first().id
                                students = Student.objects.filter(
                                    team_id=team_pk)
                                for studs in students:
                                    Review2(srn=studs.srn, fac_id=i["fac_id"].value, requirements_specification=0, user_interface_use_cases=0, understanding_of_technology_platform_middleware=0, viva_voce=0,
                                            comments="not yet scored", id=str(studs.srn)+'_'+i["fac_id"].value+'_'+str(i["review_number"].value)).save()
                            elif i["review_number"].value == 3:
                                team_pk = Team.objects.filter(
                                    team_year_code=i["team_year_code"].value, team_id=i["team_id"].value).first().id
                                students = Student.objects.filter(
                                    team_id=team_pk)
                                for studs in students:
                                    Review3(srn=studs.srn, fac_id=i["fac_id"].value, design_philosophy_methodology=0, user_interface_design_backend_design_and_design_for_any_algorithms=0, suitably_of_design_in_comparison_to_the_technology_proposed=0, progress_of_the_project_work=0, viva_voce=0,
                                            comments="not yet scored", id=str(studs.srn)+'_'+i["fac_id"].value+'_'+str(i["review_number"].value)).save()
                            elif i["review_number"].value == 4:
                                team_pk = Team.objects.filter(
                                    team_year_code=i["team_year_code"].value, team_id=i["team_id"].value).first().id
                                students = Student.objects.filter(
                                    team_id=team_pk)
                                for studs in students:
                                    Review4(srn=studs.srn, fac_id=i["fac_id"].value, project_work_results=0, quality_of_demo=0, project_report=0, viva_voce=0,
                                            comments="not yet scored", id=str(studs.srn)+'_'+i["fac_id"].value+'_'+str(i["review_number"].value)).save()
                            elif i["review_number"].value == 5:
                                team_pk = Team.objects.filter(
                                    team_year_code=i["team_year_code"].value, team_id=i["team_id"].value).first().id
                                students = Student.objects.filter(
                                    team_id=team_pk)
                                for studs in students:
                                    Review5(srn=studs.srn, fac_id=i["fac_id"].value, project_work_results=0, quality_of_demo=0, project_report=0, viva_voce=0,
                                            comments="not yet scored", id=str(studs.srn)+'_'+i["fac_id"].value+'_'+str(i["review_number"].value)).save()

                else:
                    return Response(fail, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"detail": "Identify youself"}, status=status.HTTP_401_UNAUTHORIZED)

        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user, panel_year_code, panel_id):
        try:
            if(user == User.objects.get(id=jwt_decode_handler(request.META["HTTP_AUTHORIZATION"].split()[1])["user_id"]).get_username()):
                accept = []
                fail = []
                for i in request.data:
                    if(panel_id == i["panel_id"] and panel_year_code == i["panel_year_code"]):
                        p_id = Panel.objects.filter(
                            panel_id=panel_id, panel_year_code=panel_year_code).first().id
                        if FacultyPanel.objects.filter(fac_id=user, id=p_id).first().is_coordinator == True:
                            td = Team.objects.filter(
                                team_id=i["team_id"], team_year_code=i["team_year_code"]).first().id
                            if TeamFacultyReview.objects.filter(team_id=td, fac_id=i["fac_id"]).first().exists():
                                if Team.filter(team_year_code=i["team_year_code"], team_id=i["team_id"]).first().guide.fac_id == i["fac_id"]:
                                    row = TeamFacultyReview.objects.filter(
                                        team_id=td, fac_id=i["fac_id"]).first()
                                    accept.append(row)
                                else:
                                    fail.append(
                                        {"value": i, "detail": "cant remove guide mofo"})
                            else:
                                fail.append({"value": i})
                        else:
                            return Response({"detail": "you aint a coord for thiss panel bruv"}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response({"detail": "he aint in this panel dude"}, status=status.HTTP_400_BAD_REQUEST)
                if fail == []:
                    for i in accept:
                        if i.is_valid:
                            i.delete()
                            if i["review_number"].value == 1:
                                team_pk = Team.objects.filter(
                                    team_year_code=i["team_year_code"].value, team_id=i["team_id"].value).first().id
                                students = Student.objects.filter(
                                    team_id=team_pk)
                                for studs in students:
                                    Review1(id=str(
                                        studs.srn)+'_'+i["fac_id"].value+'_'+str(i["review_number"].value)).delete()
                            elif i["review_number"].value == 2:
                                team_pk = Team.objects.filter(
                                    team_year_code=i["team_year_code"].value, team_id=i["team_id"].value).first().id
                                students = Student.objects.filter(
                                    team_id=team_pk)
                                for studs in students:
                                    Review2(id=str(
                                        studs.srn)+'_'+i["fac_id"].value+'_'+str(i["review_number"].value)).delete()
                            elif i["review_number"].value == 3:
                                team_pk = Team.objects.filter(
                                    team_year_code=i["team_year_code"].value, team_id=i["team_id"].value).first().id
                                students = Student.objects.filter(
                                    team_id=team_pk)
                                for studs in students:
                                    Review3(d=str(
                                        studs.srn)+'_'+i["fac_id"].value+'_'+str(i["review_number"].value)).delete()
                            elif i["review_number"].value == 4:
                                team_pk = Team.objects.filter(
                                    team_year_code=i["team_year_code"].value, team_id=i["team_id"].value).first().id
                                students = Student.objects.filter(
                                    team_id=team_pk)
                                for studs in students:
                                    Review4(id=str(
                                        studs.srn)+'_'+i["fac_id"].value+'_'+str(i["review_number"].value)).delete()
                            elif i["review_number"].value == 5:
                                team_pk = Team.objects.filter(
                                    team_year_code=i["team_year_code"].value, team_id=i["team_id"].value).first().id
                                students = Student.objects.filter(
                                    team_id=team_pk)
                                for studs in students:
                                    Review5(id=str(
                                        studs.srn)+'_'+i["fac_id"].value+'_'+str(i["review_number"].value)).delete()
                else:
                    return Response(fail, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"detail": "Identify youself"}, status=status.HTTP_401_UNAUTHORIZED)

        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class Team_Student_CSV(APIView):

    parser_classes = [JSONParser]

    def post(self, request, user):
        # try:
        if(user == User.objects.get(id=jwt_decode_handler(request.META["HTTP_AUTHORIZATION"].split()[1])["user_id"]).get_username()):
            response_list = []
            null_set_list = []
            for i in request.data:
                if("panel_id" in i and i["panel_id"] != None and "panel_year_code" in i and i["panel_year_code"] != None):
                    p = Panel.objects.filter(
                        panel_id=i["panel_id"], panel_year_code=i["panel_year_code"], is_active=True)
                    i.pop("panel_year_code")
                    if(p.exists() and "guide" in i and FacultyPanel.objects.filter(fac_id=i["guide"], panel_id=p.first().id).exists()):
                        i["panel_id"] = p.first().id
                    else:
                        i["panel_id"] = None
                        null_set_list.append(
                            {"value": i, "detail": "panel set to NULL,either panel does not or guide does not exist in panel"})
                else:
                    i.pop("panel_year_code")
                    i["panel_id"] = None
                    null_set_list.append(
                        {"value": i, "detail": "panel set to NULL,either panel does not or guide does not exist in panel"})
                team_data = {"name": i["team_name"], "description": i["description"],
                             "guide": i["guide"], "panel_id": i["panel_id"], "team_id": add_one_team(i["team_year_code"]), "team_year_code": i["team_year_code"]}
                team_serial = Team_Serializer(data=team_data)
                if team_serial.is_valid():
                    team_serial.save()
                    t = Team.objects.filter(
                        team_id=team_data["team_id"], team_year_code=team_data["team_year_code"]).first()
                else:
                    response_list.append(
                        {"value": i, "detail": team_serial.errors})
                if(len(i["srn"]) == len(i["name"]) and len(i["name"]) == len(i["email"]) and len(i["email"]) == len(i["phone"]) and len(i["phone"]) == len(i["dept"])):
                    student_data = [{"srn": i["srn"][j], "name":i["name"][j], "email":i["email"][j],
                                     "phone":i["phone"][j], "dept":i["dept"][j], "team_id":t.id} for j in range(len(i["srn"]))]
                    for k in student_data:
                        student_serial = Student_Serializer(data=k)
                        if student_serial.is_valid():
                            student_serial.save()
                        else:
                            response_list.append(
                                {"value": i, "detail": student_serial.errors})
                else:
                    response_list.append(
                        {"values": i, "detail": "mismatch data"})
            if(response_list == []):
                return Response({"detail": "insert successful"}, status=status.HTTP_201_CREATED)
            else:
                response_list.extend(null_set_list)
                return Response(response_list, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
        # except:
        #     return Response(response_list, status=status.HTTP_400_BAD_REQUEST)

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


class EvaluatorMarksView:

    parser_classes = [JSONParser]

    def get(self, request, user, panel_id=None, panel_year_code=None, team_id=None, team_year_code=None, review_number=None):
        try:
            if(user == User.objects.get(id=jwt_decode_handler(request.META["HTTP_AUTHORIZATION"].split()[1])["user_id"]).get_username()):
                t = Team.objects.filter(
                    team_id=team_id, team_year_code=team_year_code)
                t_serial = list(t.values())[0]
                t_serial.pop(id)
                res = {"team": t_serial}
                if(TeamFacultyReview.objects.filter(team_id=t.first().id, fac_id=user, review_nember=review_number).exists()):
                    tfr = TeamFacultyReview.objects.filter(
                        team_id=t.first().id, fac_id=user, review_nember=review_number).first()
                    res = res.update({"team_remarks": tfr.remarks})
                    s = Student.objects.filter(team_id=t).order_by("srn")
                    if(review_number == 1):
                        r = list(Review1.objects.filter(
                            srn__in=s, fac_id=user).order_by("srn").values())
                    elif(review_number == 2):
                        r = list(Review2.objects.filter(
                            srn__in=s, fac_id=user).order_by("srn").values())
                    elif(review_number == 3):
                        r = list(Review3.objects.filter(
                            srn__in=s, fac_id=user).order_by("srn").values())
                    elif(review_number == 4):
                        r = list(Review4.objects.filter(
                            srn__in=s, fac_id=user).order_by("srn").values())
                    elif(review_number == 5):
                        r = list(Review5.objects.filter(
                            srn__in=s, fac_id=user).order_by("srn").values())
                    for i in r:
                        student = Student.objects.get(srn=i["srn"])
                        i["name"] = student.name
                        i["email"] = student.email
                        i["phone"] = student.phone
                    res = res.update({"individual_review": r})
                return Response(res, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, user, panel_id=None, panel_year_code=None, team_id=None, team_year_code=None, review_number=None):

        try:
            if(user == User.objects.get(id=jwt_decode_handler(request.META["HTTP_AUTHORIZATION"].split()[1])["user_id"]).get_username()):

                t = Team.objects.filter(
                    team_id=team_id, team_year_code=team_year_code).first()
                if(TeamFacultyReview(fac_id=user, team_id=t, review_number=review_number)):
                    response_list = []
                    valid_list = []
                    Remark = request.data.pop('remark')
                    for i in request.data["individual_review"]:
                        i.pop("email")
                        i.pop("name")
                        i.pop("phone")
                        if (review_number == 1):
                            serial = Review1_Serializer(Review1.objects.filter(
                                srn=i["srn"], fac_id=user).first(), data=i)
                        elif (review_number == 2):
                            serial = Review2_Serializer(Review2.objects.filter(
                                srn=i["srn"], fac_id=user).first(), data=i)
                        elif (review_number == 3):
                            serial = Review3_Serializer(Review3.objects.filter(
                                srn=i["srn"], fac_id=user).first(), data=i)
                        elif (review_number == 4):
                            serial = Review4_Serializer(Review4.objects.filter(
                                srn=i["srn"], fac_id=user).first(), data=i)
                        elif (review_number == 5):
                            serial = Review5_Serializer(Review5.objects.filter(
                                srn=i["srn"], fac_id=user).first(), data=i)

                        if not serial.is_valid():
                            response_list.append(
                                {"value": i, "detail": serial.errors})
                        else:
                            valid_list.append(serial)

                    if(response_list == []):

                        tfr = TeamFacultyReview.objects.filter(
                            team_id=t, fac_id=user, review_number=review_number).first()
                        tfr.remark = Remark
                        tfr.save()
                        for i in valid_list:
                            i.save()
                        return Response({"detail": "update successful"}, status=status.HTTP_202_ACCEPTED)
                    else:
                        return Response(response_list, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"details": "invalid team or review_number"}, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({"details": "invalid token"}, status=status.HTTP_403_FORBIDDEN)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class GeneralMarksView(APIView):

    parser_classes = [JSONParser]

    def get(self, request, user):
        try:
            if(user == User.objects.get(id=jwt_decode_handler(request.META["HTTP_AUTHORIZATION"].split()[1])["user_id"]).get_username()):
                if(Faculty.objects.get(fac_id=user).is_admin == True):
                    if "srn" in request.GET and len(request.GET["srn"]) > 7:
                        student_as_object = Student.objects.filter(
                            srn__startswith=request.GET["srn"]).order_by("-srn")
                    else:
                        return Response({"detail": "provide more detailed srn, too heavy for server"}, status=status.HTTP_400_BAD_REQUEST)
                    content = list(student_as_object.values())
                    for i in content:
                        i.pop("phone")
                        i.pop("email")
                        i["review"] = {}
                        if i["team_id_id"] != None:
                            t = Team.objects.get(id=i.pop("team_id_id"))
                            i["team_id"] = t.team_id
                            i["team_year_code"] = t.team_year_code
                            r1 = Review1.objects.filter(srn=i["srn"])
                            r2 = Review2.objects.filter(srn=i["srn"])
                            r3 = Review3.objects.filter(srn=i["srn"])
                            r4 = Review4.objects.filter(srn=i["srn"])
                            r5 = Review5.objects.filter(srn=i["srn"])
                            if r1.exists():
                                i["review"] = i["review"].update(
                                    {"1": Review1_Serializer(r1.first())})
                            if r2.exists():
                                i["review"] = i["review"].update(
                                    {"2": Review2_Serializer(r2.first())})
                            if r3.exists():
                                i["review"] = i["review"].update(
                                    {"3": Review3_Serializer(r3.first())})
                            if r4.exists():
                                i["review"] = i["review"].update(
                                    {"4": Review4_Serializer(r4.first())})
                            if r5.exists():
                                i["review"] = i["review"].update(
                                    {"5": Review5_Serializer(r5.first())})
                        else:
                            i.pop("team_id_id")
                            i["team_id"] = None
                            i["team_year_code"] = None
                    return Response(content, status=status.HTTP_200_OK)
                else:
                    return Response(status=status.HTTP_403_FORBIDDEN)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
