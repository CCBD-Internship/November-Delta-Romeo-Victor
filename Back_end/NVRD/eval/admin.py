from django.contrib import admin
from .models import *
# Register your models here.
our_models = [Department, Faculty, Panel, PanelReview, Reviews, Student, Team, TeamFacultyReview, FacultyPanel, Profile_Photo]
admin.site.register(our_models)