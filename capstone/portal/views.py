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
from django.contrib.auth.models import Group


# Create your views here.
@login_required(login_url="login")
def index(request):
    if request.user.is_superuser:
        return render(request, "administration/index.html")
    elif request.user.groups.contains(Group.objects.get(name="HR")):
        return render(request, "administration/hr-index.html")
    else:
        return render(request, "portal/index.html")


def login_view(request):
    if request.method == "POST":
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
                try:
                    latest_student = Student.student.latest("date_joined")
                    serial = latest_student.username.split("-")
                    id = serial[1].strip()
                except (Student.DoesNotExist, IndexError):
                    id = 0
                try:
                    match row["faculty"].strip():
                        case "LAW":
                            id = f'LL-{int(id) + 1}-{datetime.datetime.now().strftime("%y")}'
                        case "PHY_SCI":
                            id = f'PS-{int(id) + 1}-{datetime.datetime.now().strftime("%y")}'
                        case "EDU":
                            id = f'EDU-{int(id) + 1}-{datetime.datetime.now().strftime("%y")}'
                        case "SOC_SCI":
                            id = f'SC-{int(id) + 1}-{datetime.datetime.now().strftime("%y")}'
                        case "BUS":
                            id = f'BU-{int(id) + 1}-{datetime.datetime.now().strftime("%y")}'
                        case "HEALTH_SCI":
                            id = f'HS-{int(id) + 1}-{datetime.datetime.now().strftime("%y")}'
                        case _:
                            return JsonResponse({"status": 912})
                    try:
                        Student.student.create(
                            username=id,
                            first_name=row["first_name"].strip(),
                            last_name=row["last_name"].strip(),
                            phone_number=row["phone_number"],
                            national_id=row["nationalID"],
                            gender=row["gender"].strip(),
                            faculty=Faculty.objects.get(faculty=row["faculty"].strip()),
                            course=Course.objects.get(course=row["course"].strip())
                        )
                        # student.user_permissions.clear()
                        # comrade = Group.objects.get(name="Comrade")
                        # student.groups.add(comrade)
                        # student.save()
                    except IntegrityError:
                        return JsonResponse({"status": 935})
                except KeyError:
                    return JsonResponse({"status": 900})
        return JsonResponse({"status": 200})
    else:
        return JsonResponse({"status": "POST method required"})


@permission_required("add_lecturer")
@login_required(login_url="login")
@csrf_exempt
def upload_lecturers(request):
    if request.method == "POST":
        file = pd.read_excel(request.body)
        file.to_csv("portal/static/portal/lecturers.csv", index=None, header=True)
        with open("portal/static/portal/lecturers.csv") as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    latest_lecturer = Lecturer.lecturer.latest("date_joined")
                    serial = latest_lecturer[0].username.split("-")
                    id = serial[1].strip()
                except (IndexError, Lecturer.DoesNotExist):
                    id = 0
                try:
                    match row["department"].strip():
                        case "Computer Science":
                            id = f'ECS-{int(id) + 1}-{datetime.datetime.now().strftime("%y")}'
                        case "Psychology":
                            id = f'EPS-{int(id) + 1}-{datetime.datetime.now().strftime("%y")}'
                        case "Early Childhood Education":
                            id = f'EEC-{int(id) + 1}-{datetime.datetime.now().strftime("%y")}'
                        case "Chemical Engineering":
                            id = f'ECE-{int(id) + 1}-{datetime.datetime.now().strftime("%y")}'
                        case "Finance":
                            id = f'EFI-{int(id) + 1}-{datetime.datetime.now().strftime("%y")}'
                        case _:
                            return JsonResponse({"status": 912})
                    try:
                        Lecturer.lecturer.get(national_id=row["nationalID"])
                        return JsonResponse({"status": 935})
                    except Lecturer.DoesNotExist:
                        try:
                            lecturer = Lecturer.lecturer.create(
                                username=id,
                                first_name=row["first_name"].strip(),
                                last_name=row["last_name"].strip(),
                                phone_number=row["phone_number"],
                                national_id=row["nationalID"],
                                gender=row["gender"].strip(),
                                department=row["department"].strip(),
                                faculty=row["faculty"].strip(),
                            )
                            lecturer.user_permissions.clear()
                            comrade = Group.objects.get(name="Lecturer")
                            lecturer.groups.add(comrade)
                            lecturer.save()
                        except IntegrityError:
                            return JsonResponse({"status": 935})
                except KeyError:
                    return JsonResponse({"status": 900})
        return JsonResponse({"status": 200})
    else:
        return JsonResponse({"error": "POST method required"})


