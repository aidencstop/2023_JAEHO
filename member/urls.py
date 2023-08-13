from django.urls import path
from .views import *
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('login/', member_login, name='member_login'),
    path('member_main/', member_main, name='member_main'),
    path('history_and_progress/', member_history_and_progress, name='member_history_and_progress'),
    path('start_workout/', member_start_workout, name='member_start_workout'),
    path('start_workout_alone/', member_start_workout_alone, name='member_start_workout_alone'),
    path('start_workout_group/', member_start_workout_group, name='member_start_workout_group'),
    path('start_workout_group_booked/<int:class_pk>/', member_start_workout_group_booked, name='member_start_workout_group_booked'),
    path('record/', member_record, name='member_record'),
]
