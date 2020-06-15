# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = True` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename #db_table values or field names.
from django.db import models
from django.utils import timezone


class Department(models.Model):
    dept = models.CharField(primary_key=True, max_length=50)

    class Meta:
        managed = True
        #db_table = 'department'


class Faculty(models.Model):
    fac_id = models.CharField(primary_key=True, max_length=50)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=13)
    dept = models.ForeignKey('Department', models.DO_NOTHING)
    fac_type = models.CharField(max_length=20, choices=[("assistant_prof", "assistant_prof"), (
        "associate_prof", "associate_prof"), ("professor", "professor")], default="professor")
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    class Meta:
        managed = True
        constraints = [
            models.CheckConstraint(
                name='phone_constraint_faculty', check=models.Q(phone__startswith='+')),
        ]
        #db_table = 'faculty'


class FacultyPanel(models.Model):
    fac_id = models.ForeignKey('Faculty', models.CASCADE)
    panel_id = models.ForeignKey('Panel', models.CASCADE)
    is_coordinator = models.BooleanField(default=False)
    id = models.AutoField(primary_key=True)

    class Meta:
        managed = True
        #db_table = 'faculty_panel'
        unique_together = (('fac_id', 'panel_id'),)


# use this to generate values for panel_id
# def add_one_panel(year_code):
#     largest = Panel.objects.filter(year_code=year_code).order_by('panel_id').last()
#     if not largest:
#         return str(1).zfill(10)
#     return str(int(largest.panel_id) + 1).zfill(10)

class Panel(models.Model):

    panel_year_code = models.CharField(max_length=10)
    panel_id = models.CharField(max_length=10)
    panel_name = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    ctime = models.DateTimeField(default=timezone.now)
    id = models.AutoField(primary_key=True)

    class Meta:
        managed = True
        #db_table = 'panel'
        unique_together = (('panel_year_code', 'panel_id'),)


class PanelReview(models.Model):

    review_number = models.IntegerField()
    panel_id = models.ForeignKey('Panel', models.CASCADE)
    open_time = models.DateTimeField()
    close_time = models.DateTimeField()
    id = models.AutoField(primary_key=True)

    class Meta:
        managed = True
        #db_table = 'panel_review'
        unique_together = (('panel_id', 'review_number'),)


class Review1(models.Model):
    srn = models.ForeignKey('Student', models.CASCADE)
    fac_id = models.ForeignKey(
        Faculty, models.DO_NOTHING, null=True, blank=True)
    project_work = models.IntegerField()
    quality_of_demo = models.IntegerField()
    project_report = models.IntegerField()
    viva_voce = models.IntegerField()
    comments = models.CharField(max_length=200, blank=True, null=True)
    id = models.AutoField(primary_key=True)

    class Meta:
        managed = True
        #db_table = 'review_1'
        unique_together = (('srn', 'fac_id'),)


class Review2(models.Model):
    srn = models.ForeignKey('Student', models.CASCADE)
    fac_id = models.ForeignKey(
        Faculty, models.DO_NOTHING, null=True, blank=True)
    project_work = models.IntegerField()
    quality_of_demo = models.IntegerField()
    project_report = models.IntegerField()
    viva_voce = models.IntegerField()
    comments = models.CharField(max_length=200, blank=True, null=True)
    id = models.AutoField(primary_key=True)

    class Meta:
        managed = True
        #db_table = 'review_2'
        unique_together = (('srn', 'fac_id'),)


class Review3(models.Model):
    srn = models.ForeignKey('Student', models.CASCADE)
    fac_id = models.ForeignKey(
        Faculty, models.DO_NOTHING, null=True, blank=True)
    project_work = models.IntegerField()
    quality_of_demo = models.IntegerField()
    project_report = models.IntegerField()
    viva_voce = models.IntegerField()
    comments = models.CharField(max_length=200, blank=True, null=True)
    id = models.AutoField(primary_key=True)

    class Meta:
        managed = True
        #db_table = 'review_3'
        unique_together = (('srn', 'fac_id'),)


class Review4(models.Model):
    srn = models.ForeignKey('Student', models.CASCADE)
    fac_id = models.ForeignKey(
        Faculty, models.DO_NOTHING, null=True, blank=True)
    project_work = models.IntegerField()
    quality_of_demo = models.IntegerField()
    project_report = models.IntegerField()
    viva_voce = models.IntegerField()
    comments = models.CharField(max_length=200, blank=True, null=True)
    id = models.AutoField(primary_key=True)

    class Meta:
        managed = True
        #db_table = 'review_4'
        unique_together = (('srn', 'fac_id'),)


class Review5(models.Model):
    srn = models.ForeignKey('Student', models.CASCADE)
    fac_id = models.ForeignKey(
        Faculty, models.DO_NOTHING, null=True, blank=True)
    project_work = models.IntegerField()
    quality_of_demo = models.IntegerField()
    project_report = models.IntegerField()
    viva_voce = models.IntegerField()
    comments = models.CharField(max_length=200, blank=True, null=True)
    id = models.AutoField(primary_key=True)

    class Meta:
        managed = True
        #db_table = 'review_5'
        unique_together = (('srn', 'fac_id'),)


class Student(models.Model):
    srn = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=13)
    dept = models.ForeignKey(Department, models.DO_NOTHING)
    team = models.ForeignKey('Team', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        constraints = [
            models.CheckConstraint(
                name='phone_constraint_student', check=models.Q(phone__startswith='+')),
            models.CheckConstraint(name='srn_constraint',
                                   check=models.Q(srn__startswith='PES')),
        ]
        #db_table = 'student'

# use this function to generate team_id always
# def add_one_team(year_code):
#     largest = Team.objects.filter(year_code=year_code).order_by('team_id').last()
#     if not largest:
#         return str(1).zfill(10)
#     return str(int(largest.team_id) + 1).zfill(10)


class Team(models.Model):
    team_year_code = models.CharField(max_length=10)
    team_id = models.CharField(max_length=10)
    team_name = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    guide = models.ForeignKey(
        Faculty, models.DO_NOTHING, blank=True, null=True)
    panel = models.ForeignKey(Panel, models.DO_NOTHING, blank=True, null=True)
    id = models.AutoField(primary_key=True)

    class Meta:
        managed = True
        unique_together = (('team_year_code', 'team_id'),)
        #db_table = 'team'


class TeamFacultyReview(models.Model):
    team_id = models.ForeignKey(Team, models.DO_NOTHING)
    fac_id = models.ForeignKey(
        Faculty, models.DO_NOTHING, null=True, blank=True)
    review_number = models.IntegerField()
    remark = models.CharField(max_length=200, blank=True, null=True)
    id = models.AutoField(primary_key=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                name='review_number_gte', check=models.Q(review_number__gte=1)),
            models.CheckConstraint(
                name='review_number_lte', check=models.Q(review_number__lte=5))
        ]
        managed = True
        #db_table = 'team_faculty_review'
        unique_together = (('team_id', 'fac_id', 'review_number'),)

# from django.contrib.auth.models import User
# # from eval.models import *
# from rest_framework.authtoken.models import Token
# for i in Faculty.objects.all():
#     if(not User.objects.filter(username=i.fac_id).exists()):
#         User.objects.create_user(last_name=i.name,username=i.fac_id,password=i.fac_id,email=None)
#         print("hi")
#     if(not Token.objects.filter(user=User.objects.get(username=i.fac_id)).exists()):
#         token = Token.objects.create(user=User.objects.get(username=i.fac_id))
#         print("hey")
