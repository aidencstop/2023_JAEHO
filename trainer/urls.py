from django.urls import path
from .views import *
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('login/', trainer_login, name='trainer_login'),
    path('trainer_main/', trainer_main, name='trainer_main'),
    path('manage_class/', trainer_manage_class, name='trainer_manage_class'),
    path('manage_class_detail/<int:class_pk>/', trainer_manage_class_detail, name='trainer_manage_class_detail'),
    path('member_progress/', trainer_member_progress, name='trainer_member_progress'),
    path('history_and_progress/<int:member_pk>/', trainer_history_and_progress, name='trainer_history_and_progress'),
]

