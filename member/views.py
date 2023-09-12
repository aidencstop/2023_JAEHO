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
import pandas as pd
import matplotlib


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
            today_year = str(datetime.datetime.today().year)
            today_month = str(datetime.datetime.today().month)
            today_day = str(datetime.datetime.today().day)
            today = datetime.date(year=int(today_year), month=int(today_month), day=int(today_day))
            today_workout_record_list = Workout.objects.filter(date=today)
            if len(today_workout_record_list)>0:
                #TODO: 여기에 오늘 운동 이미 정해졌으니 record로 가라는 메시지
                pass
            else:
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

            # 오늘 몸무게 기록 가져오기
            today_bodyweight_record = Workout.objects.filter(date=last_date, workout='bodyweight')

            # 오늘 운동 기록 있고, 몸무게 기록 없으면 record 페이지로 이동
            if today == last_date and len(today_bodyweight_record)==0:
                return redirect('/member/record/')
            # 오늘 운동 기록 있고, 몸무게 기록 있으면 이동 불가
            elif today == last_date and len(today_bodyweight_record)>0:
            # TODO: 메시지 띄우기
                pass
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
    member = auth.get_user(request)
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
    figure = total_df.plot(kind='line', legend=True).get_figure()

    from pathlib import Path
    # Build paths inside the project like this: BASE_DIR / 'subdir'.
    BASE_DIR = Path(__file__).resolve().parent.parent

    figure.savefig(os.path.join(BASE_DIR, 'static') + "/image/figure.png")

    return render(request, 'member-history-and-progress-page.html')

@csrf_exempt
def member_start_workout(request):
    if request.method == 'POST':
        if 'back' in request.POST:
            return redirect('/member/member_main/')

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
                #TODO: 여기에 message 추가(오늘 이미 group 운동을 했다는 내용)
                pass
            elif today == last_date and alone_or_group == 0:
                #TODO: 여기에 message 추가(오늘 이미 개인 운동을 했다는 내용)
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
                #TODO: 여기에 message 추가(오늘 이미 개인 운동을 했다는 내용)
                pass
            elif today == last_date and alone_or_group == 1:
                #TODO: 여기에 message 추가(오늘 이미 group 운동을 했다는 내용)
                pass
            else:
                return redirect('/member/start_workout_group/')
    return render(request, 'member-start-workout-page.html')

