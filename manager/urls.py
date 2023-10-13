from django.urls import path
from .views import *
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('login/', manager_login, name='manager_login'),
    path('manager_main/', manager_main, name='manager_main'),
    path('manager_sign_up/', manager_sign_up, name='manager_sign_up'),
    path('manager_edit/', manager_edit, name='manager_edit'),
    path('manager_edit_form/<int:pk>/', manager_edit_form, name='manager_edit_form'),
]
