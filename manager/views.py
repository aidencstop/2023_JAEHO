from django.contrib import auth
from django.contrib.auth import authenticate
from member.models import User
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
from member.forms import CustomUserChangeForm, CustomUserDeleteForm, AdminLoginForm
from django.contrib import messages

import os
from pathlib import Path


@csrf_exempt
def manager_login(request):
    if request.method == 'POST':
        if 'back' in request.POST:
            return redirect('/')
        if 'login' in request.POST:
            member_id = request.POST['id']
            password = request.POST['password']
            try:
                user = User.objects.get(member_id=member_id)

                if check_password(password, user.password) and user.authority>=2:
                    auth.login(request, user)
                    return redirect('/manager/manager_main/', {'user': user})
                elif user.authority < 2:
                    messages.error(request, 'You\'re not allowed for manager menu!', extra_tags='')
                    return redirect('/manager/login/')
                else:
                    messages.error(request, 'Please enter correct password!', extra_tags='')
                    return redirect('/manager/login/')
            except Exception:
                messages.error(request, 'Please enter correct ID!', extra_tags='')
                return redirect('/manager/login/')
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
        if 'back' in request.POST:

            return redirect('/manager/manager_main/')
        if 'save' in request.POST:
            if request.POST['password1']==request.POST['password2']:
                print('okay')
                user = User.objects.create_user(
                    member_id=request.POST['member_id'],
                    password=request.POST['password1'],
                    authority=request.POST['authority'],
                    name=request.POST['name'],
                    age=request.POST['age'],
                    gender=request.POST['gender'],
                    height=request.POST['height'],
                )
            # auth.login(request, user)
            return redirect('/manager/manager_sign_up/')

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
    authority_list = []
    for user in users:
        if user.authority==0:
            authority_list.append('Member')
        elif user.authority==1:
            authority_list.append('Trainer')
        else:
            authority_list.append('Manager')
    data_list = zip(users, authority_list)
    return render(
        request,
        'manager-edit-page.html',
        {
            'users': users,
            'authorities': authority_list,
            'data_list': data_list,
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
