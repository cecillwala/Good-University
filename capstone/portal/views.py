from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *
from django.core.exceptions import ObjectDoesNotExist
import pandas as pd
import csv
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

@login_required(login_url="login")
def index(request):
    return render(request, "portal/index.html")


@login_required(login_url="login")
def emp_index(request):
    return render(request, "administration/ass-index.html")


def login_view(request):
    if request.method == "POST":
        print(request.POST)
        user = authenticate(request, username=request.POST["employeeId"], password=request.POST["password"])
        if user is None:
           return render(request, "portal/login.html", {
               "message": "Invalid ID and/or password"
           })
        else:
            login(request, user)
            if request.POST["rank"] == "Student":
                return HttpResponseRedirect(reverse("index"))
            else:
                return HttpResponseRedirect(reverse("emp_index"))
    return render(request, "portal/login.html")


def register_view(request):
    if request.method == 'POST':
        if request.POST["password"] == request.POST["confirmation"]:
            try:
                user = User.objects.get(username=request.POST["username"])
            except ObjectDoesNotExist:
                return render(request, "portal/register.html", {
                    "no_user": "ID does not exist"
                })
            user.set_password(request.POST["password"])
            user.save()
            if request.POST["rank"] == "Student":
                return HttpResponseRedirect(reverse("index"))
            else:
                return HttpResponseRedirect(reverse("emp_index"))
        else:
            return render(request, "portal/register.html", {
                "message": "Passwords do not match"
            })
    logout(request)
    return render(request, "portal/register.html")


@login_required(login_url="login")
@csrf_exempt
def upload_students(request):
    if request.method == 'POST':
        file = pd.read_excel(request.body)
        file.to_csv("portal/static/portal/test.csv", index=None, header=True) 
    return JsonResponse({"status": 200})