@permission_required("add_lecturer")
@login_required(login_url="login")
@csrf_exempt
def register_lecturer(request):
    if request.method == "POST":
        data = json.loads(request.body)
        latest_lecturer = Lecturer.lecturer.latest("date_joined")
        try:
            serial = latest_lecturer[0].username.split("-")
            id = serial[1].strip()
        except (AttributeError, Lecturer.DoesNotExist, IndexError):
            id = 0
        try:
            match data["department"].strip():
                case "Computer Science":
                    id = f'ECS-{int(id) + 1}-{datetime.datetime.now().strftime("%y")}'
                case "Psychology":
                    id = f'EPS-{int(id) + 1}-{datetime.datetime.now().strftime("%y")}'
                case "Early Childhood Education":
                    id = f'EEC-{int(id) + 1}-{datetime.datetime.now().strftime("%y")}'
                case "Chemical Engineering":
                    id = f'ECE-{int(id) + 1}-{datetime.datetime.now().strftime("%y")}'
                case "Finance":
                    id = f'EFI-{int(id) + 1}-{datetime.datetime.now().strftime("%y")}'
                case _:
                    return JsonResponse({"status": 912})
            try:
                Lecturer.lecturer.get(national_id=data["nationalID"])
                return JsonResponse({"status": 935})
            except Lecturer.DoesNotExist:
                try:
                    lecturer = Lecturer.lecturer.create(
                        username=id,
                        first_name=data["first_name"].strip(),
                        last_name=data["last_name"].strip(),
                        phone_number=data["phone_number"],
                        national_id=data["nationalID"],
                        gender=data["gender"].strip(),
                        department=data["department"].strip(),
                        faculty=data["faculty"].strip(),
                    )
                    lecturer.user_permissions.clear()
                    comrade = Group.objects.get(name="Lecturer")
                    lecturer.groups.add(comrade)
                    lecturer.save()
                except IntegrityError:
                    return JsonResponse({"status": 935})
        except KeyError:
            return JsonResponse({"status": 900})

        return JsonResponse({"status": 200})
    else:
        return JsonResponse({"status": "POST method required"})


