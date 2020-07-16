# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = True` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename #db_table values or field names.
from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator
from django_bleach.models import BleachField


class Department(models.Model):
    dept = BleachField(primary_key=True, max_length=50, validators=[
                       RegexValidator(regex='^[^\<\>]*$', message='Invalid Text-Field Input')])

    class Meta:
        managed = True


class Open_Close(models.Model):
    oc_type = BleachField(primary_key=True, max_length=50, validators=[
                          RegexValidator(regex='^[^\<\>]*$', message='Invalid Text-Field Input')])
    open_time = models.DateTimeField()
    close_time = models.DateTimeField()

    class Meta:
        managed = True


class Faculty(models.Model):
    fac_id = BleachField(primary_key=True, max_length=50, validators=[
                         RegexValidator(regex='^[^\<\>]*$', message='Invalid Text-Field Input')])
    name = BleachField(max_length=100, validators=[RegexValidator(
        regex='^[^\<\>]*$', message='Invalid Text-Field Input')])
    email = models.EmailField()
    phone = BleachField(max_length=10, validators=[RegexValidator(
        regex='^[0-9]{10}$', message='Invalid Phone Number')])
    dept = models.ForeignKey('Department', models.DO_NOTHING)
    fac_type = BleachField(max_length=20, choices=[("Assistant Professor", "Assistant Professor"), (
        "Associate Professor", "Associate Professor"), ("Professor", "Professor")], default="Professor")
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    mynotes = BleachField(blank=True, null=True, max_length=1000,
                          default="my notes!!, can write a memo upto 1000 characters")

    class Meta:
        managed = True


class FacultyPanel(models.Model):
    fac_id = models.ForeignKey('Faculty', models.CASCADE)
    panel_id = models.ForeignKey('Panel', models.CASCADE)
    is_coordinator = models.BooleanField(default=False)
    id = models.AutoField(db_column="id", primary_key=True)

    class Meta:
        managed = True
        unique_together = (('fac_id', 'panel_id'),)


# use this to generate values for panel_id
# def add_one_panel(year_code):
#     largest = Panel.objects.filter(year_code=year_code).order_by('panel_id').last()
#     if not largest:
#         return str(1).zfill(10)
#     return str(int(largest.panel_id) + 1).zfill(10)

class Panel(models.Model):

    panel_year_code = BleachField(
        db_column="panel_year_code", max_length=10, validators=[RegexValidator(regex='^[^\<\>]*$', message='Invalid Text-Field Input')])
    panel_id = BleachField(db_column="panel_id", max_length=10, validators=[
                           RegexValidator(regex='^[^\<\>]*$', message='Invalid Text-Field Input')])
    # panel_name = BleachField(
    #     db_column="panel_name", max_length=100, blank=True, null=True)
    panel_name = BleachField(max_length=100, blank=True, null=True, validators=[
                             RegexValidator(regex='^[^\<\>]*$', message='Invalid Text-Field Input')])
    is_active = models.BooleanField(default=True)
    ctime = models.DateTimeField(default=timezone.now)
    id = models.AutoField(db_column="id", primary_key=True)

    class Meta:
        managed = True
        unique_together = (('panel_year_code', 'panel_id'),)


class PanelReview(models.Model):

    review_number = models.IntegerField()
    panel_id = models.ForeignKey('Panel', models.CASCADE, db_column="panel_id")
    open_time = models.DateTimeField()
    close_time = models.DateTimeField()
    id = BleachField(max_length=23, db_column="id", primary_key=True, validators=[
                     RegexValidator(regex='^[^\<\>]*$', message='Invalid Text-Field Input')])

    class Meta:
        managed = True
        unique_together = (('panel_id', 'review_number'),)


