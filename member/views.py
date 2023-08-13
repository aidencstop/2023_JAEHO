from django.contrib import auth
from django.contrib.auth import authenticate
from .models import User
from workout.models import Workout, GroupWorkoutClass
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .forms import CustomUserChangeForm, CustomUserDeleteForm, AdminLoginForm
from django.contrib.auth.hashers import check_password
import datetime
import calendar

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
        if 'logout' in request.POST:
            auth.logout(request)
            return redirect('/')

        if 'history_and_progress' in request.POST:

            return redirect('/member/history_and_progress/')
        if 'start_workout' in request.POST:

            return redirect('/member/start_workout/')
        if 'record' in request.POST:
            # 유저의 마지막 운동 기록으로부터 마지막 운동 일자 추출
            user = auth.get_user(request)
            all_workouts = Workout.objects.all().order_by('date')
            user_workouts = [a for a in all_workouts if a.member_id == user.member_id]
            last_date = user_workouts[-1].date  # type: datetime.date
            
            # 오늘 날짜 산출
            today_year = str(datetime.datetime.today().year)
            today_month = str(datetime.datetime.today().month)
            today_day = str(datetime.datetime.today().day)
            today = datetime.date(year=int(today_year), month=int(today_month), day=int(today_day))

            # 오늘 운동 기록 있으면 record 페이지로 이동
            if today == last_date:
                return redirect('/member/record/')
            # 오늘 운동 기록 없으면 이동 불가
            else:
                #TODO: 메시지 띄우기
                pass

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
        if 'logout' in request.POST:
            auth.logout(request)
            return redirect('/')
        if 'start_workout_alone' in request.POST:
            # 오늘 이미 group workout을 한 record가 있으면 열리지 않아야 함
            user = auth.get_user(request)
            all_workouts = Workout.objects.all().order_by('date')
            user_workouts = [a for a in all_workouts if a.member_id == user.member_id]
            last_date = user_workouts[-1].date  # type: datetime.date
            member_last_date_workouts = [a for a in user_workouts if a.workout != 'bodyweight']
            alone_or_group = member_last_date_workouts[-1].alone_or_group
            today_year = str(datetime.datetime.today().year)
            today_month = str(datetime.datetime.today().month)
            today_day = str(datetime.datetime.today().day)

            today = datetime.date(year=int(today_year), month=int(today_month), day=int(today_day))
            if today == last_date and alone_or_group == 1:
                #TODO: 여기에 message 추가 가능
                pass
            else:
                return redirect('/member/start_workout_alone/')

        if 'start_workout_group' in request.POST:
            user = auth.get_user(request)
            all_workouts = Workout.objects.all().order_by('date')
            user_workouts = [a for a in all_workouts if a.member_id == user.member_id]
            last_date = user_workouts[-1].date # type: datetime.date
            member_last_date_workouts = [a for a in user_workouts if a.workout!='bodyweight']
            alone_or_group=member_last_date_workouts[-1].alone_or_group
            today_year = str(datetime.datetime.today().year)
            today_month = str(datetime.datetime.today().month)
            today_day = str(datetime.datetime.today().day)

            today = datetime.date(year=int(today_year), month=int(today_month), day=int(today_day))
            if today==last_date and alone_or_group==0:
                # TODO: 여기에 message 추가 가능
                pass
            else:
                return redirect('/member/start_workout_group/')
    return render(request, 'member-start-workout-page.html')

