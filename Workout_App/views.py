from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import (
    HttpResponse,
    HttpResponseRedirect,
    Http404,
    HttpResponseBadRequest,
)
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.forms import TextInput, FloatField, NumberInput
from django.contrib.auth.decorators import login_required
from .models import User, Exercise, Training
import re
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
import json
import requests
from django.http import JsonResponse
from django.core.paginator import Paginator


@login_required(login_url="login")
def index(request):

    """
    url1 = "https://exercisedb.p.rapidapi.com/exercises/equipment/body weight"

    headers1 = {
	"content-type": "application/octet-stream",
	"X-RapidAPI-Key": "b84e9736b1mshb31f7b5ac63e0b4p10780djsn852923eec100",
	"X-RapidAPI-Host": "exercisedb.p.rapidapi.com"
    }

    bodyweightexercises  = requests.get(url1, headers=headers1)
    url = "https://exercisedb.p.rapidapi.com/exercises/bodyPart/upper arms"

    headers = {
	"content-type": "application/octet-stream",
	"X-RapidAPI-Key": "b84e9736b1mshb31f7b5ac63e0b4p10780djsn852923eec100",
	"X-RapidAPI-Host": "exercisedb.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)
    """
    user = User.objects.get(pk=request.user.id)

    
    
    return render(
        request,
        "index.html",
        {"mainexercises": "page_objects", "fullexercises": "response.json()", "size": "SIZE", "state": "Active Listings"}
    )


@login_required(login_url="login")
def closed(request):

    return render(
        request,
        "index.html",
        {

            "state": "Closed Listings",
            "size": "SIZE",
        },
    )
    


def login_view(request):
    global user_id
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "register.html", {"message": "Passwords must match."}
            )
        # User data
        age = request.POST["age"]

        gender = request.POST["gender"]
        height = request.POST["height"]
        weight = request.POST["weight"]
        goal = request.POST["goal"]
        activity = request.POST["activity"]
        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.age = age
            user.gender = gender
            user.height = height
            user.weight = weight
            user.goal = goal
            user.activity = activity
            user.save()
            id = user.id
            calculate_health_data(user.id)
        except IntegrityError:
            return render(
                request,
                "register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        
        return render(request, "register.html" )

def profile(request, username, operation=0):
    user = User.objects.get(pk=request.user.id)
    if operation == 1:
        calculate_health_data(user.id)
        return JsonResponse({"user": user.serialize()})
    
    fitness_data = calculate_health_data(user.id)
    return render(request, "profile.html",  {"user": user, "fitness": fitness_data})

def calculate_health_data(id):
    
    user = User.objects.get(pk=id)
    age = user.age
    height = user.height
    weight = user.weight
    gender = user.gender
    activity_rate = user.activity
    # Calculate BMI
    bmi = round(weight / ((height / 100) ** 2), 1)

    # Calculate BMR
    if gender == 'm':
        bmr = round(88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age), 1)
    else:
        bmr = round(447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age), 1)

    # Calculate daily caloric needs based on activity level
    activity_factors = {1: 1.2, 2: 1.375, 3: 1.55, 4: 1.725, 5: 1.9}
    calories = round(bmr * activity_factors[activity_rate], 1)
    user.bmi = bmi
    user.bmr = bmr
    user.calories = calories
    user.save()
    return {'BMI': bmi, 'BMR': bmr, 'Calories': calories}

def start_workout(request):
    # Renders muscle, exercise

    exercises = Training.objects.all()
    paginator = Paginator(exercises, 1)
    page_number = request.GET.get('page')
    leng = len(exercises)
    page_objects = paginator.get_page(page_number)
    return render(request, "workout.html", {"exercises": page_objects})

def loader(request):
    url3 = "https://exercisedb.p.rapidapi.com/exercises"

    headers3 = {
        "content-type": "application/octet-stream",
        "X-RapidAPI-Key": "b84e9736b1mshb31f7b5ac63e0b4p10780djsn852923eec100",
        "X-RapidAPI-Host": "exercisedb.p.rapidapi.com"
    }

    allexercises  = requests.get(url3, headers=headers3)

    data = allexercises.json()
    for item in data:

        name =  item.get("name")
        bodypart = item.get("bodyPart")
        equipment = item.get("equipment")
        gif = item.get("gifUrl")
        target = item.get("target")
        exercise = Exercise.objects.create( name=name, bodypart=bodypart, equipment=equipment, gifUrl=gif, targetmuscle=target, description="")
        exercise.save()
    return render(request, "new.html")

@csrf_exempt
def edit(request, parameter):
    user = User.objects.get(pk=request.user.id)
    

    
    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("new_edit") is not None:
            if parameter == "age":
                user.age = data["new_edit"]
            elif parameter == "height":
                user.height = data["new_edit"]
            elif parameter == "weight":
                user.weight = data["new_edit"]
        user.save()
        calculate_health_data(user.id)
        return HttpResponse(status=204)
    # Post must be via PUT
    else:
        return JsonResponse({
            "error": "PUT request required."
        }, status=400)    
    pass

@csrf_exempt
def workout_saver(request):
    if request.method == "POST":
        time = request.POST["timed"]
        return HttpResponse(status=204)
        pass