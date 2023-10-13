from django.contrib import auth
from django.contrib.auth import authenticate
from member.models import User
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
from member.forms import CustomUserChangeForm, CustomUserDeleteForm, AdminLoginForm

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
        if 'signup' in request.POST:
            return redirect('/manager/manager_sign_up/')
        if 'edit' in request.POST:
            return redirect('/manager/manager_edit/')
        # if 'remove' in request.POST:
        #     selected = request.POST.getlist('selected')
        #     for pk in selected:
        #         user = User.objects.get(pk=int(pk))
        #         # print(user.name)
        #         form = CustomUserDeleteForm(request.POST, instance=user)
        #         if form.is_valid():
        #             # form.save()
        #             user = form.save()  # 변경
        #             user.is_active = False  # 변경
        #             user.save()
    #     if 'edit' in request.POST:
    #         selected = request.POST.getlist('selected')
    #         print(selected)
    #         if len(selected)>1:
    #             pass
    #         elif len(selected)==1:
    #             pk = selected[0]
    #             user = User.objects.get(pk=pk)
    #
    #             return render(
    #                 request,
    #                 'admin4.html',
    #                 {
    #                     'user': user
    #                 }
    #             )
    #         else:
    #             pass

    members = User.objects.all().order_by('pk')
    active_members = [member for member in members]
    return render(
        request,
        'manager-main-page.html',
        {
            'members': active_members
        }
    )

@csrf_exempt
def manager_sign_up(request):
    if request.method == 'POST':
        if 'logout' in request.POST:
            auth.logout(request)
            return redirect('/')
        if 'save' in request.POST:
            user = User.objects.create_user(
                member_id=request.POST['member_id'],
                authority=request.POST['authority'],
                name=request.POST['name'],
                age=request.POST['age'],
                gender=request.POST['gender'],
                height=request.POST['height'],
            )
            # auth.login(request, user)
            return redirect('/member/add_a_new_member/')

    return render(request, 'manager-sign-up-page.html')


@csrf_exempt
def manager_edit(request):
    if request.method == 'POST':
        if 'back' in request.POST:
            return redirect('/manager/manager_main/')
        # if 'edit' in request.POST:
        #     user = User.objects.get(pk=pk)
        #
        #     form = CustomUserChangeForm(request.POST, instance=user)
        #     if form.is_valid():
        #         form.save()
        #
        #         return render(
        #             request,
        #             'admin4.html',
        #             {
        #                 'user': user
        #             }
        #         )
    users = User.objects.all().order_by('pk')

    return render(
        request,
        'manager-edit-page.html',
        {
            'users': users
        }
    )

@csrf_exempt
def manager_edit_form(request, pk):
    if request.method == 'POST':
        if 'back' in request.POST:
            return redirect('/manager/manager_edit/')
        if 'save' in request.POST:
            user = User.objects.get(pk=pk)
            user.setMemberId(request.POST['member_id'])
            user.setAuthority(request.POST['authority'])
            user.setName(request.POST['name'])
            user.setAge(request.POST['age'])
            user.setGender(request.POST['gender'])
            user.setHeight(request.POST['height'])
            return redirect('/manager/manager_edit_form/' + str(pk) + '/')

    user = User.objects.get(pk=pk)
    return render(
        request,
        'manager-edit-form-page.html',
        {
            'user': user
        }
    )
