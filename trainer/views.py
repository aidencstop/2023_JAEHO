from django.contrib import auth
from django.contrib.auth import authenticate
from member.models import User
from workout.models import Workout, GroupWorkoutClass
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
import pandas as pd
import os
from django.contrib import messages
from pathlib import Path


@csrf_exempt
def trainer_login(request):
    if request.method == 'POST':
        if 'back' in request.POST:
            return redirect('/')
        if 'login' in request.POST:
            member_id = request.POST['id']
            password = request.POST['password']
            try:
                user = User.objects.get(member_id=member_id)

                if check_password(password, user.password) and user.authority>=1:
                    auth.login(request, user)
                    return redirect('/trainer/trainer_main/', {'user': user})
                elif user.authority<1:
                    messages.error(request, 'You\'re not allowed for trainer menu!', extra_tags='')
                    return redirect('/trainer/login/')
                else:
                    messages.error(request, 'Please enter correct password!', extra_tags='')
                    return redirect('/trainer/login/')
            except Exception:
                messages.error(request, 'Please enter correct ID!', extra_tags='')
                return redirect('/trainer/login/')
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
        if 'back' in request.POST:
            auth.logout(request)
            return redirect('/trainer/trainer_main/')
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
    if request.method == 'POST':
        if 'back' in request.POST:
            auth.logout(request)
            return redirect('/trainer/manage_class/')
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
    workout1_set1 = curr_class_workout_list[0]
    workout1_set2 = curr_class_workout_list[1]
    workout1_set3 = curr_class_workout_list[2]
    workout2_set1 = curr_class_workout_list[3]
    workout2_set2 = curr_class_workout_list[4]
    workout2_set3 = curr_class_workout_list[5]
    workout3_set1 = curr_class_workout_list[6]
    workout3_set2 = curr_class_workout_list[7]
    workout3_set3 = curr_class_workout_list[8]
    return render(request, 'trainer-manage-class-detail-page.html',
                  {
                      'curr_class': curr_class,
                      'curr_class_workout_list': curr_class_workout_list,
                      'workout1_set1': workout1_set1,
                      'workout1_set2': workout1_set2,
                      'workout1_set3': workout1_set3,
                      'workout2_set1': workout2_set1,
                      'workout2_set2': workout2_set2,
                      'workout2_set3': workout2_set3,
                      'workout3_set1': workout3_set1,
                      'workout3_set2': workout3_set2,
                      'workout3_set3': workout3_set3,
                  })

@csrf_exempt
def trainer_member_progress(request):
    if request.method == 'POST':
        if 'back' in request.POST:
            return redirect('/trainer/trainer_main/')

    # 모든 멤버 데려오기
    all_members = User.objects.all().order_by('pk')
    guest_members = [m for m in all_members if m.authority==0]
    # print(guest_members)
    return render(request,
                  'trainer-member-progress-page.html',
            {
                'member_list': guest_members,
            }
    )

@csrf_exempt
def trainer_history_and_progress(request, member_pk):
    if request.method == 'POST':
        if 'back' in request.POST:
            return redirect('/trainer/member_progress/')
    member = User.objects.get(pk=member_pk)
    member_height = member.height
    member_workout_bodyweight_list = Workout.objects.filter(member_id=member.member_id, workout='bodyweight').order_by('date')
    member_date_list = [a.date for a in member_workout_bodyweight_list]
    member_bodyweight_list = [a.reps for a in member_workout_bodyweight_list]

    member_workout_alone_list = Workout.objects.filter(member_id=member.member_id).order_by('date')
    member_workout_alone_list = [w for w in member_workout_alone_list if w.class_pk[0]=='0']
    member_workout_alone_wo_bodyweight_list = [a for a in member_workout_alone_list if a.workout !='bodyweight']
    member_alone_workout_bodyweight_list = Workout.objects.filter(member_id=member.member_id, workout='bodyweight', class_pk='00').order_by('date')
    member_alone_bodyweight_list = [a.reps for a in member_alone_workout_bodyweight_list]
    member_alone_date_list = [a.date for a in member_alone_workout_bodyweight_list]

    expected_bodyweight_list = []

    for idx in range(len(member_alone_date_list)):
        if idx==0:
            prev_bmi_grade = "04"
            prev_bodyweight = int(24.9*((int(member_height)/100.0) ** 2))
        else:
            prev_date = member_alone_date_list[idx-1]
            prev_bodyweight = member_alone_bodyweight_list[idx-1]
            prev_bmi_grade = int(prev_bodyweight) / ((int(member_height)/100.0) ** 2)

        curr_date = member_alone_date_list[idx]

        curr_date_workout_list = [a for a in member_workout_alone_wo_bodyweight_list if a.date==curr_date]
        print(curr_date)
        print(curr_date_workout_list)
        curr_bmi_grade = curr_date_workout_list[0].class_pk
        curr_date_completion_rate_list = [a.completion_rate for a in curr_date_workout_list]
        curr_date_mean_completion_rate = sum(curr_date_completion_rate_list)*1.0/len(curr_date_completion_rate_list)

        trend = 0
        # calculating trend
        if idx<3:
            trend = 0
        else:
            prev_bodyweight_list = member_alone_bodyweight_list[:idx+1]
            growth_rate_list = []
            for i in range(1, idx+1):
                growth_rate_list.append((prev_bodyweight_list[i]-prev_bodyweight_list[i-1])/prev_bodyweight_list[i-1])
            trend = sum(growth_rate_list)/len(growth_rate_list)

        if prev_bmi_grade in ['05', '06', '07', '08']:
            expected_bodyweight = (prev_bodyweight - (curr_date_mean_completion_rate / 1000.0)) * (1+trend)
        else:
            expected_bodyweight = (prev_bodyweight + (curr_date_mean_completion_rate / 1000.0)) * (1+trend)

        expected_bodyweight_list.append(expected_bodyweight)

    real_bodyweight_df = pd.DataFrame(index = member_date_list)
    real_bodyweight_df['bodyweight_real'] = member_bodyweight_list
    expected_bodyweight_df = pd.DataFrame(index = member_alone_date_list)
    expected_bodyweight_df['bodyweight_expected'] = expected_bodyweight_list
    total_df = pd.merge(real_bodyweight_df, expected_bodyweight_df, left_index=True, right_index=True, how='left')
    figure = total_df.plot(kind='line', legend=True, rot=45, fontsize=6).get_figure()

    from pathlib import Path
    # Build paths inside the project like this: BASE_DIR / 'subdir'.
    BASE_DIR = Path(__file__).resolve().parent.parent

    figure.savefig(os.path.join(BASE_DIR, 'static') + "/images/figure.png")

    return render(request, 'trainer-member-history-and-progress-page.html',
                  {
                      'member': member,
                  })