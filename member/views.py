from django.contrib import auth
from django.contrib.auth import authenticate
from .models import User
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .forms import CustomUserChangeForm, CustomUserDeleteForm, AdminLoginForm
from django.contrib.auth.hashers import check_password

import os
from pathlib import Path

@csrf_exempt
def member_login(request):
    if request.method == 'POST':
        # if 'to_main' in request.POST:
        #     return redirect('/')
        if 'login' in request.POST:
            member_id = request.POST['id']
            password = request.POST['password']
            try:
                user = User.objects.get(member_id=member_id)

                if check_password(password, user.password):
                    auth.login(request, user)
                    return redirect('/member/member_main/', {'user': user})
                else:
                    return redirect('/member/login/')
            except Exception:
                pass
                # TODO:should deal with invalid user case

            return redirect('/member/login/')

    return render(request, 'member-login-page.html')

@csrf_exempt
def member_main(request):
    if request.method == 'POST':
        if 'history_and_progress' in request.POST:

            return redirect('/member/history_and_progress/')
        if 'start_workout' in request.POST:

            return redirect('/member/start_workout/')
        if 'record' in request.POST:

            return redirect('/member/record/')

    return render(request, 'member-main-page.html')

@csrf_exempt
def member_history_and_progress(request):
    if request.method == 'POST':
        if 'logout' in request.POST:
            auth.logout(request)
            return redirect('/')
    return render(request, 'member-history-and-progress-page.html')

@csrf_exempt
def member_start_workout(request):
    if request.method == 'POST':
        if 'start_workout_alone' in request.POST:

            return redirect('/member/start_workout_alone/')
        if 'start_workout_group' in request.POST:

            return redirect('/member/start_workout_group/')
    return render(request, 'member-start-workout-page.html')

@csrf_exempt
def member_start_workout_alone(request):
    # if request.method == 'POST':
    return render(request, 'member-start-workout-alone-page.html')

@csrf_exempt
def member_start_workout_group(request):
    # if request.method == 'POST':
    return render(request, 'member-start-workout-group-page.html')


@csrf_exempt
def member_record(request):
    # if request.method == 'POST':
    return render(request, 'member-record-page.html')
