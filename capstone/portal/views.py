from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from .models import *
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
import pandas as pd
import json
import csv
import datetime
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import Group, Permission

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
        user = authenticate(
            request,
            username=request.POST["employeeId"],
            password=request.POST["password"],
        )
        if user is None:
            return render(
                request, "portal/login.html", {"message": "Invalid ID and/or password"}
            )
        else:
            login(request, user)
            if request.POST["rank"] == "Student":
                return HttpResponseRedirect(reverse("index"))
            else:
                return HttpResponseRedirect(reverse("emp_index"))
    logout(request)
    return render(request, "portal/login.html")


def register_view(request):
    if request.method == "POST":
        if request.POST["password"] == request.POST["confirmation"]:
            try:
                user = User.objects.get(username=request.POST["username"])
            except ObjectDoesNotExist:
                return render(
                    request, "portal/register.html", {"no_user": "ID does not exist"}
                )
            user.set_password(request.POST["password"])
            user.save()
            if request.POST["rank"] == "Student":
                return HttpResponseRedirect(reverse("index"))
            else:
                return HttpResponseRedirect(reverse("emp_index"))
        else:
            return render(
                request, "portal/register.html", {"message": "Passwords do not match"}
            )
    logout(request)
    return render(request, "portal/register.html")


@permission_required("portal.add_user")
@login_required(login_url="login")
@csrf_exempt
def upload_students(request):
    if request.method == "POST":
        file = pd.read_excel(request.body)
        file.to_csv("portal/static/portal/students.csv", index=None, header=True)
        with open("portal/static/portal/students.csv") as file:
            reader = csv.DictReader(file)
            for row in reader:
                latest_student = Student.objects.order_by("-date_joined")[:1]
                try:
                    serial = latest_student[0].username.split("-")
                    id = serial[1]
                except (AttributeError, IndexError):
                    id = 0
                try:
                    match row["course"]:
                        case "B.Sc. Computer Science":
                            id = f'CS-{int(id) + 1}-{datetime.datetime.now().strftime("%y")}'
                        case "B.A. Psychology":
                            id = f'PS-{int(id) + 1}-{datetime.datetime.now().strftime("%y")}'
                        case "B.Ed. Early Childhood Education":
                            id = f'EC-{int(id) + 1}-{datetime.datetime.now().strftime("%y")}'
                        case "B.E. Chemical Engineering":
                            id = f'CE-{int(id) + 1}-{datetime.datetime.now().strftime("%y")}'
                        case "B.B.A. Finance":
                            id = f'FI-{int(id) + 1}-{datetime.datetime.now().strftime("%y")}'
                        case _:
                            return JsonResponse({"error": 912})
                    try:   
                        Student.objects.create(username=id, first_name=row["first_name"], last_name=row["last_name"], 
                                            phone_number=row["phone_number"], national_id=row["nationalID"], 
                                            gender=row["gender"], course=row["course"]
                                            )
                    except IntegrityError:
                        return JsonResponse({"status": 935})
                except KeyError:
                    return JsonResponse({"status": 900})

    return JsonResponse({"status": 200})


@permission_required("portal.add_user")
@login_required(login_url="login")
@csrf_exempt
def register_lecturers(request):
    if request.method == "POST":
        file = pd.read_excel(request.body)
        file.to_csv("portal/static/portal/lecturers.csv", index=None, header=True)
    return JsonResponse(200, safe=False)


@permission_required("portal.add_user")
@login_required(login_url="login")
@csrf_exempt
def register_student(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST method required"})
    else:
        data = json.loads(request.body)
        return JsonResponse(200, safe=False)
