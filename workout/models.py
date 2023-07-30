from django.db import models


class Workout(models.Model):
    member_id = models.CharField(max_length=200)
    date = models.DateField()
    workout = models.CharField(max_length=20)
    set = models.IntegerField(default=5)
    weight = models.IntegerField(max_length=200)
    value = models.IntegerField(max_length=200)
    category = models.IntegerField(max_length=1)

    def __str__(self):
        return str(self.date) + ": " + str(self.member_id)
