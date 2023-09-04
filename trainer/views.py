from django.contrib import auth
from django.contrib.auth import authenticate
from member.models import User
from workout.models import Workout, GroupWorkoutClass
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
    if request.method == 'POST':
        if 'logout' in request.POST:
            auth.logout(request)
            return redirect('/')
    #요일별 클래스 리스트 만들기
    monday_class_list = []
    tuesday_class_list = []
    wednesday_class_list = []
    thursday_class_list = []
    friday_class_list = []

    all_classes = GroupWorkoutClass.objects.all().order_by('class_pk')
    for gwc in all_classes:
        if gwc.class_pk[0]=='1':
            monday_class_list.append(gwc)
        elif gwc.class_pk[0]=='2':
            tuesday_class_list.append(gwc)
        elif gwc.class_pk[0]=='3':
            wednesday_class_list.append(gwc)
        elif gwc.class_pk[0]=='4':
            thursday_class_list.append(gwc)
        elif gwc.class_pk[0]=='5':
            friday_class_list.append(gwc)

    return render(request, 'trainer-manage-class-page.html',
                  {
                      'monday_class_list': monday_class_list,
                      'tuesday_class_list': tuesday_class_list,
                      'wednesday_class_list': wednesday_class_list,
                      'thursday_class_list': thursday_class_list,
                      'friday_class_list': friday_class_list,
                  },
                  )

@csrf_exempt
def trainer_manage_class_detail(request, class_pk):
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

    curr_class = GroupWorkoutClass.objects.get(class_pk=class_pk)
    curr_class_workout_list = []
    all_workouts = Workout.objects.all().order_by('class_pk', 'workout')
    for workout in all_workouts:
        if workout.class_pk == str(class_pk):
            curr_class_workout_list.append(workout)
    print(curr_class.pk)
    print(len(curr_class_workout_list))
    return render(request, 'trainer-manage-class-detail-page.html',
                  {
                      'curr_class': curr_class,
                      'curr_class_workout_list': curr_class_workout_list
                  })

@csrf_exempt
def trainer_member_progress(request):
    if request.method == 'POST':
        if 'logout' in request.POST:
            auth.logout(request)
            return redirect('/')

    # 모든 멤버 데려오기
    all_members = User.objects.all().order_by('pk')

    return render(request,
                  'trainer-member-progress-page.html',
            {
                'member_list': all_members
            }
    )

@csrf_exempt
def trainer_history_and_progress(request, member_pk):
    if request.method == 'POST':
        if 'back' in request.POST:
            return redirect('/trainer/member_progress/')
    member = User.objects.get(pk=member_pk)
    #TODO: 여기 그래프 구현해야 함
    return render(request,
                  'trainer-member-history-and-progress-page.html',
                  {
                      'member': member
                  },
    )
