from django.contrib import admin
from .models import Department, Faculty, Panel, PanelReview, Review1, Review2, Review3, Review4, Review5, Student, Team, TeamFaculty
# Register your models here.
our_models = [Department, Faculty, Panel, PanelReview, Review1, Review2,
              Review3, Review4, Review5, Student, Team, TeamFaculty]
admin.site.register(our_models)