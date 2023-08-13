from django.contrib import auth
from django.contrib.auth import authenticate
from member.models import User
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password

import os
from pathlib import Path


@csrf_exempt
def manager_login(request):
    if request.method == 'POST':
        # if 'to_main' in request.POST:
        #     return redirect('/')
        if 'login' in request.POST:
            member_id = request.POST['id']
            password = request.POST['password']
            try:
                user = User.objects.get(member_id=member_id)

                if check_password(password, user.password) and user.authority>=2:
                    auth.login(request, user)
                    return redirect('/manager/manager_main/', {'user': user})
                else:
                    return redirect('/manager/login/')
            except Exception:
                pass
                # TODO:should deal with invalid user case

            return redirect('/manager/login/')

    return render(request, 'manager-login-page.html')


@csrf_exempt
def manager_main(request):
    if request.method == 'POST':
        if 'logout' in request.POST:
            auth.logout(request)
            return redirect('/')


    return render(request, 'manager-main-page.html')
