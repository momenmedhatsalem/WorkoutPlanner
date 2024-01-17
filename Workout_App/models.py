from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):


    gender = models.CharField(max_length=20)
    age = models.IntegerField(default=0)
    activity = models.PositiveIntegerField(default=0)
    goal = models.CharField(max_length=20)
    height = models.FloatField(default=0)
    weight = models.FloatField(default=0)
    total_workout_time = models.PositiveIntegerField(default=0)
    workout_number = models.PositiveIntegerField(default=0)
    needed_calories = models.FloatField(default=0)
    bmi = models.FloatField(default=0)
    bmr = models.FloatField(default=0)
    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "gender": self.gender,
            "age": self.age,
            "activity": self.activity,
            "goal": self.goal,
            "height": self.height,
            "weight": self.weight,
            "weight": self.weight,
            "total_workout_time": self.total_workout_time,
            "workout_number": self.workout_number,
            "needed_calories": self.needed_calories,
            "bmi": self.bmi,
            "bmr": self.bmr
            }







    pass
class Exercise(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=200, default="")
    bodypart = models.CharField(max_length=20)
    equipment = models.CharField(max_length=20)
    gifUrl  = models.CharField(max_length=200)
    targetmuscle  = models.CharField(max_length=20)


    def create (self, name, bodypart, equipment, gifUrl, targetmuscle, description):

        self.name = name
        self.description = description
        self.bodypart = bodypart
        self.equipment = equipment
        self.gifUrl = gifUrl
        self.targetmuscle = targetmuscle
        self.save()


class Training(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=2000, default="")
    gifUrl  = models.CharField(max_length=200)
    targetmuscle  = models.CharField(max_length=200)
    calories = models.FloatField(default=0)
    reps = models.PositiveIntegerField(default=0)
    duration = models.PositiveIntegerField(default=0)


class Workout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="workouts")
    Id = models.ForeignKey(Training, on_delete=models.CASCADE, related_name="workout_id", default=1)
    date = models.DateField()
    time = models.TimeField()
    sets = models.PositiveIntegerField()
    reps = models.PositiveIntegerField()
    duration = models.PositiveIntegerField()
    calories = models.PositiveIntegerField()

class Food(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="foods")
    date = models.DateField()
    time = models.TimeField()
    food = models.CharField(max_length=20)
    calories = models.PositiveIntegerField()
