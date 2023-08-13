from django.contrib import admin
from .models import Workout, GroupWorkoutClass

# Register your models here.
admin.site.register(Workout)
admin.site.register(GroupWorkoutClass)