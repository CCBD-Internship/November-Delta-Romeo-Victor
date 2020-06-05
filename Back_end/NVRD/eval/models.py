# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Department(models.Model):
    dept = models.CharField(primary_key=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'department'


class Faculty(models.Model):
    fac_id = models.CharField(primary_key=True, max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=13)
    dept = models.ForeignKey(Department, models.DO_NOTHING, db_column='dept')
    panel = models.ForeignKey('Panel', models.DO_NOTHING, blank=True, null=True)
    is_coordinator = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'faculty'


class Panel(models.Model):
    label = models.CharField(max_length=100)
    ctime = models.DateTimeField(blank=True, null=True)
    is_sealed = models.BooleanField(blank=True, null=True)
    panel_id = models.BigIntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'panel'


class PanelReview(models.Model):
    panel = models.OneToOneField(Panel, models.DO_NOTHING, primary_key=True)
    review_number = models.IntegerField()
    open_time = models.DateTimeField()
    close_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'panel_review'
        unique_together = (('panel', 'review_number'),)


class Review1(models.Model):
    srn = models.OneToOneField('Student', models.DO_NOTHING, db_column='srn', primary_key=True)
    team = models.ForeignKey('TeamFaculty', models.DO_NOTHING)
    fac_id = models.CharField(max_length=50)
    project_work = models.IntegerField()
    quality_of_demo = models.IntegerField()
    project_report = models.IntegerField()
    viva_voce = models.IntegerField()
    comments = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'review_1'
        unique_together = (('srn', 'fac_id'),)


class Review2(models.Model):
    srn = models.OneToOneField('Student', models.DO_NOTHING, db_column='srn', primary_key=True)
    team = models.ForeignKey('TeamFaculty', models.DO_NOTHING)
    fac_id = models.CharField(max_length=50)
    project_work = models.IntegerField()
    quality_of_demo = models.IntegerField()
    project_report = models.IntegerField()
    viva_voce = models.IntegerField()
    comments = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'review_2'
        unique_together = (('srn', 'fac_id'),)


class Review3(models.Model):
    srn = models.OneToOneField('Student', models.DO_NOTHING, db_column='srn', primary_key=True)
    team = models.ForeignKey('TeamFaculty', models.DO_NOTHING)
    fac_id = models.CharField(max_length=50)
    project_work = models.IntegerField()
    quality_of_demo = models.IntegerField()
    project_report = models.IntegerField()
    viva_voce = models.IntegerField()
    comments = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'review_3'
        unique_together = (('srn', 'fac_id'),)


class Review4(models.Model):
    srn = models.OneToOneField('Student', models.DO_NOTHING, db_column='srn', primary_key=True)
    team = models.ForeignKey('TeamFaculty', models.DO_NOTHING)
    fac_id = models.CharField(max_length=50)
    project_work = models.IntegerField()
    quality_of_demo = models.IntegerField()
    project_report = models.IntegerField()
    viva_voce = models.IntegerField()
    comments = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'review_4'
        unique_together = (('srn', 'fac_id'),)


class Review5(models.Model):
    srn = models.OneToOneField('Student', models.DO_NOTHING, db_column='srn', primary_key=True)
    team = models.ForeignKey('TeamFaculty', models.DO_NOTHING)
    fac_id = models.CharField(max_length=50)
    project_work = models.IntegerField()
    quality_of_demo = models.IntegerField()
    project_report = models.IntegerField()
    viva_voce = models.IntegerField()
    comments = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'review_5'
        unique_together = (('srn', 'fac_id'),)


class Student(models.Model):
    srn = models.CharField(primary_key=True, max_length=15)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=13)
    dept = models.ForeignKey(Department, models.DO_NOTHING, db_column='dept')
    team = models.ForeignKey('Team', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'student'


class Team(models.Model):
    team_name = models.CharField(max_length=50)
    description = models.CharField(max_length=200, blank=True, null=True)
    guide = models.ForeignKey(Faculty, models.DO_NOTHING, db_column='guide', blank=True, null=True)
    panel = models.ForeignKey(Panel, models.DO_NOTHING, blank=True, null=True)
    team_id = models.BigIntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'team'


class TeamFaculty(models.Model):
    team = models.OneToOneField(Team, models.DO_NOTHING, primary_key=True)
    fac = models.ForeignKey(Faculty, models.DO_NOTHING)
    remark_1 = models.CharField(max_length=200, blank=True, null=True)
    remark_2 = models.CharField(max_length=200, blank=True, null=True)
    remark_3 = models.CharField(max_length=200, blank=True, null=True)
    remark_4 = models.CharField(max_length=200, blank=True, null=True)
    remark_5 = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'team_faculty'
        unique_together = (('team', 'fac'),)
