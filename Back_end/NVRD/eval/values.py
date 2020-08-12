from eval.models import *
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

# def add_one_panel(panel_year_code):
#     largest = Panel.objects.filter(
#         panel_year_code=panel_year_code).order_by('panel_id').last()
#     if not largest:
#         return str(1).zfill(10)
#     return str(int(largest.panel_id) + 1).zfill(10)


# def add_one_team(team_year_code):
#     largest = Team.objects.filter(
#         team_year_code=team_year_code).order_by('team_id').last()
#     if not largest:
#         return str(1).zfill(10)
#     return str(int(largest.team_id) + 1).zfill(10)

d = Department(dept="CSE")
d.save()
fnames=["admin","eval1","eval2","coord1","coord2"]
fadmins=[1,0,0,0,0]
for i in range(len(fnames)):
    f = Faculty(fac_id=fnames[i], dept=Department.objects.filter(dept="CSE").first(),
            email="karob12273@mail2paste.com", phone="1234567890", name=fnames[i],is_admin=fadmins[i])
    f.save()
for i in Faculty.objects.all():
    if(not User.objects.filter(username=i.fac_id).exists()):
        User.objects.create_user(last_name=i.name,username=i.fac_id,password=i.fac_id,email=None)
    if(not Token.objects.filter(user=User.objects.get(username=i.fac_id)).exists()):
        token = Token.objects.create(user=User.objects.get(username=i.fac_id))

oc=Open_Close(oc_type="student_portal",open_time=timezone.now(),close_time=timezone.now())
oc.save()