class Review1(models.Model):
    srn = models.ForeignKey('Student', models.CASCADE)
    fac_id = models.ForeignKey(
        Faculty, models.SET_NULL, null=True, blank=True)
    concept_of_the_work = models.IntegerField()
    methodology_proposed = models.IntegerField()
    literature_survey = models.IntegerField()
    knowledge_on_the_project = models.IntegerField()
    private_comments = BleachField(max_length=200, blank=True, null=True)
    public_comments = BleachField(max_length=200, blank=True, null=True)
    is_evaluated = models.BooleanField(default=False)
    id = BleachField(max_length=200, primary_key=True, validators=[
                     RegexValidator(regex='^[^\<\>]*$', message='Invalid Text-Field Input')])

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
        unique_together = (('srn', 'fac_id'),)


class Review2(models.Model):
    srn = models.ForeignKey('Student', models.CASCADE)
    fac_id = models.ForeignKey(
        Faculty, models.SET_NULL, null=True, blank=True)
    requirements_specification = models.IntegerField()
    user_interface_use_cases = models.IntegerField()
    understanding_of_technology_platform_middleware = models.IntegerField()
    viva_voce = models.IntegerField()
    private_comments = BleachField(max_length=200, blank=True, null=True)
    public_comments = BleachField(max_length=200, blank=True, null=True)
    is_evaluated = models.BooleanField(default=False)
    id = BleachField(max_length=200, primary_key=True, validators=[
                     RegexValidator(regex='^[^\<\>]*$', message='Invalid Text-Field Input')])

    class Meta:
        managed = True
        constraints = [
            models.CheckConstraint(
                name='2_requirements_specification', check=models.Q(requirements_specification__lte=10) & models.Q(requirements_specification__gte=0)),
            models.CheckConstraint(
                name='2_user_interface_use_cases', check=models.Q(user_interface_use_cases__lte=10) & models.Q(user_interface_use_cases__gte=0)),
            models.CheckConstraint(
                name='2_understanding_of_technology_platform_middleware', check=models.Q(understanding_of_technology_platform_middleware__lte=10) & models.Q(understanding_of_technology_platform_middleware__gte=0)),
            models.CheckConstraint(
                name='2_viva_voce', check=models.Q(understanding_of_technology_platform_middleware__lte=10) & models.Q(understanding_of_technology_platform_middleware__gte=0))
        ]
        #db_table = 'review_2'
        unique_together = (('srn', 'fac_id'),)


class Review3(models.Model):
    srn = models.ForeignKey('Student', models.CASCADE)
    fac_id = models.ForeignKey(
        Faculty, models.SET_NULL, null=True, blank=True)
    design_philosophy_methodology = models.IntegerField()
    user_interface_design_backend_design_and_design_for_any_algorithms = models.IntegerField(
        db_column="user_interface_design_backend_algorithms")
    suitably_of_design_in_comparison_to_the_technology_proposed = models.IntegerField()
    progress_of_the_project_work = models.IntegerField()
    viva_voce = models.IntegerField()
    private_comments = BleachField(max_length=200, blank=True, null=True)
    public_comments = BleachField(max_length=200, blank=True, null=True)
    is_evaluated = models.BooleanField(default=False)
    id = BleachField(max_length=200, primary_key=True)

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
        unique_together = (('srn', 'fac_id'),)


class Review4(models.Model):
    srn = models.ForeignKey('Student', models.CASCADE)
    fac_id = models.ForeignKey(
        Faculty, models.SET_NULL, null=True, blank=True)
    project_work_results = models.IntegerField()
    quality_of_demo = models.IntegerField()
    project_report = models.IntegerField()
    viva_voce = models.IntegerField()
    private_comments = BleachField(max_length=200, blank=True, null=True)
    public_comments = BleachField(max_length=200, blank=True, null=True)
    is_evaluated = models.BooleanField(default=False)
    id = BleachField(max_length=200, primary_key=True, validators=[
                     RegexValidator(regex='^[^\<\>]*$', message='Invalid Text-Field Input')])

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
        unique_together = (('srn', 'fac_id'),)