@csrf_exempt
def member_start_workout_alone(request):
    def bmi_to_class_pk(bmi):
        if bmi<16.0:
            return "01"
        elif bmi<17.0:
            return "02"
        elif bmi<18.5:
            return "03"
        elif bmi<25:
            return "04"
        elif bmi<27.5:
            return "05"
        elif bmi<30.0:
            return "06"
        elif bmi<35:
            return "07"
        else:
            return "08"
    def completion_rate_increment(reps, completion_rate):
        increased_reps = reps
        if 95 <= completion_rate <= 100:
            increased_reps = reps + 2
        elif 80 <= completion_rate < 95:
            increased_reps = reps + 1
        elif 65 <= completion_rate < 80:
            # increased_reps = reps
            pass
        elif 50 <= completion_rate < 65:
            # increased_reps = reps
            pass
        else:
            # increased_reps = reps
            pass
        return increased_reps

    if request.method == 'POST':
        if 'logout' in request.POST:
            auth.logout(request)
            return redirect('/')

    # 오늘 날짜 정보
    target_year = str(datetime.datetime.today().year)
    target_month = str(datetime.datetime.today().month)
    target_day = str(datetime.datetime.today().day)

    # 최종적으로 추천해줄 운동 리스트
    recommended_workout_list = []

    # 유저 정보 불러오기
    user = auth.get_user(request)

    # 유저 키 가져오기
    user_height = user.height

    # 유저 몸무게 가져오기
    user_bodyweight_workout_list = Workout.objects.filter(member_id=user.member_id, workout='bodyweight').order_by('date')
    user_bodyweight_list = [int(wo.reps) for wo in user_bodyweight_workout_list]
    user_alone_bodyweight_workout_list = Workout.objects.filter(member_id=user.member_id, workout='bodyweight', class_pk='00').order_by('date')
    user_alone_bodyweight_list = [int(wo.reps) for wo in user_alone_bodyweight_workout_list]

    # BMI 기반 class pk 산출
    default_bmi_class_pk = "04"
    if len(user_alone_bodyweight_list)==0:
        if len(user_bodyweight_list)==0:
            print('case 1')
            bmi_class_pk = default_bmi_class_pk
            class_pk_workout_list = Workout.objects.filter(member_id='0000', class_pk=bmi_class_pk).order_by('workout', 'set')
            print(len(class_pk_workout_list))
            for class_pk_workout in class_pk_workout_list:
                newly_created_workout = Workout.objects.create(
                    member_id=user.member_id,
                    date=target_year + '-' + target_month + '-' + target_day,
                    workout=class_pk_workout.workout,
                    set=class_pk_workout.set,
                    weight=class_pk_workout.weight,
                    reps=class_pk_workout.reps,
                    alone_or_group=class_pk_workout.alone_or_group,
                    class_pk=class_pk_workout.class_pk,
                )
                recommended_workout_list.append(newly_created_workout)
            print("default")
            print(len(recommended_workout_list))
        else:
            print('case 2')
            curr_user_bodyweight = user_bodyweight_list[-1]
            curr_bmi = int(curr_user_bodyweight) / ((int(user_height)/100.0) ** 2)
            curr_bmi_class_pk = bmi_to_class_pk(curr_bmi)

            bmi_class_pk = curr_bmi_class_pk
            class_pk_workout_list = Workout.objects.filter(member_id='0000', class_pk=bmi_class_pk).order_by('workout', 'set')
            print(len(class_pk_workout_list))
            for class_pk_workout in class_pk_workout_list:
                newly_created_workout = Workout.objects.create(
                    member_id=user.member_id,
                    date=target_year + '-' + target_month + '-' + target_day,
                    workout=class_pk_workout.workout,
                    set=class_pk_workout.set,
                    weight=class_pk_workout.weight,
                    reps=class_pk_workout.reps,
                    alone_or_group=class_pk_workout.alone_or_group,
                    class_pk=class_pk_workout.class_pk,
                )
                recommended_workout_list.append(newly_created_workout)
            print("1 bodyweight")
            print(len(recommended_workout_list))

    elif len(user_alone_bodyweight_list)==1:
        print('case 3')
        curr_user_bodyweight = user_alone_bodyweight_list[-1]
        curr_bmi = int(curr_user_bodyweight) / ((int(user_height)/100.0) ** 2)
        curr_bmi_class_pk = bmi_to_class_pk(curr_bmi)

        bmi_class_pk = curr_bmi_class_pk
        class_pk_workout_list = Workout.objects.filter(member_id='0000', class_pk=bmi_class_pk).order_by('workout', 'set')
        print(len(class_pk_workout_list))
        for class_pk_workout in class_pk_workout_list:
            newly_created_workout = Workout.objects.create(
                member_id=user.member_id,
                date=target_year + '-' + target_month + '-' + target_day,
                workout=class_pk_workout.workout,
                set=class_pk_workout.set,
                weight=class_pk_workout.weight,
                reps=class_pk_workout.reps,
                alone_or_group=class_pk_workout.alone_or_group,
                class_pk=class_pk_workout.class_pk,
            )
            recommended_workout_list.append(newly_created_workout)
        print("1 bodyweight")
        print(len(recommended_workout_list))

    else:
        print('case 4')

        curr_user_alone_bodyweight = user_alone_bodyweight_list[-1]
        curr_bmi = int(curr_user_alone_bodyweight) / ((int(user_height)/100.0) ** 2)
        curr_bmi_class_pk = bmi_to_class_pk(curr_bmi)
        prev_user_alone_bodyweight = user_alone_bodyweight_list[-2]
        prev_bmi = int(prev_user_alone_bodyweight) / ((int(user_height)/100.0) ** 2)
        prev_bmi_class_pk = bmi_to_class_pk(prev_bmi)

        if prev_bmi_class_pk != curr_bmi_class_pk:
            class_pk_workout_list = Workout.objects.filter(member_id='0000', class_pk=curr_bmi_class_pk).order_by('workout', 'set')
            print(len(class_pk_workout_list))
            for class_pk_workout in class_pk_workout_list:
                newly_created_workout = Workout.objects.create(
                    member_id=user.member_id,
                    date=target_year + '-' + target_month + '-' + target_day,
                    workout=class_pk_workout.workout,
                    set=class_pk_workout.set,
                    weight=class_pk_workout.weight,
                    reps=class_pk_workout.reps,
                    alone_or_group=class_pk_workout.alone_or_group,
                    class_pk=class_pk_workout.class_pk,
                )
                recommended_workout_list.append(newly_created_workout)
            print("curr bmi class pk: "+curr_bmi_class_pk)
            print(len(recommended_workout_list))

        else:
            print('case 5')

            member_workout_list = Workout.objects.filter(member_id=user.member_id, alone_or_group=0).order_by('date', 'workout', 'set')
            # bodyweight 기록은 어차피 alone_or_group이 0이어서 빼줌
            member_workout_wo_bodyweight_list = [wo for wo in member_workout_list if wo.workout!='bodyweight']
            member_last_workout_date = max([wo.date for wo in member_workout_wo_bodyweight_list])
            member_last_workout_wo_bodyweight_list = [wo for wo in member_workout_wo_bodyweight_list if wo.date==member_last_workout_date]
            for member_last_workout in member_last_workout_wo_bodyweight_list:
                newly_created_workout = Workout.objects.create(
                    member_id=user.member_id,
                    date=target_year + '-' + target_month + '-' + target_day,
                    workout=member_last_workout.workout,
                    set=member_last_workout.set,
                    weight=member_last_workout.weight,
                    reps=completion_rate_increment(member_last_workout.reps, member_last_workout.completion_rate),
                    alone_or_group=member_last_workout.alone_or_group,
                    class_pk=member_last_workout.class_pk,
                )
                recommended_workout_list.append(newly_created_workout)
            print("curr bmi class pk: "+curr_bmi_class_pk)
            print(len(recommended_workout_list))

    recommended_workout_dictionary = {}
    for rw in recommended_workout_list:
        if rw.workout in recommended_workout_dictionary.keys():
            recommended_workout_dictionary[rw.workout]['set'].append(rw.set)
            recommended_workout_dictionary[rw.workout]['weight'].append(rw.weight)
            recommended_workout_dictionary[rw.workout]['reps'].append(rw.reps)
        else:
            recommended_workout_dictionary[rw.workout]={'set':[], 'weight':[], 'reps':[]}
            recommended_workout_dictionary[rw.workout]['set'].append(rw.set)
            recommended_workout_dictionary[rw.workout]['weight'].append(rw.weight)
            recommended_workout_dictionary[rw.workout]['reps'].append(rw.reps)
    print(recommended_workout_dictionary.keys())
    recommended_workout = recommended_workout_dictionary.keys()
    return render(request, 'member-start-workout-alone-recommend-page.html', {'recommended_workout': recommended_workout,'recommended_workout_dictionary':recommended_workout_dictionary,})

