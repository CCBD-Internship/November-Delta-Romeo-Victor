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
    id = models.AutoField(db_column="id",primary_key=True)

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

    panel_year_code = models.CharField(db_column="panel_year_code",max_length=10)
    panel_id = models.CharField(db_column="panel_id",max_length=10)
    panel_name = models.CharField(db_column="panel_name",max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    ctime = models.DateTimeField(default=timezone.now)
    id = models.AutoField(db_column="id",primary_key=True)

    class Meta:
        managed = True
        #db_table = 'panel'
        unique_together = (('panel_year_code', 'panel_id'),)


class PanelReview(models.Model):

    review_number = models.IntegerField()
    panel_id = models.ForeignKey('Panel', models.CASCADE,db_column="panel_id")
    open_time = models.DateTimeField()
    close_time = models.DateTimeField()
    # id = models.AutoField(db_column="id",primary_key=True)
    id = models.CharField(max_length=23,db_column="id",primary_key=True)

    class Meta:
        managed = True
        #db_table = 'panel_review'
        unique_together = (('panel_id', 'review_number'),)


class Review1(models.Model):
    srn = models.ForeignKey('Student', models.CASCADE)
    fac_id = models.ForeignKey(Faculty, models.DO_NOTHING, null=True, blank=True)
    concept_of_the_work= models.integerfield()
    methodology_proposed = models.integerfield()
    literature_survey = models.integerfield()
    knowledge_on_the_project = models.integerfield()
    comments = models.CharField(max_length=200, blank=True, null=True)
    id = models.AutoField(primary_key=True)

    class Meta:
        managed = True
        constraints = [
            models.CheckConstraint(
                name='1_concept_of_the_work', check=models.Q(concept_of_the_work__lte=10) & models.Q(concept_of_the_work__gte=0)),
            models.CheckConstraint(
                name='1_methodology_proposed', check=models.Q(methodology_proposed__lte=10) & models.Q(methodology_proposed__gte=0)),
            models.CheckConstraint(
                name='1_literature_survey', check=models.Q(literature_survey__lte=10) & models.Q(literature_survey__gte=0)),
            models.CheckConstraint(
                name='1_knowledge_on_the_project', check=models.Q(knowledge_on_the_project__lte=10) & models.Q(knowledge_on_the_project__gte=0))
        ]
        #db_table = 'review_1'
        unique_together = (('srn', 'fac_id'),)


class Review2(models.Model):
    srn = models.ForeignKey('Student', models.CASCADE)
    fac_id = models.ForeignKey(Faculty, models.DO_NOTHING, null=True, blank=True)
    requirements_specification = models.integerfield()
    user_interface_use_cases = models.integerfield()
    understanding_of_technology_platform_middleware = models.integerfield()
    viva_voce = models.integerfield()
    comments = models.CharField(max_length=200, blank=True, null=True)
    id = models.AutoField(primary_key=True)

    class Meta:
        managed = True
        constraints = [
            models.CheckConstraint(
                name='2_requirements_specification', check=models.Q(requirements_specification__lte=10) & models.Q(requirements_specification__gte=0)),
            models.CheckConstraint(
                name='2_user_interface_use_cases', check=models.Q(user_interface_use_cases__lte=10) & models.Q(user_interface_use_cases__gte=0)),
            models.CheckConstraint(
                name='2_understanding_of_technology_platform_middleware', check=models.Q(understanding_of_technology_platform_middleware__lte=10) & models.Q(lunderstanding_of_technology_platform_middleware__gte=0)),
            models.CheckConstraint(
                name='2_viva_voce', check=models.Q(knowledge_on_the_project__lte=10) & models.Q(knowledge_on_the_project__gte=0))
        ]
        #db_table = 'review_2'
        unique_together = (('srn', 'fac_id'),)


class Review3(models.Model):
    srn = models.ForeignKey('Student', models.CASCADE)
    fac_id = models.ForeignKey(Faculty, models.DO_NOTHING, null=True, blank=True)
    design_philosophy_methodology = models.integerfield()
    user_interface_design_backend_design_and_design_for_any_algorithms = models.integerfield()
    suitably_of_design_in_comparison_to_the_technology_proposed = models.integerfield()
    progress_of_the_project_work = models.integerfield()
    viva_voce = models.integerfield()
    comments = models.CharField(max_length=200, blank=True, null=True)
    id = models.AutoField(primary_key=True)

    class Meta:
        managed = True
        constraints = [
            models.CheckConstraint(
                name='3_design_philosophy_methodology', check=models.Q(design_philosophy_methodology__lte=10) & models.Q(design_philosophy_methodology__gte=0)),
            models.CheckConstraint(
                name='3_user_interface_design_backend_design_and_design_for_any_algorithms', check=models.Q(user_interface_design_backend_design_and_design_for_any_algorithms__lte=10) & models.Q(user_interface_design_backend_design_and_design_for_any_algorithms__gte=0)),
            models.CheckConstraint(
                name='3_suitably_of_design_in_comparison_to_the_technology_proposed', check=models.Q(suitably_of_design_in_comparison_to_the_technology_proposed__lte=5) & models.Q(suitably_of_design_in_comparison_to_the_technology_proposed__gte=0)),
            models.CheckConstraint(
                name='3_progress_of_the_project_work', check=models.Q(progress_of_the_project_work__lte=5) & models.Q(progress_of_the_project_work__gte=0)),
            models.CheckConstraint(
                name='3_viva_voce', check=models.Q(viva_voce__lte=5) & models.Q(viva_voce__gte=0))
        ]
        #db_table = 'review_3'
        unique_together = (('srn', 'fac_id'),)


class Review4(models.Model):
    srn = models.ForeignKey('Student', models.CASCADE)
    fac_id = models.ForeignKey(Faculty, models.DO_NOTHING, null=True, blank=True)
    project_work_results = models.integerfield()
    quality_of_demo = models.integerfield()
    project_report = models.integerfield()
    viva_voce = models.integerfield()
    comments = models.CharField(max_length=200, blank=True, null=True)
    id = models.AutoField(primary_key=True)

    class Meta:
        managed = True
        constraints = [
            models.CheckConstraint(
                name='4_project_work_results', check=models.Q(project_work_results__lte=10) & models.Q(project_work_results__gte=0)),
            models.CheckConstraint(
                name='4_quality_of_demo', check=models.Q(quality_of_demo__lte=10) & models.Q(quality_of_demo__gte=0)),
            models.CheckConstraint(
                name='4_project_report', check=models.Q(project_report__lte=10) & models.Q(project_report__gte=0)),
            models.CheckConstraint(
                name='4_viva_voce', check=models.Q(viva_voce__lte=10) & models.Q(viva_voce__gte=0))
        ]
        #db_table = 'review_4'
        unique_together = (('srn', 'fac_id'),)

class Review5(models.Model):
    srn = models.ForeignKey('Student', models.CASCADE)
    fac_id = models.ForeignKey(
        Faculty, models.DO_NOTHING, null=True, blank=True,db_column="fac_id")
    project_work_results = models.integerfield()
    quality_of_demo = models.integerfield()
    project_report = models.integerfield()
    viva_voce = models.integerfield()
    comments = models.CharField(max_length=200, blank=True, null=True)
    id = models.AutoField(db_column="id",primary_key=True)

    class Meta:
        managed = True
        constraints = [
            models.CheckConstraint(
                name='5_project_work_results', check=models.Q(project_work_results__lte=10) & models.Q(project_work_results__gte=0)),
            models.CheckConstraint(
                name='5_quality_of_demo', check=models.Q(quality_of_demo__lte=10) & models.Q(quality_of_demo__gte=0)),
            models.CheckConstraint(
                name='5_project_report', check=models.Q(project_report__lte=10) & models.Q(project_report__gte=0)),
            models.CheckConstraint(
                name='5_viva_voce', check=models.Q(viva_voce__lte=10) & models.Q(viva_voce__gte=0))
        ]
        #db_table = 'review_5'
        unique_together = (('srn', 'fac_id'),)


class Student(models.Model):
    srn = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=13)
    dept = models.ForeignKey(Department, models.DO_NOTHING)
    team_id = models.ForeignKey('Team', models.DO_NOTHING, blank=True, null=True)

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
    team_year_code = models.CharField(db_column="team_year_code",max_length=10)
    team_id = models.CharField(db_column="team_id",max_length=10)
    team_name = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    guide = models.ForeignKey(
        Faculty, models.DO_NOTHING, blank=True, null=True)
    panel_id = models.ForeignKey(Panel, models.DO_NOTHING, blank=True, null=True)
    id = models.AutoField(db_column="id",primary_key=True)

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
    id = models.AutoField(db_column="id",primary_key=True)

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