class Review5(models.Model):
    srn = models.ForeignKey('Student', models.CASCADE)
    fac_id = models.ForeignKey(
        Faculty, models.SET_NULL, null=True, blank=True, db_column="fac_id")
    project_work_results = models.IntegerField()
    quality_of_demo = models.IntegerField()
    project_report = models.IntegerField()
    viva_voce = models.IntegerField()
    private_comments = BleachField(max_length=200, blank=True, null=True)
    public_comments = BleachField(max_length=200, blank=True, null=True)
    is_evaluated = models.BooleanField(default=False)
    id = BleachField(max_length=200, primary_key=True, validators=[
                     RegexValidator(regex='^[^\<\>]*$', message='Invalid Text-Field Input')])

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
        unique_together = (('srn', 'fac_id'),)


class Student(models.Model):
    srn = BleachField(primary_key=True, max_length=20, validators=[
        RegexValidator(regex='^PES', message='SRN incorrect')])
    name = BleachField(max_length=100, validators=[RegexValidator(
        regex='^[^\<\>]*$', message='Invalid Text-Field Input')])
    email = models.EmailField()
    phone = BleachField(max_length=10, validators=[RegexValidator(
        regex='^[0-9]{10}$', message='Invalid Phone number')])
    dept = models.ForeignKey(Department, models.DO_NOTHING)
    team_id = models.ForeignKey('Team', models.SET_NULL, null=True, blank=True)

    class Meta:
        managed = True


class Team(models.Model):
    team_year_code = BleachField(
        db_column="team_year_code", max_length=10, validators=[RegexValidator(regex='^[^\<\>]*$', message='Invalid Text-Field Input')])
    team_id = BleachField(db_column="team_id", max_length=10, validators=[
                          RegexValidator(regex='^[^\<\>]*$', message='Invalid Text-Field Input')])
    team_name = BleachField(max_length=100, blank=True, null=True, validators=[
                            RegexValidator(regex='^[^\<\>]*$', message='Invalid Text-Field Input')])
    description = BleachField(max_length=200, blank=True, null=True, validators=[
                              RegexValidator(regex='^[^\<\>]*$', message='Invalid Text-Field Input')])
    guide = models.ForeignKey(
        Faculty, models.SET_NULL, blank=True, null=True)
    panel_id = models.ForeignKey(Panel, models.SET_NULL, blank=True, null=True)
    id = models.AutoField(db_column="id", primary_key=True)

    class Meta:
        managed = True
        unique_together = (('team_year_code', 'team_id'),)


class TeamFacultyReview(models.Model):
    team_id = models.ForeignKey(Team, models.CASCADE)
    fac_id = models.ForeignKey(
        Faculty, models.SET_NULL, null=True, blank=True)
    review_number = models.IntegerField()
    remark = BleachField(max_length=200, blank=True, null=True, validators=[
                         RegexValidator(regex='^[^\<\>]*$', message='Invalid Text-Field Input')])
    id = models.AutoField(db_column="id", primary_key=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                name='review_number_gte', check=models.Q(review_number__gte=1)),
            models.CheckConstraint(
                name='review_number_lte', check=models.Q(review_number__lte=5))
        ]
        managed = True
        unique_together = (('team_id', 'fac_id', 'review_number'),)


class Profile_Photo(models.Model):
    srn = models.OneToOneField(Student,
                               on_delete=models.CASCADE,
                               primary_key=True,)
    image = models.ImageField(
        default="static/default_user.png", upload_to="student_images")

# from django.contrib.auth.models import User
# from eval.models import *
# from rest_framework.authtoken.models import Token
# for i in Faculty.objects.all():
#     if(not User.objects.filter(username=i.fac_id).exists()):
#         User.objects.create_user(last_name=i.name,username=i.fac_id,password=i.fac_id,email=None)
#         print("hi")
#     if(not Token.objects.filter(user=User.objects.get(username=i.fac_id)).exists()):
#         token = Token.objects.create(user=User.objects.get(username=i.fac_id))
#         print("hey")