@permission_required("add_student")
@login_required(login_url="login")
@csrf_exempt
def register_student(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST method required"})
    else:
        data = json.loads(request.body)
        try:
            latest_student = Student.student.latest("date_joined")
            serial = latest_student.username.split("-")
            id = serial[1].strip()
        except (AttributeError, Student.DoesNotExist, IndexError):
            id = 0
        try:
            match data["faculty"].strip():
                case "LAW":
                    id = f'LL-{int(id) + 1}-{datetime.datetime.now().strftime("%y")}'
                case "PHY_SCI":
                    id = f'PS-{int(id) + 1}-{datetime.datetime.now().strftime("%y")}'
                case "EDU":
                    id = f'EDU-{int(id) + 1}-{datetime.datetime.now().strftime("%y")}'
                case "SOC_SCI":
                    id = f'SC-{int(id) + 1}-{datetime.datetime.now().strftime("%y")}'
                case "BUS":
                    id = f'BU-{int(id) + 1}-{datetime.datetime.now().strftime("%y")}'
                case "HEALTH_SCI":
                    id = f'HS-{int(id) + 1}-{datetime.datetime.now().strftime("%y")}'
                case _:
                    return JsonResponse({"status": 912})
            try:
                Student.student.get(national_id=data["nationalID"])
                return JsonResponse({"status": 935})
            except Student.DoesNotExist:
                student = Student.student.create(
                    username=id,
                    first_name=data["first_name"].strip(),
                    last_name=data["last_name"].strip(),
                    phone_number=data["phone_number"],
                    national_id=data["nationalID"].strip(),
                    gender=data["gender"].strip(),
                    faculty=data["faculty"].strip(),
                    course=data["course"].strip(),
                )
                student.user_permissions.clear()
                comrade = Group.objects.get(name="Comrade")
                student.groups.add(comrade)
                student.save()
        except KeyError:
            return JsonResponse({"status": 900})
    return JsonResponse({"status": 200})


@login_required(login_url="login")
def faculties_view(request):
    if request.user.is_superuser:
        return render(request, "administration/faculties.html")


@login_required(login_url="login")
def faculty_details(request):
    faculties = []
    for faculty in Faculty.objects.all():
        faculties.append(
            {
                faculty.name(): [
                    department.serialize() for department in faculty.school.all()
                ],
                "courses": [course.serialize() for course in faculty.division.all()],
            }
        )
    return JsonResponse(faculties, safe=False)


@permission_required("add_department")
@login_required(login_url="login")
@csrf_exempt
def upload_departments(request):
    if request.method == "POST":
        file = pd.read_excel(request.body)
        file.to_csv("portal/static/portal/departments.csv", index=None, header=True)
        with open("portal/static/portal/departments.csv") as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    try:
                        try:
                            faculty = Faculty.objects.get(faculty=row["faculty"])
                            Department.objects.create(
                                faculty=faculty, department=row["department"]
                            )
                        except KeyError:
                            return JsonResponse({"status": 900})
                    except IntegrityError:
                        return JsonResponse({"status": 935})
                except Faculty.DoesNotExist:
                    return JsonResponse({"status": 905})
        return JsonResponse({"status": 200})


@permission_required("add_department")
@login_required(login_url="login")
@csrf_exempt
def register_department(request):
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            try:
                try:
                    faculty = Faculty.objects.get(faculty=data["faculty"])
                    Department.objects.create(
                        faculty=faculty, department=data["department"]
                    )
                except KeyError:
                    return JsonResponse({"status": 900})
            except IntegrityError:
                return JsonResponse({"status": 935})
        except Faculty.DoesNotExist:
            return JsonResponse({"status": 905})
        return JsonResponse({"status": 200})
    else:
        return JsonResponse({"error": "POST method required"})


@permission_required("add_course")
@login_required(login_url="login")
@csrf_exempt
def upload_courses(request):
    if request.method == "POST":
        file = pd.read_excel(request.body)
        file.to_csv("portal/static/portal/courses.csv", index=None, header=True)
        with open("portal/static/portal/courses.csv") as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    try:
                        try:
                            faculty = Faculty.objects.get(faculty=row["faculty"])
                            Course.objects.create(faculty=faculty, course=row["course"])
                        except KeyError:
                            return JsonResponse({"status": 900})
                    except IntegrityError:
                        return JsonResponse({"status": 935})
                except Faculty.DoesNotExist:
                    return JsonResponse({"status": 905})
        return JsonResponse({"status": 200})


@permission_required("add_course")
@login_required(login_url="login")
@csrf_exempt
def register_course(request):
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            try:
                try:
                    faculty = Faculty.objects.get(faculty=data["faculty"])
                    Course.objects.create(faculty=faculty, course=data["course"])
                except KeyError:
                    return JsonResponse({"status": 900})
            except IntegrityError:
                return JsonResponse({"status": 935})
        except Faculty.DoesNotExist:
            return JsonResponse({"status": 905})
        return JsonResponse({"status": 200})
    else:
        return JsonResponse({"error": "POST method required"})