@csrf_exempt
def member_start_workout_group(request):
    if request.method == 'POST':
        if 'logout' in request.POST:
            auth.logout(request)
            return redirect('/')
    # 그 중 종료 시간이 현재시간 이전인 것을 클릭 불가능
    # 클릭 가능한 class를 누르면 해당 클래스 상세 페이지로 넘어감
    # if request.method == 'POST':

    # class 중 오늘의 요일에 해당하는 class들을 남김
    all_group_workout_class = GroupWorkoutClass.objects.all().order_by('class_pk')
    weekday = str(datetime.datetime.today().weekday()+1) # datetime.datetime.today().weekday(): monday=0~sunday=6
    weekday_group_workout_class = []

    for gwc in all_group_workout_class:
        print(type(gwc.class_pk))
        if gwc.class_pk[0]==weekday:
            weekday_group_workout_class.append(gwc)
    # print(datetime.datetime.today())
    weekday_group_workout = []
    all_workout = Workout.objects.all().order_by('class_pk',  'workout', 'set')

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
        if 'back' in request.POST:
            return redirect('/member/member_main/')
        if 'save' in request.POST:
            # 유저 정보를 불러옴
            user = auth.get_user(request)

            # 오늘 일자를 가져옴
            target_year = str(datetime.datetime.today().year)
            target_month = str(datetime.datetime.today().month)
            target_day = str(datetime.datetime.today().day)

            tmp_member_last_date_workout = member_last_date_workouts_wo_bodyweight[-1]

            bodyweight_class_pk = "10"
            if tmp_member_last_date_workout.class_pk[0]=='0':
                bodyweight_class_pk = "00"

            bodyweight = request.POST['bodyweight'] # type: str
            Workout.objects.create(
                member_id=user.member_id,
                date=target_year + '-' + target_month + '-' + target_day,
                workout="bodyweight",
                set=0,
                weight=0,
                reps=int(bodyweight),
                alone_or_group=0,
                class_pk=bodyweight_class_pk,
            )

            workout_list = request.POST.getlist('workout')
            set_list = request.POST.getlist('set')
            set_list = [int(a) for a in set_list]
            weight_list = request.POST.getlist('weight')
            weight_list = [int(a) for a in weight_list]
            reps_list = request.POST.getlist('reps')
            reps_list = [int(a) for a in reps_list]
            print(len(workout_list))
            asdf = zip(workout_list, set_list, weight_list, reps_list)
            for i in asdf:
                print(i)

            for idx in range(len(member_last_date_workouts_wo_bodyweight)):
                curr_record = member_last_date_workouts_wo_bodyweight[idx]
                curr_record.workout=workout_list[idx]
                curr_record.set = set_list[idx]
                curr_record.weight = weight_list[idx]
                curr_record.completion_rate = int(reps_list[idx]*100.0 / curr_record.reps)
                curr_record.reps = reps_list[idx]
                curr_record.save()

            print(member_last_date_workouts_wo_bodyweight)



            return redirect('/member/member_main/')

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
    #TODO: 시간에 따라 ok / nope 나누어야 함
    if request.method == 'POST':
        if 'logout' in request.POST:
            auth.logout(request)
            return redirect('/')
        if 'ok' in request.POST:
            #TODO: create workout for selected class for curr user

            # 유저 정보를 불러옴
            user = auth.get_user(request)

            # 오늘 일자를 가져옴
            target_year = str(datetime.datetime.today().year)
            target_month = str(datetime.datetime.today().month)
            target_day = str(datetime.datetime.today().day)

            newly_created_workout_list = []
            class_pk_workout_list = Workout.objects.filter(class_pk=class_pk).order_by('workout', 'set')
            print(len(class_pk_workout_list))
            for class_pk_workout in class_pk_workout_list:
                newly_created_workout = Workout.objects.create(
                    member_id=user.member_id,
                    date=target_year + '-' + target_month + '-' + target_day,
                    workout=class_pk_workout.workout,
                    set=class_pk_workout.set,
                    weight=class_pk_workout.weight,
                    reps=class_pk_workout.reps,
                    alone_or_group=class_pk_workout.alone_or_group,
                    class_pk=class_pk_workout.class_pk,
                )
                newly_created_workout_list.append(newly_created_workout)
            print(len(newly_created_workout_list))
            return redirect('/member/member_main/')
        if 'cancel' in request.POST:
            return redirect('/member/start_workout_group/')

    all_group_workout_class = GroupWorkoutClass.objects.all().order_by('class_pk')
    selected_group_workout_class = None
    for gwc in all_group_workout_class:
        if class_pk==gwc.class_pk:
            selected_group_workout_class=gwc

    today_month = datetime.datetime.today().month
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
        'member-start-workout-group-booked-page.html',
        {
            'monthday': monthday,
            'selected_group_workout_class': selected_group_workout_class
        }
    )