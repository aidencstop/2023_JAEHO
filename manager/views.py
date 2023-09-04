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
        if 'signup' in request.POST:
            return redirect('/manager/manager_sign_up/')
        if 'restore' in request.POST:
            return redirect('/manager/restore_members/')
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
            return redirect('/member/member_list/')
        if 'save' in request.POST:
            user = User.objects.create_user(
                member_id=request.POST['member_id'],
                name=request.POST['name'],
                age=request.POST['age'],
                gender=request.POST['gender'],
                registration_date=request.POST['registration_date'],
                phone_number=request.POST['phone_number'],
                athletic_experience=request.POST['athletic_experience'],
                expiration_date=request.POST['expiration_date'],
            )
            # auth.login(request, user)
            return redirect('/member/add_a_new_member/')

    return render(request, 'manager-sign-up-page.html')

@csrf_exempt
def edit_member_info(request, pk):
    if request.method == 'POST':
        if 'back' in request.POST:
            return redirect('/member/member_list/')
        if 'save' in request.POST:
            user = User.objects.get(pk=pk)

            form = CustomUserChangeForm(request.POST, instance=user)
            if form.is_valid():
                form.save()

                return render(
                    request,
                    'admin4.html',
                    {
                        'user': user
                    }
                )

    user = User.objects.get(pk=pk)
    return render(
        request,
        'admin4.html',
        {
            'user': user
        }
    )


@csrf_exempt
def restore_members(request):
    if request.method == 'POST':
        if 'restore' in request.POST:
            selected = request.POST.getlist('selected')
            for pk in selected:
                user = User.objects.get(pk=int(pk))
                # print(user.name)
                form = CustomUserDeleteForm(request.POST, instance=user)
                if form.is_valid():
                    # form.save()
                    user = form.save()  # 변경
                    user.is_active = True  # 변경
                    user.save()
        if 'back' in request.POST:
            return redirect('/member/member_list/')

    users = User.objects.all().order_by('pk')
    deleted_users = [user for user in users if not user.is_active]
    return render(
        request,
        'admin5.html',
        {
            'users': deleted_users
        }
    )