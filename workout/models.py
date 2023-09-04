from django.db import models

import datetime


class Workout(models.Model):
    member_id = models.CharField(max_length=200)
    date = models.DateField()
    workout = models.CharField(max_length=100) # workout's name. bodyweight included
    set = models.IntegerField(default=0)
    weight = models.IntegerField(default=10) # dumbbbell/disk weight
    reps = models.IntegerField(default=10) # reps or timege
    alone_or_group = models.IntegerField(default=0) # alone: 0 / group: 1
    class_pk = models.CharField(max_length=2, default="00")
    completion_rate = models.IntegerField(default=100)

    key_workout_dict = {
        0: "aa",
        1: "ab",
        2: "ac",
        3: "ad",
        4: "ae",
    }

    key_default_reps_dict = {
        0: 10,
        1: 10,
        2: 10,
        3: 10,
        4: 10,
    }

    key_increase_rate_dict = {
        0: 1.1,
        1: 1.1,
        2: 1.1,
        3: 1.1,
        4: 1.1,
    }




    @staticmethod
    def bmi_grade_to_workout_list(bmi_grade): #bmi_grade: 0~5
        # get bmi grade, and return workout list
        # 1~5 set
        # each workout has default weight as 10
        # each workout has default value
        # all workouts are alone

        target_year = str(datetime.datetime.today().year)
        target_month = str(datetime.datetime.today().month)
        target_day = str(datetime.datetime.today().day)
        date = target_year + '-' + target_month + '-' + target_day

        workout_list = []

        for i in range(5):
            workout_key = bmi_grade*5+i
            for j in range(3): # default number of set
                w = Workout.objects.create(
                    member_id="",
                    date=date,
                    workout=Workout.key_workout_dict[workout_key],
                    set=j+1,
                    weight=10, # default weight
                    reps=Workout.key_default_reps_dict[workout_key], # default reps of each workout
                    alone_or_group=0,
                )
                workout_list.append(w)
        return workout_list

    def __str__(self):
        return str(self.date) + ": " + str(self.member_id) + ": " + str(self.workout) + ": " + str(self.set)


class GroupWorkoutClass(models.Model):
    day = models.CharField(max_length=3)
    start_time = models.TimeField(max_length=20)
    end_time = models.TimeField(max_length=20)
    class_pk = models.CharField(max_length=2) # mon:1 ~ fri:5 / 1st:1 ~ 4th:4
    contents = models.CharField(max_length=100, default="") # whatever trainer wants

    def __str__(self):
        return str(self.day) + ": " + str(self.start_time) + ": " + str(self.end_time) + ": " + str(self.class_pk)
