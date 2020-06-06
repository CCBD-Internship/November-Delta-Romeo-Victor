from django.contrib import admin
from .models import *
# Register your models here.
our_models = [Department, Faculty, Panel, PanelReview, Review1, Review2,
              Review3, Review4, Review5, Student, Team, TeamFacultyReview,FacultyPanel]
admin.site.register(our_models)