from django.contrib import auth
from django.contrib.auth import authenticate
from member.models import User
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password

import os
from pathlib import Path


@csrf_exempt
def trainer_login(request):
    if request.method == 'POST':
        # if 'to_main' in request.POST:
        #     return redirect('/')
        if 'login' in request.POST:
            member_id = request.POST['id']
            password = request.POST['password']
            try:
                user = User.objects.get(member_id=member_id)

                if check_password(password, user.password) and user.authority>=1:
                    auth.login(request, user)
                    return redirect('/trainer/trainer_main/', {'user': user})
                else:
                    return redirect('/trainer/login/')
            except Exception:
                pass
                # TODO:should deal with invalid user case

            return redirect('/trainer/login/')

    return render(request, 'trainer-login-page.html')


@csrf_exempt
def trainer_main(request):
    if request.method == 'POST':
        if 'logout' in request.POST:
            auth.logout(request)
            return redirect('/')

        if 'member_progress' in request.POST:

            return redirect('/trainer/member_progress/')
        if 'manage_class' in request.POST:

            return redirect('/trainer/manage_class/')

    return render(request, 'trainer-main-page.html')

@csrf_exempt
def trainer_manage_class(request):
    # if request.method == 'POST':
    #     if 'history_and_progress' in request.POST:
    #
    #         return redirect('/member/history_and_progress/')
    #     if 'start_workout' in request.POST:
    #
    #         return redirect('/member/start_workout/')
    #     if 'record' in request.POST:
    #
    #         return redirect('/member/record/')

    return render(request, 'trainer-manage-class-page.html')

@csrf_exempt
def trainer_manage_class_detail(request):
    # if request.method == 'POST':
    #     if 'history_and_progress' in request.POST:
    #
    #         return redirect('/member/history_and_progress/')
    #     if 'start_workout' in request.POST:
    #
    #         return redirect('/member/start_workout/')
    #     if 'record' in request.POST:
    #
    #         return redirect('/member/record/')

    return render(request, 'trainer-manage-class-detail-page.html')

@csrf_exempt
def trainer_member_progress(request):
    # if request.method == 'POST':
    #     if 'history_and_progress' in request.POST:
    #
    #         return redirect('/member/history_and_progress/')
    #     if 'start_workout' in request.POST:
    #
    #         return redirect('/member/start_workout/')
    #     if 'record' in request.POST:
    #
    #         return redirect('/member/record/')

    return render(request, 'trainer-member-progress-page.html')
