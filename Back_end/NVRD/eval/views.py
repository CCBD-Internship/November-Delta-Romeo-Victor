from django.views.decorators.csrf import ensure_csrf_cookie
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
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import FileResponse
from .models import *
from .serializers import *
from django.core.files.base import ContentFile
from django.core.mail import send_mail, send_mass_mail
import json
import datetime
from NVRD.settings import SIMPLE_JWT, BASE_DIR, EMAIL_HOST_USER
import jwt
import csv
import hashlib
from PIL import Image
import base64
import io
import os
# Create your views here.

# from django_cron import CronJobBase, Schedule

# class MyCronJob(CronJobBase):
#     RUN_EVERY_MINS = 120 # every 2 hours

#     schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
#     code = 'my_app.my_cron_job'    # a unique code

#     def do(self):
#         pass    # do your thing here


def student_login(request):
    return render(request, 'eval/student_login.html')


@login_required(login_url='')
def home(request, user):
    if request.COOKIES.get('username'):
        args = {}
        fac = Faculty.objects.get(fac_id=user)
        args["is_admin"] = fac.is_admin
        return render(request, "eval/main.html", args)
    else:
        logout(request)
        response = redirect('/')
        return response


@login_required(login_url='')
@ensure_csrf_cookie
def refresh(request, user):
    try:
        if request.method == 'POST':
            token = RefreshToken(request.session["refresh"])
            if(not token.check_exp(claim='exp', current_time=timezone.now()+SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'])):
                response = HttpResponse()
                response.set_cookie('token', str(
                    token.access_token), expires=timezone.now()+datetime.timedelta(days=1), samesite='Lax')
                return response
            else:
                return force_logoutUser(request)
        else:
            return force_logoutUser(request)
    except:
        return force_logoutUser(request)


def force_logoutUser(request):
    logout(request)
    response = HttpResponse(status=308)
    response.delete_cookie('token')
    response.delete_cookie('refresh')
    response.delete_cookie('username')
    return response


@ensure_csrf_cookie
def loginpage(request):
    if request.user.is_authenticated:
        return redirect(str(request.user)+'/home')
    else:
        context = {}
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            if(User.objects.filter(username=request.POST.get("username")).exists()):
                user = User.objects.get(username=username)
                if(user.check_password(password)):
                    token = RefreshToken.for_user(user)
                    login(request, user,
                          backend='django.contrib.auth.backends.ModelBackend')
                    response = redirect('/'+username+'/home')
                    response.set_cookie('token', str(
                        token.access_token), expires=timezone.now()+datetime.timedelta(days=1))
                    request.session["refresh"] = str(token)
                    # response.set_cookie('refresh', str(
                    #     token), expires=timezone.now()+datetime.timedelta(days=100))
                    response.set_cookie(
                        'username', username, expires=timezone.now()+datetime.timedelta(days=100))
                    return response
                else:
                    context["error"] = "invalid user"
                return render(request, 'eval/login.html', context)
        else:
            context["error"] = "invalid user"
        return render(request, 'eval/login.html', context)


def logoutUser(request):
    logout(request)
    response = redirect('/')
    response.delete_cookie('token')
    response.delete_cookie('refresh')
    response.delete_cookie('username')
    return response


@login_required(login_url='')
def coordinator_teamHTML(request, panel_id, panel_year_code, user):
    return render(request, "eval/containers/coordinator_team.html")


@login_required(login_url='')
def coordinator_teamJS(request, panel_id, panel_year_code, user):
    return render(request, "eval/scripts/coordinator_team.js")


@login_required(login_url='')
def coordinator_team_faculty_reviewHTML(request, panel_id, panel_year_code, user):
    return render(request, "eval/containers/coordinator_team_faculty_review.html")


@login_required(login_url='')
def coordinator_team_faculty_reviewJS(request, panel_id, panel_year_code, user):
    return render(request, "eval/scripts/coordinator_team_faculty_review.js")


@login_required(login_url='')
def coordinator_studentHTML(request, panel_id, panel_year_code, user):
    return render(request, "eval/containers/coordinator_student.html")


@login_required(login_url='')
def coordinator_studentJS(request, panel_id, panel_year_code, user):
    return render(request, "eval/scripts/coordinator_student.js")


@login_required(login_url='')
def admin_faculty_panelHTML(request, user):
    return render(request, "eval/containers/admin_faculty_panel.html")


@login_required(login_url='')
def admin_faculty_panelJS(request, user):
    return render(request, "eval/scripts/admin_faculty_panel.js")


@login_required(login_url='')
def admin_facultyHTML(request, user):
    return render(request, "eval/containers/admin_faculty.html")


@login_required(login_url='')
def admin_facultyJS(request, user):
    return render(request, "eval/scripts/admin_faculty.js")


@login_required(login_url='')
@ensure_csrf_cookie
def indexpage(request, user):
    return render(request, "eval/main.html")


@login_required(login_url='')
@ensure_csrf_cookie
def indexJS(request, user):
    return render(request, "eval/scripts/main.js")


@login_required(login_url='')
@ensure_csrf_cookie
def admin_studentHTML(request, user):
    return render(request, "eval/containers/admin_student.html")


@login_required(login_url='')
@ensure_csrf_cookie
def admin_studentJS(request, user):
    return render(request, "eval/scripts/admin_student.js")


@login_required(login_url='')
@ensure_csrf_cookie
def admin_student_portalHTML(request, user):
    return render(request, "eval/containers/admin_student_portal.html")


@login_required(login_url='')
@ensure_csrf_cookie
def admin_student_portalJS(request, user):
    return render(request, "eval/scripts/admin_student_portal.js")


@login_required(login_url='')
@ensure_csrf_cookie
def admin_panelHTML(request, user):
    return render(request, "eval/containers/admin_panel.html")


@login_required(login_url='')
@ensure_csrf_cookie
def admin_panelJS(request, user):
    return render(request, "eval/scripts/admin_panel.js")


@login_required(login_url='')
@ensure_csrf_cookie
def admin_teamHTML(request, user):
    return render(request, "eval/containers/admin_team.html")


@login_required(login_url='')
@ensure_csrf_cookie
def admin_teamJS(request, user):
    return render(request, "eval/scripts/admin_team.js")


@login_required(login_url='')
@ensure_csrf_cookie
def admin_marks_viewHTML(request, user):
    return render(request, "eval/containers/admin_marks_view.html")


@login_required(login_url='')
@ensure_csrf_cookie
def admin_marks_viewJS(request, user):
    return render(request, "eval/scripts/admin_marks_view.js")


@login_required(login_url='')
def coordinator_panel_reviewHTML(request, panel_id, panel_year_code, user):
    return render(request, "eval/containers/coordinator_panel_review.html")


@login_required(login_url='')
def coordinator_panel_reviewJS(request, panel_id, panel_year_code, user):
    return render(request, "eval/scripts/coordinator_panel_review.js")


@login_required(login_url='')
@ensure_csrf_cookie
def evaluator_teamHTML(request, panel_id, panel_year_code, user, review_number=None):
    return render(request, "eval/containers/evaluator_team.html")


@login_required(login_url='')
@ensure_csrf_cookie
def evaluator_teamJS(request, panel_id, panel_year_code, user, review_number=None):
    return render(request, "eval/scripts/evaluator_team.js")


@login_required(login_url='')
@ensure_csrf_cookie
def evaluator_studentHTML(request, panel_id, panel_year_code, user, review_number=None):
    return render(request, "eval/containers/evaluator_student.html")


@login_required(login_url='')
@ensure_csrf_cookie
def evaluator_studentJS(request, panel_id, panel_year_code, user, review_number=None):
    return render(request, "eval/scripts/evaluator_student.js")


@login_required(login_url='')
@ensure_csrf_cookie
def coordinator_facpanelHTML(request, panel_id, panel_year_code, user):
    return render(request, "eval/containers/coordinator_faculty_panel.html")


@login_required(login_url='')
@ensure_csrf_cookie
def evaluator_facpanelHTML(request, panel_id, panel_year_code, user):
    return render(request, "eval/containers/evaluator_faculty_panel.html")


@login_required(login_url='')
@ensure_csrf_cookie
def coordinator_facpanelJS(request, panel_id, panel_year_code, user):
    return render(request, "eval/scripts/coordinator_faculty_panel.js")


@login_required(login_url='')
@ensure_csrf_cookie
def evaluator_evaluationsHTML(request, panel_id, panel_year_code, user, review_number):
    return render(request, "eval/containers/evaluator_evaluations.html")


@login_required(login_url='')
@ensure_csrf_cookie
def evaluator_evaluationsJS(request, panel_id, panel_year_code, user, review_number):
    return render(request, "eval/scripts/evaluator_evaluations.js")


@login_required(login_url='')
@ensure_csrf_cookie
def evaluator_facpanelJS(request, panel_id, panel_year_code, user):
    return render(request, "eval/scripts/evaluator_faculty_panel.js")


def add_one_panel(panel_year_code, serializer_list=None):
    if serializer_list and serializer_list != []:
        for i in serializer_list[::-1]:
            if(i.validated_data["panel_year_code"] == panel_year_code):
                return str(int(i.validated_data["panel_id"]) + 1).zfill(10)
    largest = Panel.objects.filter(
        panel_year_code=panel_year_code).order_by('panel_id').last()
    if not largest:
        return str(1).zfill(10)
    return str(int(largest.panel_id) + 1).zfill(10)


def add_one_team(team_year_code, serializer_list=None):
    if serializer_list and serializer_list != []:
        for i in serializer_list[::-1]:
            if(i.validated_data["team_year_code"] == team_year_code):
                return str(int(i.validated_data["team_id"]) + 1).zfill(10)
    largest = Team.objects.filter(
        team_year_code=team_year_code).order_by('team_id').last()
    if not largest:
        return str(1).zfill(10)
    return str(int(largest.team_id) + 1).zfill(10)


def compute_total_download(d):
    marks_scored = 0
    total_marks = 0
    for i in d:
        marks_scored += i["marks_scored"]
        total_marks += i["total_marks"]
    return [marks_scored, round(marks_scored/total_marks*100, 2)]


def individual_review_dict_download(l, rno):
    marks_scored = 0
    c = 0
    for i in l:
        if i["is_evaluated"]:
            c += 1
            for j in i:
                if type(i[j]) == int:
                    marks_scored += i[j]
    total_marks = 40
    if (rno == 3):
        total_marks = 35
    if(c):
        avg = marks_scored/c
    else:
        avg = 0
    return avg


def password_generate(user):
    my_hash = (hashlib.sha256(user.encode()).hexdigest())
    return str(hex(int(my_hash, 16)+int(hashlib.sha256("NVRD_69420_Your_Choice_!!!".encode()).hexdigest(), 16)))[-16:-1]


def password_match(user, p):
    return(password_generate(user) == p)


def student_logout(request):
    logout(request)
    response = redirect('/my_student_login/')
    return response


def student_validate(request):
    try:
        if(request.method == 'POST'):
            stuff = json.loads(request.body.decode('UTF-8'))
            if(Student.objects.filter(srn=stuff["username"]).exists() and Student.objects.filter(srn=stuff["username"]).first().team_id):
                student_portal = Open_Close.objects.get(
                    oc_type="student_portal")
                if(timezone.now() >= student_portal.open_time and timezone.now() <= student_portal.close_time):
                    if(password_match(stuff["username"], stuff["password"])):
                        response = HttpResponse()
                        request.session["SRN"] = stuff["username"]
                        request.session["password"] = stuff["password"]
                        request.session.set_expiry(60*60)
                        return response
                    else:
                        return HttpResponse("incorrect SRN or password", status=403)
                else:
                    return HttpResponse("Portal Not Open", status=403)
            else:
                return HttpResponse("Invalid", status=404)
        return HttpResponse("Invalid", status=403)
    except:
        return HttpResponse("Invalid", status=404)


def student_page(request):
    return render(request, "eval/student_page.html")


def get_image_name(imgname):
    # imgname = 'whatever.xyz'
    fullname = os.path.join(BASE_DIR+'/eval/student_images/', imgname)
    if os.path.exists(fullname):
        os.remove(fullname)
    return imgname


class my_student(APIView):

    parser_classes = [JSONParser]
    permission_classes = (AllowAny,)

    def get(self, request):
        try:
            c = True  # check if open
            if(Student.objects.filter(srn=request.session["SRN"]).exists() and Student.objects.filter(srn=request.session["SRN"]).first().team_id):
                student_portal = Open_Close.objects.get(
                    oc_type="student_portal")
                if(timezone.now() >= student_portal.open_time and timezone.now() <= student_portal.close_time):
                    if(password_match(request.session["SRN"], request.session["password"])):
                        a = Student.objects.filter(
                            srn=request.session["SRN"]).first()
                        team_details = Team_Serializer(Student.objects.filter(
                            srn=request.session["SRN"]).first().team_id).data
                        f = Faculty.objects.get(fac_id=team_details["guide"])
                        team_details["guide_name"] = f.name
                        team_details["guide_designation"] = f.fac_type
                        student_details = Student_Serializer(
                            Student.objects.filter(srn=request.session["SRN"]).first())
                        my_comments = {1: [], 2: [], 3: [], 4: [], 5: []}
                        myp = Profile_Photo.objects.get(
                            srn=request.session["SRN"])
                        aaa = (base64.b64encode(myp.image.read()))
                        for x, y in zip([Review1, Review2, Review3, Review4, Review5], range(1, 6)):
                            for j in x.objects.filter(srn=a):
                                if j.is_evaluated:
                                    my_comments[y].append({"designation": j.fac_id.fac_type, "fac_name": j.fac_id.name,
                                                           "comments": j.public_comments, "is_guide": team_details["guide"] == j.fac_id.fac_id})
                        data = {"srn": request.session["SRN"], "team": team_details,
                                "student": student_details.data, "comments": my_comments, "photo": aaa}
                        return Response(data, status=status.HTTP_200_OK)
                    else:
                        return Response({"detail": "incorrect SRN or password"}, status=status.HTTP_403_FORBIDDEN)
                else:
                    return Response({"detail": "Portal Not Open"}, status=status.HTTP_403_FORBIDDEN)
            return Response(status=status.HTTP_403_FORBIDDEN)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        try:
            if(Student.objects.filter(srn=request.session["SRN"]).exists() and Student.objects.filter(srn=request.session["SRN"]).first().team_id):
                student_portal = Open_Close.objects.get(
                    oc_type="student_portal")
                if(timezone.now() >= student_portal.open_time and timezone.now() <= student_portal.close_time):
                    if(password_match(request.session["SRN"], request.session["password"])):
                        if(request.data["type"] == "description"):
                            t = Student.objects.get(
                                srn=request.session["SRN"]).team_id
                            t.description = request.data["description"]
                            t.save()
                            return Response({"description": t.description}, status=status.HTTP_200_OK)
                        elif(request.data["type"] == "photo"):
                            msg = request.data["description"].split(',')[-1]
                            msg = base64.b64decode(msg)
                            a = Profile_Photo.objects.get(
                                srn=Student.objects.get(srn=request.session["SRN"]))
                            fname = get_image_name(
                                request.session["SRN"]+".jpg")
                            a.image.save(fname, ContentFile(msg))
                            a.save()
                            return Response(status=status.HTTP_200_OK)
                    else:
                        return Response({"detail": "incorrect SRN or password"}, status=status.HTTP_403_FORBIDDEN)
                else:
                    return Response({"detail": "Portal Not Open"}, status=status.HTTP_403_FORBIDDEN)
            return Response(status=status.HTTP_403_FORBIDDEN)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


def Photo_upload(request):
    if request.method == 'PUT':
        return HttpResponse(status=200)
    if request.method == 'GET':
        pass


class File_List(APIView):

    parser_classes = [JSONParser]
    permission_classes = (AllowAny,)

    def post(self, request, user):
        try:
            if(user == User.objects.get(id=jwt_decode_handler(request.META["HTTP_AUTHORIZATION"].split()[1])["user_id"]).get_username()):
                if(Faculty.objects.get(fac_id=user).is_admin == True):
                    response = HttpResponse(content_type='text/csv')
                    response['Content-Disposition'] = 'attachment; filename="results.csv"'
                    writer = csv.writer(response)
                    writer.writerow(['SRN', 'Name', 'Review 1(40)', 'Review 2(40)',
                                     'Review 3(35)', 'Review 4(40)', 'Review 5(40)', 'Total(195)', 'Percentage'])
                    # based on srns in a list in request
                    # request contains a list of srns
                    for srns in request.data:
                        i = Student.objects.filter(srn=srns).first()
                        if i.team_id != None:
                            r1 = Review1.objects.filter(srn=i.srn)
                            r2 = Review2.objects.filter(srn=i.srn)
                            r3 = Review3.objects.filter(srn=i.srn)
                            r4 = Review4.objects.filter(srn=i.srn)
                            r5 = Review5.objects.filter(srn=i.srn)
                            marks = [individual_review_dict(x, y) for x, y in zip(
                                [r1.values(), r2.values(), r3.values(), r4.values(), r5.values()], [1, 2, 3, 4, 5])]
                            mark1 = [individual_review_dict_download(x, y) for x, y in zip(
                                [r1.values(), r2.values(), r3.values(), r4.values(), r5.values()], [1, 2, 3, 4, 5])]
                            writer.writerow(
                                [i.srn, i.name, *mark1, *compute_total_download(marks)])

                    return response
                else:
                    return Response({"detail": "User is not an Admin"}, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


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
                faculty_as_object = Faculty.objects.filter().order_by("fac_id")
                if "active" in request.GET:
                    faculty_as_object = faculty_as_object.filter(
                        is_active=request.GET['active'])
                else:
                    faculty_as_object = faculty_as_object.filter(
                        is_active=True)
                if "fac_id" in request.GET:
                    faculty_as_object = faculty_as_object.filter(
                        fac_id__contains=request.GET['fac_id'])
                if "fac_name" in request.GET:
                    faculty_as_object = faculty_as_object.filter(
                        name__contains=request.GET['fac_name'])
                if 'inactive' in request.GET:
                    active_panels = Panel.objects.filter(is_active=True)
                    active_faculty = FacultyPanel.objects.filter(
                        panel_id__in=active_panels)
                    included_facs = [i.fac_id.fac_id for i in active_faculty]
                    faculty_as_object = faculty_as_object.exclude(
                        fac_id__in=included_facs)
                content = list(faculty_as_object.values())
                for i in content:
                    i["dept"] = i.pop("dept_id")
                    i.pop("mynotes")
                return Response(content)
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
                                send_mail('PES Evaluation System ACCOUNT CREATED', 'Dear '+i["name"].value+',\n\nYour PES Evaluation System faculty account has been created\nUsername: ' +
                                          i["fac_id"].value+'\nPassword: '+i["fac_id"].value+'\nYour password is currently your username, so please change your password the next time you login', EMAIL_HOST_USER, [i["email"].value])
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
                            f = Faculty.objects.filter(
                                fac_id=i.get("fac_id")).first()
                            serial = Faculty_Serializer(
                                f, data=i, partial=True)
                            # if "email" in i:
                            #     u = User.objects.get(id=user)
                            #     u.set_email(i["email"])
                            #     u.save()
                            if not serial.is_valid():
                                response_list.append(
                                    {"value": i, "detail": serial.errors})
                            else:
                                valid_list.append(serial)
                        else:
                            response_list.append(
                                {"value": i, "detail": "faculty does not exist"})
                    if(response_list == []):
                        for i, j in zip(valid_list, request.data):
                            f = Faculty.objects.filter(
                                fac_id=j.get("fac_id")).first()
                            if("is_active" in j and Faculty.objects.get(fac_id=j["fac_id"]).is_active == True and j["is_active"] == False):
                                teams_under = Team.objects.filter(guide=f)
                                facpan = FacultyPanel.objects.filter(
                                    fac_id=f, panel_id__in=Panel.objects.filter(is_active=True))
                                for fp in facpan:
                                    fp.delete()
                                for tm in teams_under:
                                    if(tm.panel_id == None or tm.panel_id.is_active == True):
                                        tm.guide = None
                                        tm.panel_id = None
                                        tm.save()
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
                            fac_id__contains=request.GET['fac_id'])
                    if 'panel_year_code' in request.GET:
                        facultypanel_as_object = facultypanel_as_object.filter(
                            panel_id__in=Panel.objects.filter(panel_year_code=request.GET['panel_year_code']))
                    if 'panel_id' in request.GET:
                        facultypanel_as_object = facultypanel_as_object.filter(
                            panel_id__in=Panel.objects.filter(panel_id=request.GET['panel_id']))
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
                            fac_id__contains=request.GET['fac_id'])
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
                            if(Panel.objects.filter(panel_year_code=i["panel_year_code"], panel_id=i["panel_id"], is_active=True).exists()):
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
                                t.panel_id = Panel.objects.get(
                                    id=i["panel_id"].value)
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
                            if(Panel.objects.filter(panel_year_code=i["panel_year_code"], panel_id=i["panel_id"], is_active=True).exists()):
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
                                serial = FacultyPanel_Serializer(
                                    f, data=d, partial=True)
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
                            teams = Team.objects.filter(
                                panel_id=p, guide=Faculty.objects.get(fac_id=i["fac_id"]))
                            for t in teams:
                                t.panel_id = None
                                t.save()
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
                        panel_as_object = Panel.objects.all().order_by("-panel_year_code", "panel_id")
                    else:
                        panel_as_object = Panel.objects.filter(
                            panel_id=panel_id, panel_year_code=panel_year_code).order_by("-ctime")
                    if 'active' in request.GET:
                        panel_as_object = panel_as_object.filter(
                            is_active=request.GET['active'])
                    if("panel_year_code" in request.GET):
                        panel_as_object = panel_as_object.filter(
                            panel_year_code__contains=request.GET["panel_year_code"])
                    if("panel_id" in request.GET):
                        panel_as_object = panel_as_object.filter(
                            panel_id__endswith=request.GET["panel_id"])
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
                        i["panel_id"] = add_one_panel(
                            i["panel_year_code"], serial_list)
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
                                # PanelReview(review_number=k, panel_id=p, open_time=timezone.now(), close_time=timezone.make_aware(datetime.datetime.now(
                                # )+datetime.timedelta(days=365), timezone.get_default_timezone()), id=i["panel_year_code"].value+'_'+i["panel_id"].value+'_'+str(k)).save()
                                PanelReview(review_number=k, panel_id=p, open_time=p.ctime, close_time=p.ctime,
                                            id=i["panel_year_code"].value+'_'+i["panel_id"].value+'_'+str(k)).save()
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
                if(FacultyPanel.objects.filter(fac_id=user, panel_id=p.id).exists()):
                    PanelReview_as_object = PanelReview.objects.filter(
                        panel_id=p).order_by("review_number")
                    content = list(PanelReview_as_object.values())
                    for i in content:
                        i.pop("panel_id_id")
                        i.pop("id")
                        i["panel_id"] = panel_id
                        i["panel_year_code"] = panel_year_code
                    return Response(content, status=status.HTTP_200_OK)
                else:
                    return Response({"detail": "only panel member can access"}, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, user, panel_year_code, panel_id):
        try:
            p_id = Panel.objects.filter(
                panel_id=panel_id, panel_year_code=panel_year_code).first().id
            c2 = FacultyPanel.objects.filter(
                fac_id=user, panel_id=p_id).first().is_coordinator
            if(user == User.objects.get(id=jwt_decode_handler(request.META["HTTP_AUTHORIZATION"].split()[1])["user_id"]).get_username() and c2 == True):
                valid_list = []
                response_list = []
                for i in request.data:
                    if(panel_id == i["panel_id"] and panel_year_code == i["panel_year_code"]):
                        i["panel_id"] = p_id
                        serial = PanelReview_Serializer(PanelReview.objects.filter(panel_id=i["panel_id"],
                                                                                   review_number=i["review_number"]).first(), data=i, partial=True)
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
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


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
                        srn__contains=request.GET['srn'])
                if 'name' in request.GET:
                    student_as_object = student_as_object.filter(
                        name__contains=request.GET['name'])
                if 'team_id' in request.GET:
                    team_idl = Team.objects.filter(
                        team_id__endswith=request.GET['team_id'])
                    student_as_object = student_as_object.filter(
                        team_id__in=[i.id for i in team_idl])
                if 'team_year_code' in request.GET:
                    team_year_codel = Team.objects.filter(
                        team_year_code__contains=request.GET['team_year_code'])
                    student_as_object = student_as_object.filter(
                        team_id__in=[i.id for i in team_year_codel])
                if 'guide' in request.GET:
                    team_guidel = Team.objects.filter(
                        guide__in=Faculty.objects.filter(fac_id__contains=request.GET['guide']))
                    student_as_object = student_as_object.filter(
                        team_id__in=[i.id for i in team_guidel])
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
                    null_set_list = []
                    for i in request.data:
                        if("team_id" in i and i["team_id"] != None and "team_year_code" in i and i["team_year_code"] != None):
                            t = Team.objects.filter(
                                team_id=i["team_id"], team_year_code=i["team_year_code"])
                            i.pop("team_year_code")
                            if(t.exists()):
                                i["team_id"] = t.first().id
                            else:
                                i["team_id"] = None
                                null_set_list.append(
                                    {"value": i, "detail": "team set null as it is not valid"})
                        else:
                            i["team_id"] = None
                            null_set_list.append(
                                {"value": i, "detail": "team set null as it is not valid"})
                        serial = Student_Serializer(data=i)
                        if not serial.is_valid():
                            response_list.append(
                                {"value": i, "detail": serial.errors})
                        else:
                            serial_list.append(serial)
                    if(response_list == []):
                        for i in serial_list:
                            i.save()
                            a = Profile_Photo(srn=Student.objects.get(
                                srn=i.validated_data['srn']))
                            a.save()
                        return Response({"detail": "insert successful", "assumption": null_set_list}, status=status.HTTP_201_CREATED)
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
                        if("team_id" in i and i["team_id"] != None and "team_year_code" in i and i["team_year_code"] != None):
                            t = Team.objects.filter(
                                team_id=i["team_id"], team_year_code=i["team_year_code"])
                            i.pop("team_year_code")
                            if(t.exists()):
                                i["team_id"] = t.first().id
                            else:
                                i["team_id"] = None
                                null_set_list.append(
                                    {"value": i, "detail": "team set null as it is not valid"})
                        else:
                            i["team_id"] = None
                            null_set_list.append(
                                {"value": i, "detail": "team set null as it is not valid"})
                        if(Student.objects.filter(srn=i["srn"]).exists()):
                            serial = Student_Serializer(Student.objects.get(
                                srn=i["srn"]), data=i, partial=True)
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
                        return Response({"detail": "update successful", "assumption": null_set_list}, status=status.HTTP_202_ACCEPTED)
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
                        if("team_id" in i and i["team_id"] != None and "team_year_code" in i and i["team_year_code"] != None):
                            t = Team.objects.filter(
                                team_id=i["team_id"], team_year_code=i["team_year_code"])
                            i.pop("team_year_code")
                            if(t.exists()):
                                i["team_id"] = t.first().id
                            else:
                                i["team_id"] = None
                        else:
                            i["team_id"] = None
                        if(Student.objects.filter(srn=i["srn"]).exists()):
                            serial = Student_Serializer(Student.objects.get(
                                srn=i["srn"]), data=i, partial=True)
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
                            panel_id__in=Panel.objects.filter(panel_year_code__contains=request.GET['panel_year_code']))
                    if 'panel_id' in request.GET:
                        team_as_object = team_as_object.filter(
                            panel_id__in=Panel.objects.filter(panel_id__endswith=request.GET['panel_id']))
                elif(FacultyPanel.objects.filter(fac_id=user, panel_id=Panel.objects.filter(panel_year_code=panel_year_code, panel_id=panel_id).first()).exists()):
                    id = Panel.objects.filter(
                        panel_year_code=panel_year_code, panel_id=panel_id).first().id
                    if(review_number == None):
                        team_as_object = Team.objects.filter(panel_id=id)
                    else:
                        team_as_object = Team.objects.filter(id__in=[i.team_id.id for i in TeamFacultyReview.objects.filter(
                            fac_id=user, review_number=review_number)], panel_id=id)
                else:
                    return Response(status=status.HTTP_403_FORBIDDEN)
                if 'team_id' in request.GET:
                    team_as_object = team_as_object.filter(
                        team_id__endswith=request.GET['team_id'])
                if 'team_year_code' in request.GET:
                    team_as_object = team_as_object.filter(
                        team_year_code__contains=request.GET['team_year_code'])
                if 'team_name' in request.GET:
                    team_as_object = team_as_object.filter(
                        team_name__contains=request.GET['team_name'])
                if 'guide' in request.GET:
                    team_as_object = team_as_object.filter(
                        guide__in=Faculty.objects.filter(fac_id__contains=request.GET['guide']))
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
                        i["team_id"] = add_one_team(
                            i["team_year_code"], serial_list)
                        if("panel_id" in i and "panel_year_code" in i and "guide" in i and i["panel_id"] != None and i["panel_year_code"] != None and FacultyPanel.objects.filter(panel_id__in=Panel.objects.filter(is_active=True, panel_year_code=i["panel_year_code"], panel_id=i["panel_id"]), fac_id=i["guide"]).exists()):
                            p = FacultyPanel.objects.filter(panel_id__in=Panel.objects.filter(
                                is_active=True, panel_year_code=i["panel_year_code"], panel_id=i["panel_id"]), fac_id=i["guide"]).first().panel_id
                            i["panel_id"] = p.id
                        elif("guide" in i and FacultyPanel.objects.filter(panel_id__in=Panel.objects.filter(is_active=True), fac_id=i["guide"]).exists()):
                            p = FacultyPanel.objects.filter(panel_id__in=Panel.objects.filter(
                                is_active=True), fac_id=i["guide"]).order_by("-id").first().panel_id
                            i["panel_id"] = p.id
                        else:
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
                        return Response({"detail": "insert successful", "assumption": null_set_list}, status=status.HTTP_202_ACCEPTED)
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
                        if("panel_id" in i and "panel_year_code" in i and "guide" in i and i["panel_id"] != None and i["panel_year_code"] != None and FacultyPanel.objects.filter(panel_id__in=Panel.objects.filter(is_active=True, panel_year_code=i["panel_year_code"], panel_id=i["panel_id"]), fac_id=i["guide"]).exists()):
                            p = FacultyPanel.objects.filter(panel_id__in=Panel.objects.filter(
                                is_active=True, panel_year_code=i["panel_year_code"], panel_id=i["panel_id"]), fac_id=i["guide"]).first().panel_id
                            i["panel_id"] = p.id
                        elif("guide" in i and FacultyPanel.objects.filter(panel_id__in=Panel.objects.filter(is_active=True), fac_id=i["guide"]).exists()):
                            p = FacultyPanel.objects.filter(panel_id__in=Panel.objects.filter(
                                is_active=True), fac_id=i["guide"]).order_by("-id").first().panel_id
                            i["panel_id"] = p.id
                        else:
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
                        return Response({"detail": "update successful", "assumption": null_set_list}, status=status.HTTP_202_ACCEPTED)
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
                        if("panel_id" in i):
                            i.pop("panel_id")
                        if("panel_year_code" in i):
                            i.pop("panel_year_code")
                        if(Team.objects.filter(team_id=i["team_id"], team_year_code=i["team_year_code"]).exists()):
                            serial = Team_Serializer(Team.objects.filter(
                                team_id=i["team_id"], team_year_code=i["team_year_code"]).first(), data=i, partial=True)
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

    def get(self, request, user, panel_year_code, panel_id):
        try:
            p_id = Panel.objects.get(
                panel_id=panel_id, panel_year_code=panel_year_code).id
            c2 = FacultyPanel.objects.filter(
                fac_id=user, panel_id=p_id).first().is_coordinator
            if(user == User.objects.get(id=jwt_decode_handler(request.META["HTTP_AUTHORIZATION"].split()[1])["user_id"]).get_username() and c2):
                team_info = Team.objects.filter(panel_id__in=Panel.objects.filter(
                    panel_year_code=panel_year_code, panel_id=panel_id))
                if 'team_id' in request.GET:
                    team_info = team_info.filter(
                        team_id=request.GET["team_id"])
                if 'team_year_code' in request.GET:
                    team_info = team_info.filter(
                        team_year_code=request.GET["team_year_code"])
                res = list(TeamFacultyReview.objects.filter(
                    team_id__in=team_info).values())
                for i in res:
                    i["fac_id"] = i.pop("fac_id_id")
                    i.pop('id')
                    t = Team.objects.get(id=i.pop("team_id_id"))
                    i["team_id"] = t.team_id
                    i["team_year_code"] = t.team_year_code
                    fac_d = Faculty.objects.filter(fac_id=i["fac_id"]).first()
                    i["fac_name"] = fac_d.name
                    i["fac_email"] = fac_d.email
                return Response(res, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Only Coordinator has Permission To View This Page"},
                                status=status.HTTP_403_FORBIDDEN)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, user, panel_year_code, panel_id):
        try:
            if(user == User.objects.get(id=jwt_decode_handler(request.META["HTTP_AUTHORIZATION"].split()[1])["user_id"]).get_username()):
                accept = []
                fail = []
                for i in request.data:
                    p_id = Panel.objects.filter(
                        panel_id=panel_id, panel_year_code=panel_year_code).first().id
                    if FacultyPanel.objects.filter(fac_id=user, panel_id=p_id).first().is_coordinator == True:
                        if Team.objects.filter(team_year_code=i["team_year_code"], team_id=i["team_id"], panel_id=p_id).exists():
                            g_fid = Team.objects.filter(
                                team_year_code=i["team_year_code"], team_id=i["team_id"]).first().guide.fac_id
                            t_id = Team.objects.filter(
                                team_year_code=i["team_year_code"], team_id=i["team_id"], panel_id=p_id).first().id
                            if TeamFacultyReview.objects.filter(team_id=t_id, fac_id=g_fid, review_number=i["review_number"]).exists() or g_fid == i["fac_id"]:
                                teach = i["fac_id"]
                                if FacultyPanel.objects.filter(panel_id=p_id, fac_id=teach).exists():
                                    t_id = Team.objects.filter(
                                        team_year_code=i["team_year_code"], team_id=i["team_id"]).first()
                                    row = TeamFacultyReview_Serializer(data={"team_id": t_id.id, "fac_id": teach, "review_number": i["review_number"],
                                                                             "remarks": "Unreviewed", "id": str(i["team_year_code"])+'_'+str(i["team_id"])+'_'+str(teach)+'_'+str(i["review_number"])})
                                    if row.is_valid():
                                        accept.append(row)
                                    else:
                                        fail.append(
                                            {"value": i, "detail": row.errors})
                                else:
                                    fail.append(
                                        {"value": i, "detail": "team is not present in the panel"})
                            else:
                                fail.append(
                                    {"value": i, "detail": "guide is not present in faculty:"+str(g_fid)})
                        else:
                            fail.append(
                                {"value": i, "detail": "team is not present in the panel"})

                    else:
                        fail.append(
                            {"value": i, "detail": "user is not the panel coordinator"})
                if fail == []:
                    for i in accept:
                        if i.is_valid:
                            i.save()
                            f = Faculty.objects.filter(
                                fac_id=i["fac_id"].value).first()
                            if i["review_number"].value == 1:
                                team_pk = i["team_id"].value
                                students = Student.objects.filter(
                                    team_id=team_pk)
                                for studs in students:
                                    Review1(srn=studs, fac_id=f, concept_of_the_work=0, methodology_proposed=0, literature_survey=0, knowledge_on_the_project=0,
                                            public_comments="not yet scored", private_comments="private_comments", id=str(studs.srn)+'_'+i["fac_id"].value+'_'+str(i["review_number"].value)).save()
                            elif i["review_number"].value == 2:
                                team_pk = i["team_id"].value
                                students = Student.objects.filter(
                                    team_id=team_pk)
                                for studs in students:
                                    Review2(srn=studs, fac_id=f, requirements_specification=0, user_interface_use_cases=0, understanding_of_technology_platform_middleware=0, viva_voce=0,
                                            public_comments="not yet scored", private_comments="private_comments", id=str(studs.srn)+'_'+i["fac_id"].value+'_'+str(i["review_number"].value)).save()
                            elif i["review_number"].value == 3:
                                team_pk = i["team_id"].value
                                students = Student.objects.filter(
                                    team_id=team_pk)
                                for studs in students:
                                    Review3(srn=studs, fac_id=f, design_philosophy_methodology=0, user_interface_design_backend_design_and_design_for_any_algorithms=0, suitably_of_design_in_comparison_to_the_technology_proposed=0, progress_of_the_project_work=0, viva_voce=0,
                                            public_comments="not yet scored", private_comments="private_comments", id=str(studs.srn)+'_'+i["fac_id"].value+'_'+str(i["review_number"].value)).save()
                            elif i["review_number"].value == 4:
                                team_pk = i["team_id"].value
                                students = Student.objects.filter(
                                    team_id=team_pk)
                                for studs in students:
                                    Review4(srn=studs, fac_id=f, project_work_results=0, quality_of_demo=0, project_report=0, viva_voce=0,
                                            public_comments="not yet scored", private_comments="private_comments", id=str(studs.srn)+'_'+i["fac_id"].value+'_'+str(i["review_number"].value)).save()
                            elif i["review_number"].value == 5:
                                team_pk = i["team_id"].value
                                students = Student.objects.filter(
                                    team_id=team_pk)
                                for studs in students:
                                    Review5(srn=studs, fac_id=f, project_work_results=0, quality_of_demo=0, project_report=0, viva_voce=0,
                                            public_comments="not yet scored", private_comments="private_comments", id=str(studs.srn)+'_'+i["fac_id"].value+'_'+str(i["review_number"].value)).save()
                    return Response({"detail": "OK"}, status=status.HTTP_200_OK)
                else:
                    return Response(fail, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user, panel_year_code, panel_id):
        try:
            if(user == User.objects.get(id=jwt_decode_handler(request.META["HTTP_AUTHORIZATION"].split()[1])["user_id"]).get_username()):
                accept = []
                fail = []
                for i in request.data:
                    p_id = Panel.objects.filter(
                        panel_id=panel_id, panel_year_code=panel_year_code).first().id
                    if FacultyPanel.objects.filter(fac_id=user, panel_id=p_id).first().is_coordinator == True:
                        if Team.objects.filter(team_year_code=i["team_year_code"], team_id=i["team_id"]).first().guide.fac_id != i["fac_id"]:
                            if Team.objects.filter(team_year_code=i["team_year_code"], team_id=i["team_id"], panel_id=p_id).exists():
                                teach = i["fac_id"]
                                if FacultyPanel.objects.filter(panel_id=p_id, fac_id=teach).exists():
                                    t_id = Team.objects.filter(
                                        team_year_code=i["team_year_code"], team_id=i["team_id"]).first()
                                    row = TeamFacultyReview_Serializer(TeamFacultyReview.objects.filter(team_id=t_id.id, fac_id=teach, review_number=i["review_number"]).first(), data={"team_id": t_id.id, "fac_id": teach, "review_number": i["review_number"],
                                                                                                                                                                                        "id": str(i["team_year_code"])+'_'+str(i["team_id"])+'_'+str(teach)+'_'+str(i["review_number"])})
                                    if row.is_valid():
                                        accept.append(row)
                                    else:
                                        fail.append(
                                            {"value": i, "detail": row.errors})
                                else:
                                    fail.append(
                                        {"value": i, "detail": "team is not present in the panel"})
                            else:
                                fail.append(
                                    {"value": i, "detail": "team is not present in the panel"})
                        else:
                            fail.append(
                                {"value": i, "detail": "cannot delete guide"})
                    else:
                        fail.append(
                            {"value": i, "detail": "user is not the panel coordinator"})
                if fail == []:
                    for i in accept:
                        TeamFacultyReview.objects.filter(
                            team_id=i["team_id"].value, fac_id=i["fac_id"].value, review_number=i["review_number"].value).first().delete()
                        if i["review_number"].value == 1:
                            team_pk = i["team_id"].value
                            students = Student.objects.filter(
                                team_id=team_pk)
                            for studs in students:
                                Review1(id=str(
                                    studs.srn)+'_'+i["fac_id"].value+'_'+str(i["review_number"].value)).delete()
                        elif i["review_number"].value == 2:
                            team_pk = i["team_id"].value
                            students = Student.objects.filter(
                                team_id=team_pk)
                            for studs in students:
                                Review2(id=str(
                                    studs.srn)+'_'+i["fac_id"].value+'_'+str(i["review_number"].value)).delete()
                        elif i["review_number"].value == 3:
                            team_pk = i["team_id"].value
                            students = Student.objects.filter(
                                team_id=team_pk)
                            for studs in students:
                                Review3(d=str(
                                    studs.srn)+'_'+i["fac_id"].value+'_'+str(i["review_number"].value)).delete()
                        elif i["review_number"].value == 4:
                            team_pk = i["team_id"].value
                            students = Student.objects.filter(
                                team_id=team_pk)
                            for studs in students:
                                Review4(id=str(
                                    studs.srn)+'_'+i["fac_id"].value+'_'+str(i["review_number"].value)).delete()
                        elif i["review_number"].value == 5:
                            team_pk = i["team_id"].value
                            students = Student.objects.filter(
                                team_id=team_pk)
                            for studs in students:
                                Review5(id=str(
                                    studs.srn)+'_'+i["fac_id"].value+'_'+str(i["review_number"].value)).delete()
                    return Response({"detail": "OK"}, status=status.HTTP_200_OK)
                else:
                    return Response(fail, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"detail": "Identify youself"}, status=status.HTTP_401_UNAUTHORIZED)

        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class Team_Student_CSV(APIView):

    parser_classes = [JSONParser]

    def post(self, request, user):
        try:
            if(user == User.objects.get(id=jwt_decode_handler(request.META["HTTP_AUTHORIZATION"].split()[1])["user_id"]).get_username()):
                response_list = []
                null_set_list = []
                team_list = []
                correct = []
                for i in request.data:
                    if("panel_id" in i and "panel_year_code" in i and "guide" in i and i["panel_id"] != None and i["panel_year_code"] != None and FacultyPanel.objects.filter(panel_id__in=Panel.objects.filter(is_active=True, panel_year_code=i["panel_year_code"], panel_id=i["panel_id"]), fac_id=i["guide"]).exists()):
                        p = FacultyPanel.objects.filter(panel_id__in=Panel.objects.filter(
                            is_active=True, panel_year_code=i["panel_year_code"], panel_id=i["panel_id"]), fac_id=i["guide"]).first().panel_id
                        i["panel_id"] = p.id
                    elif("guide" in i and FacultyPanel.objects.filter(panel_id__in=Panel.objects.filter(is_active=True), fac_id=i["guide"]).exists()):
                        p = FacultyPanel.objects.filter(panel_id__in=Panel.objects.filter(
                            is_active=True), fac_id=i["guide"]).order_by("-id").first().panel_id
                        i["panel_id"] = p.id
                    else:
                        i["panel_id"] = None
                        null_set_list.append(
                            {"value": [i], "detail": "panel set to NULL,either panel does not or guide does not exist in panel"})
                    team_data = {"team_name": i["team_name"], "description": i["description"],
                                 "guide": i["guide"], "panel_id": i["panel_id"], "team_id": add_one_team(i["team_year_code"]), "team_year_code": i["team_year_code"]}
                    team_list.append(team_data)
                    team_serial = Team_Serializer(data=team_data)
                    dept = i["dept"]
                    t = None
                    if team_serial.is_valid():
                        team_serial.save()
                        t = Team.objects.filter(
                            team_id=team_data["team_id"], team_year_code=team_data["team_year_code"]).first()
                    else:
                        response_list.append(
                            {"value": [i], "detail": team_serial.errors})
                    for k in i["student"]:
                        if(t):
                            k["team_id"] = t.id
                        k["dept"] = dept
                        student_serial = Student_Serializer(data=k)
                        if student_serial.is_valid():
                            correct.append(student_serial)
                        else:
                            response_list.append(
                                {"value": [i, k], "detail": student_serial.errors})
                if(response_list == []):
                    for i in correct:
                        i.save()
                        a = Profile_Photo(srn=Student.objects.get(
                            srn=i.validated_data['srn']))
                        a.save()
                    return Response({"detail": "insert successful", "assumption": null_set_list}, status=status.HTTP_201_CREATED)
                else:
                    response_list.extend(null_set_list)
                    # delete teams
                    for i in team_list:
                        Team.objects.filter(
                            team_year_code=i["team_year_code"], team_id=i["team_id"]).delete()
                    return Response(response_list, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        except:
            return Response(response_list, status=status.HTTP_400_BAD_REQUEST)

# (TokenObtainPairView,TokenRefreshView)


class AboutMe_List(APIView):

    parser_classes = [JSONParser]

    def get(self, request, user):
        try:
            if(user == User.objects.get(id=jwt_decode_handler(request.META["HTTP_AUTHORIZATION"].split()[1])["user_id"]).get_username()):
                fp = FacultyPanel.objects.filter(fac_id=user)
                res = {}
                res["user"] = Faculty.objects.filter(fac_id=user).values()[0]
                l = list(fp.values())
                for i in l:
                    p = Panel.objects.get(id=i.pop("panel_id_id"))
                    i.pop("id")
                    i["is_active"] = p.is_active
                    i["panel_year_code"] = p.panel_year_code
                    i["panel_id"] = p.panel_id
                    i["panel_name"] = p.panel_name
                    i["ctime"] = p.ctime
                l.sort(key=lambda x: x["ctime"], reverse=True)
                res["panels"] = l
                return Response(res, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class TokenBlackList(APIView):

    parser_classes = [JSONParser]
    # permission_classes = [IsAuthenticated]

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


class EvaluatorMarksView(APIView):

    parser_classes = [JSONParser]

    def get(self, request, user, panel_id=None, panel_year_code=None, team_id=None, team_year_code=None, review_number=None):
        try:
            if(user == User.objects.get(id=jwt_decode_handler(request.META["HTTP_AUTHORIZATION"].split()[1])["user_id"]).get_username()):
                t = Team.objects.filter(
                    team_id=team_id, team_year_code=team_year_code)
                t_serial = list(t.values())[0]
                t_serial.pop("id")
                t_serial["guide_id"] = Faculty.objects.get(
                    fac_id=t_serial["guide_id"]).name
                res = {"team": t_serial, "review_number": review_number}
                if(TeamFacultyReview.objects.filter(team_id=t.first().id, fac_id=user, review_number=review_number).exists()):
                    tfr = TeamFacultyReview.objects.filter(
                        team_id=t.first().id, fac_id=user, review_number=review_number).first()
                    res.update({"team_remarks": tfr.remark})
                    s = Student.objects.filter(team_id=t.first())
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
                    photos = {}
                    for i in r:
                        i["srn"] = i.pop("srn_id")
                        i["fac_id"] = i.pop("fac_id_id")
                        i.pop("id")
                        student = Student.objects.get(srn=i["srn"])
                        i["name"] = student.name
                        i["email"] = student.email
                        i["phone"] = student.phone
                        myp = Profile_Photo.objects.get(srn=i["srn"])
                        photos[i["srn"]] = (base64.b64encode(myp.image.read()))
                    res.update({"individual_review": r, "photo": photos})
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
                if TeamFacultyReview.objects.filter(fac_id=Faculty.objects.get(fac_id=user), team_id=t, review_number=review_number).exists():
                    p = PanelReview.objects.filter(panel_id=Panel.objects.filter(
                        panel_year_code=panel_year_code, panel_id=panel_id).first(), review_number=review_number).first()
                    if timezone.now() > p.open_time and timezone.now() < p.close_time:
                        response_list = []
                        valid_list = []
                        Remark = request.data.pop('team_remarks')
                        for i in request.data["individual_review"]:
                            # i.pop("email")
                            # i.pop("name")
                            # i.pop("phone")
                            if (review_number == 1):
                                serial = Review1_Serializer(Review1.objects.filter(
                                    srn=i["srn"], fac_id=user).first(), data=i, partial=True)
                            elif (review_number == 2):
                                serial = Review2_Serializer(Review2.objects.filter(
                                    srn=i["srn"], fac_id=user).first(), data=i, partial=True)
                            elif (review_number == 3):
                                serial = Review3_Serializer(Review3.objects.filter(
                                    srn=i["srn"], fac_id=user).first(), data=i, partial=True)
                            elif (review_number == 4):
                                serial = Review4_Serializer(Review4.objects.filter(
                                    srn=i["srn"], fac_id=user).first(), data=i, partial=True)
                            elif (review_number == 5):
                                serial = Review5_Serializer(Review5.objects.filter(
                                    srn=i["srn"], fac_id=user).first(), data=i, partial=True)

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
                                try:
                                    i.save()
                                except:
                                    response_list.append(
                                        {"detail": "check constraint failed"})
                            if(response_list == []):
                                return Response({"detail": "update successful"}, status=status.HTTP_202_ACCEPTED)
                            else:
                                return Response(response_list, status=status.HTTP_400_BAD_REQUEST)
                        else:
                            return Response(response_list, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response({"detail": "panel not open or panel closed"}, status.HTTP_403_FORBIDDEN)
                else:
                    return Response({"details": "invalid team or review_number"}, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({"details": "invalid token"}, status=status.HTTP_403_FORBIDDEN)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


def individual_review_dict(l, rno, weight):
    marks_scored = 0
    c = 0
    for i in l:
        if i["is_evaluated"]:
            ind_marks = 0
            for j in i:
                if type(i[j]) == int:
                    ind_marks += i[j]
            if(weight != 100 and Student.objects.filter(team_id__in=[j.id for j in Team.objects.filter(guide=i["fac_id_id"])], srn=i["srn_id"]).exists()):
                marks_scored += (ind_marks*weight/100)
                c += (1*weight/100)
            else:
                marks_scored += ind_marks
                c += 1
    total_marks = 40
    if (rno == 3):
        total_marks = 35
    if(c):
        avg = marks_scored/c
    else:
        avg = 0
    return{"marks_scored": avg, "total_marks": total_marks, "percentage": avg/total_marks*100}


def compute_total(d):
    marks_scored = 0
    total_marks = 0
    for i in d["total_individual"]:
        marks_scored += i["marks_scored"]
        total_marks += i["total_marks"]
    return{"marks_scored": marks_scored, "total_marks": total_marks, "percentage": marks_scored/total_marks*100}


class GeneralMarksView(APIView):

    parser_classes = [JSONParser]

    def get(self, request, user):
        try:
            if(user == User.objects.get(id=jwt_decode_handler(request.META["HTTP_AUTHORIZATION"].split()[1])["user_id"]).get_username()):
                if(Faculty.objects.get(fac_id=user).is_admin == True):
                    student_as_object = Student.objects.exclude(
                        team_id=None).order_by("-srn")
                    if "srn" in request.GET:
                        student_as_object = student_as_object.filter(
                            srn__contains=request.GET["srn"])
                    if "name" in request.GET:
                        student_as_object = student_as_object.filter(
                            name__contains=request.GET["name"])
                    if 'team_id' in request.GET:
                        team_idl = Team.objects.filter(
                            team_id__endswith=request.GET['team_id'])
                        student_as_object = student_as_object.filter(
                            team_id__in=[i.id for i in team_idl])
                    if 'team_year_code' in request.GET:
                        team_year_codel = Team.objects.filter(
                            team_year_code__contains=request.GET['team_year_code'])
                        student_as_object = student_as_object.filter(
                            team_id__in=[i.id for i in team_year_codel])
                    if 'guide' in request.GET:
                        team_guidel = Team.objects.filter(
                            guide__in=Faculty.objects.filter(fac_id__contains=request.GET['guide']))
                        student_as_object = student_as_object.filter(
                            team_id__in=[i.id for i in team_guidel])
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
                                i["review"].update(
                                    {"1": r1.values()})
                            if r2.exists():
                                i["review"].update(
                                    {"2": r2.values()})
                            if r3.exists():
                                i["review"].update(
                                    {"3": r3.values()})
                            if r4.exists():
                                i["review"].update(
                                    {"4": r4.values()})
                            if r5.exists():
                                i["review"].update(
                                    {"5": r5.values()})
                            i["review"].update({"total_individual": [individual_review_dict(x, y, int(request.GET["guide_weight"])) for x, y in zip(
                                [r1.values(), r2.values(), r3.values(), r4.values(), r5.values()], [1, 2, 3, 4, 5])]})
                            i["review"].update(
                                {"total": compute_total(i["review"])})
                            for j in i["review"]:
                                for k in i["review"][j]:
                                    if(j in [str(z) for z in range(1, 6)]):
                                        k.pop("id")
                                        k.pop("private_comments")
                                        k["comments"] = k.pop(
                                            "public_comments")
                                        k["fac_id"] = k.pop("fac_id_id")
                                        fac = Faculty.objects.get(
                                            fac_id=k["fac_id"])
                                        k["fac_name"] = fac.name
                                        k["fac_type"] = fac.fac_type
                                        k.pop("srn_id")
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


class MyNotes_List(APIView):

    parser_classes = [JSONParser]

    def get(self, request, user):
        try:
            if(user == User.objects.get(id=jwt_decode_handler(request.META["HTTP_AUTHORIZATION"].split()[1])["user_id"]).get_username()):
                return Response({"mynotes": str(Faculty.objects.get(fac_id=user).mynotes)}, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, user):
        try:
            if(user == User.objects.get(id=jwt_decode_handler(request.META["HTTP_AUTHORIZATION"].split()[1])["user_id"]).get_username()):
                f = Faculty.objects.get(fac_id=user)
                f.mynotes = request.data["mynotes"]
                f.save()
                return Response({"mynotes": str(f.mynotes)}, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class StudentPortal_List(APIView):

    def get(self, request, user):
        try:
            if(user == User.objects.get(id=jwt_decode_handler(request.META["HTTP_AUTHORIZATION"].split()[1])["user_id"]).get_username()):
                if(Faculty.objects.get(fac_id=user).is_admin == True):
                    student_portal = Open_Close.objects.get(
                        oc_type="student_portal")
                    return Response({"open_time": student_portal.open_time, "close_time": student_portal.close_time}, status=status.HTTP_200_OK)
                else:
                    return Response(status=status.HTTP_403_FORBIDDEN)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, user):
        try:
            if(user == User.objects.get(id=jwt_decode_handler(request.META["HTTP_AUTHORIZATION"].split()[1])["user_id"]).get_username()):
                if(Faculty.objects.get(fac_id=user).is_admin == True):
                    student_portal = Open_Close.objects.get(
                        oc_type="student_portal")
                    student_portal.open_time = request.data["open_time"]
                    student_portal.close_time = request.data["close_time"]
                    student_portal.save()
                    return Response(status=status.HTTP_202_ACCEPTED)
                else:
                    return Response(status=status.HTTP_403_FORBIDDEN)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class GenerateFacultyPanel(APIView):

    parser_classes = [JSONParser]

    def post(self, request, user):
        try:
            if(user == User.objects.get(id=jwt_decode_handler(request.META["HTTP_AUTHORIZATION"].split()[1])["user_id"]).get_username()):
                if(Faculty.objects.get(fac_id=user).is_admin == True):
                    if(len(request.data["panel_year_code"]) == len(request.data["panel_id"])):
                        faculty_list = []
                        response_list = []
                        panel_list = [[] for i in request.data["panel_id"]]
                        count_list = [FacultyPanel.objects.filter(panel_id__in=Panel.objects.filter(panel_year_code=i, panel_id=j), fac_id=user).count(
                        ) for i, j in zip(request.data["panel_year_code"], request.data["panel_id"])]
                        for i in request.data["faculty_list"]:
                            faculty_list.append((Faculty.objects.get(
                                fac_id=i).fac_id, Team.objects.filter(guide=i, panel_id=None).count()))
                        faculty_list = sorted(
                            faculty_list, key=lambda i: i[1], reverse=True)
                        for i in faculty_list:
                            min_index = count_list.index(min(count_list))
                            panel_list[min_index].append(i[0])
                            count_list[min_index] += i[1]
                        for pno in range(len(panel_list)):
                            for fno in range(len(panel_list[pno])):
                                response_list.append(
                                    {"fac_id": panel_list[pno][fno],
                                     "panel_year_code": request.data["panel_year_code"][pno],
                                     "panel_id": request.data["panel_id"][pno]})
                        return Response(response_list, status=status.HTTP_200_OK)
                    else:
                        return Response({"detail": "bad input"}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(status=status.HTTP_403_FORBIDDEN)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class StudentPasswordGenerate(APIView):

    parser_classes = [JSONParser]

    def post(self, request, user):
        try:
            if(user == User.objects.get(id=jwt_decode_handler(request.META["HTTP_AUTHORIZATION"].split()[1])["user_id"]).get_username()):
                if(Faculty.objects.get(fac_id=user).is_admin == True and User.objects.get(id=jwt_decode_handler(request.META["HTTP_AUTHORIZATION"].split()[1])["user_id"]).check_password(request.data["password"])):
                    if(request.data["type"] == "mail"):
                        data_tuples = []
                        s = Student.objects.filter(
                            srn__in=request.data["srns"])
                        for i in s:
                            data_tuples.append(("PES Evaluation System Student Credentials", i.srn+"\n\nDear "+i.name+",\n"+"Your password for the PES Final-Year-Project Student-Portal is :"+password_generate(
                                i.srn)+"\nThe password cannot be changed and Faculty Administrator can access this password, hence donot use it elsewhere", EMAIL_HOST_USER, [i.email]))
                        send_mass_mail(data_tuples, fail_silently=True)
                        return Response({"detail": successful}, status=status.HTTP_200_OK)
                    elif(request.data["type"] == "json"):
                        passwords = {}
                        for i in request.data["srns"]:
                            s = Student.objects.filter(srn=i)
                            if(s.exists()):
                                passwords[i] = {"name": s.first().name, "password": password_generate(
                                    i), "email": s.first().email}
                            else:
                                passwords[i] = {"name": None, "password": None}
                        return Response(passwords, status=status.HTTP_200_OK)
                    else:
                        return Respose({"detail": "type should be either 'mail' or 'json'"}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(status=status.HTTP_403_FORBIDDEN)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class PanelReviewMail(APIView):

    parser_classes = [JSONParser]

    def post(self, request, user, panel_year_code, panel_id):
        try:
            if(user == User.objects.get(id=jwt_decode_handler(request.META["HTTP_AUTHORIZATION"].split()[1])["user_id"]).get_username()):
                if(FacultyPanel.objects.filter(fac_id=Faculty.objects.get(fac_id=user), panel_id=Panel.objects.filter(panel_year_code=panel_year_code, panel_id=panel_id).first()).first().is_coordinator):
                    pan = Panel.objects.filter(
                        panel_year_code=panel_year_code, panel_id=panel_id).first()
                    pr = PanelReview.objects.filter(panel_id=pan)
                    coord = Faculty.objects.get(fac_id=user)
                    message = (pan.panel_year_code + '-'+pan.panel_id +
                               '\n'+pan.panel_name+'\n\n'+request.data["message"]+'\n\n')
                    for i in range(1, 6):
                        c = pr.filter(review_number=i).first()
                        if(timezone.now() > c.open_time and timezone.now() < c.close_time):
                            message += ("Review "+str(i)+": " + "The review is currently open till "+str(c.close_time)+"\n") 
                        elif(timezone.now() < c.open_time and timezone.now() < c.close_time):
                            message += ("Review "+str(i)+": " + \
                                        "The review will open at "+str(c.open_time)+" and will close at "+str(c.close_time)+"\n")
                        else:
                            message += ("Review "+str(i)+": " + \
                                        "The review is closed now"+"\n")
                    message += ('\nFrom '+coord.name+'\n(Panel Coordinator)')
                    f = FacultyPanel.objects.filter(
                        fac_id=Faculty.objects.get(fac_id=user), panel_id=pan)
                    data_tuples = []
                    for i in f:
                        fac=i.fac_id
                        data_tuples.append(('PES Evaluation System '+pan.panel_year_code +
                                            '-'+pan.panel_id+' Review Schedule', 'Dear '+fac.name+',\n\n'+message, EMAIL_HOST_USER, [fac.email]))
                    send_mass_mail(data_tuples, fail_silently=True)
                    return Response({"detail":"success"},status=status.HTTP_200_OK)
                else:
                    return Response(status=status.HTTP_403_FORBIDDEN)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
