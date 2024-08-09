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
    if request.user.is_superuser:
        return render(request, "administration/hr-index.html")
    elif request.user.groups.contains(Group.objects.get(name="HR")):
        return render(request, "administration/hr-index.html")
    else:
        return render(request, "portal/index.html")


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
            return HttpResponseRedirect(reverse("index"))
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


@permission_required("portal.Student.add_user")
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
                    id = serial[1].strip()
                except (AttributeError, IndexError):
                    id = 0
                try:
                    match row["course"].strip():
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
                            return JsonResponse({"status": 912})
                    try:
                        Student.objects.get(national_id=row["nationalID"])
                        return JsonResponse({"status": 935})
                    except Student.DoesNotExist:
                        try:
                            student = Student.objects.create(
                                username=id,
                                first_name=row["first_name"].strip(),
                                last_name=row["last_name"].strip(),
                                phone_number=row["phone_number"],
                                national_id=row["nationalID"],
                                gender=row["gender"].strip(),
                                course=row["course"].strip(),
                            )
                            student.user_permissions.clear()
                            comrade = Group.objects.get(name="Comrade")
                            student.groups.add(comrade)
                            student.save()
                        except IntegrityError:
                            return JsonResponse({"status": 935})
                except KeyError:
                    return JsonResponse({"status": 900})

    return JsonResponse({"status": 200})


@permission_required("portal.Lecturer.add_user")
@login_required(login_url="login")
@csrf_exempt
def register_lecturers(request):
    if request.method == "POST":
        file = pd.read_excel(request.body)
        file.to_csv("portal/static/portal/lecturers.csv", index=None, header=True)
    return JsonResponse(200, safe=False)


@permission_required("portal.Student.add_user")
@login_required(login_url="login")
@csrf_exempt
def register_student(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST method required"})
    else:
        data = json.loads(request.body)
        print(data)
        latest_student = Student.objects.order_by("-date_joined")[:1]
        try:
            serial = latest_student[0].username.split("-")
            id = serial[1].strip()
        except (AttributeError, IndexError):
            id = 0
        try:
            match data["course"].strip():
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
                    return JsonResponse({"status": 912})
            try:
                Student.objects.get(national_id=data["nationalID"])
                return JsonResponse({"status": 935})
            except Student.DoesNotExist:
                student = Student.objects.create(
                    username=id,
                    first_name=data["first_name"].strip(),
                    last_name=data["last_name"].strip(),
                    phone_number=data["phone_number"],
                    national_id=data["nationalID"].strip(),
                    gender=data["gender"].strip(),
                    course=data["course"].strip(),
                )
                student.user_permissions.clear()
                comrade = Group.objects.get(name="Comrade")
                student.groups.add(comrade)
                student.save()
        except KeyError:
            return JsonResponse({"status": 900})
    return JsonResponse({"status": 200})