@csrf_exempt
def member_start_workout_alone(request):
    if request.method == 'POST':
        if 'logout' in request.POST:
            auth.logout(request)
            return redirect('/')
    user = auth.get_user(request)
    all_workouts = Workout.objects.all().order_by('date')
    user_workouts = [a for a in all_workouts if a.member_id == user.member_id]
    # 운동기록 0개, 1개, 2개 이상 경우 나누기
    # date로 하면 됨



    last_date = user_workouts[-1].date  # type: datetime.date
    member_last_date_workouts_wo_bodyweight = [a for a in user_workouts if a.workout != 'bodyweight' and a.date==last_date]
    member_last_date_workouts = [a for a in user_workouts if a.date==last_date]
    alone_or_group = member_last_date_workouts_wo_bodyweight[-1].alone_or_group

    today_year = str(datetime.datetime.today().year)
    today_month = str(datetime.datetime.today().month)
    today_day = str(datetime.datetime.today().day)
    today = datetime.date(year=int(today_year), month=int(today_month), day=int(today_day))

    if today == last_date and alone_or_group == 0:
        # 오늘의 운동 기록이 이미 있으면 그냥 그걸 보여주면 됨
        # member_last_date_workouts_wo_bodyweight를 넘겨주면 됨
        pass

    return render(request, 'member-start-workout-alone-page.html')

@csrf_exempt
def member_start_workout_group(request):
    #TODO: 로그아웃 구현해야함

    # 그 중 종료 시간이 현재시간 이전인 것을 클릭 불가능
    # 클릭 가능한 class를 누르면 해당 클래스 상세 페이지로 넘어감
    if request.method == 'POST':
        if "book_now" in request.POST:
            #TODO: 여기에 class_pk를 전달받아서 url에 입력할 방법
            return redirect('/member/start_workout_group_booked/')

    # class 중 오늘의 요일에 해당하는 class들을 남김
    all_group_workout_class = GroupWorkoutClass.objects.all().order_by('class_pk')
    weekday = str(datetime.datetime.today().weekday()+1) # datetime.datetime.today().weekday(): monday=0~sunday=6
    weekday_group_workout_class = []
    for gwc in all_group_workout_class:
        if gwc.class_pk[0]==weekday:
            weekday_group_workout_class.append(gwc)
    # print(datetime.datetime.today())
    # print(weekday)

    weekday_group_workout = []
    all_workout = Workout.objects.all().order_by('class_pk')

    dictionary_list = []
    for i in range(1, 5):
        workout_list = []
        class_pk = weekday + str(i)
        for workout in all_workout:
            if workout.class_pk == class_pk:
                workout_list.append(workout)
        dictionary_list.append({'class': weekday_group_workout_class[i-1],
                'workout_list': workout_list
            }
        )

    # print(dictionary_list)

    return render(
        request,
        'member-start-workout-group-page.html',
        {
            'dictionary_list': dictionary_list,
        }
    )


@csrf_exempt
def member_record(request):
    user = auth.get_user(request)
    all_workouts = Workout.objects.all().order_by('date', 'member_id', 'workout', 'set')
    user_workouts = [a for a in all_workouts if a.member_id == user.member_id]
    last_date = user_workouts[-1].date  # type: datetime.date
    member_last_date_workouts_wo_bodyweight = [a for a in user_workouts if a.workout != 'bodyweight' and a.date==last_date]

    if request.method == 'POST':
        if 'logout' in request.POST:
            auth.logout(request)
            return redirect('/')

        #TODO: html에서 input으로 바꾸어야함
        #TODO: save로 변경사항 저장되도록



    return render(
        request,
        'member-record-page.html',
        {
            'workout_list': member_last_date_workouts_wo_bodyweight
        }
    )

@csrf_exempt
def member_start_workout_group_booked(request, class_pk):
    all_group_workout_class = GroupWorkoutClass.objects.all().order_by('class_pk')
    selected_group_workout_class = None
    for gwc in all_group_workout_class:
        if class_pk==gwc.class_pk:
            selected_group_workout_class=gwc


    today_month = str(datetime.datetime.today().month)
    month = calendar.month_name[today_month]
    today_day = str(datetime.datetime.today().day)
    day = '00'
    if today_day == 1:
        day = str(today_day) + 'st'
    elif today_day == 2:
        day = str(today_day) + 'nd'
    elif today_day == 3:
        day = str(today_day) + 'rd'
    else:
        day = str(today_day) + 'th'

    monthday = month + " " + day

    return render(
        request,
        'member-record-page.html',
        {
            'monthday': monthday,
            'selected_group_workout_class': selected_group_workout_class
        }
    )