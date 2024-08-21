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
    period = academic_year(request)
    if request.user.is_superuser:
        return render(request, "administration/index.html", {
            "dorms": [{"dorm":accom.hostel, "name":accom.name()} for accom in Residence.objects.all()],
            "faculties": [{"faculty":faculty.faculty, "name": faculty.name()} for faculty in Faculty.objects.all()],
            "courses": [course.course for course in Course.objects.all()],
            "period": period
        })
    elif request.user.groups.contains(Group.objects.get(name="hod")):
        return render(request,"administration/hod-index.html", {
            "lecturer": Lecturer.lecturer.get(username=request.user.username),
            "period": period
        })
    else:
        return render(request,"administration/lec-index.html", {
            "lecturer": Lecturer.lecturer.get(username=request.user.username),
            "period": period
        })
    # else:
    #     return render(request, "portal/index.html",{
    #         "student": Student.student.get(username=request.user.username),
    #         "dorms": [accom.name() for accom in Residence.objects.all()],
    #         "period": period
    #         }
    #     )


def login_view(request):
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST["userID"],
            password=request.POST["password"],
        )
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        elif user is None:
            return render(
                request, "portal/login.html", {"message": "Invalid ID and/or password"}
            )
    logout(request)
    return render(request, "portal/login.html")


def register_view(request):
    if request.method == "POST":
        if request.POST["password"] == request.POST["confirmation"]:
            try:
                user = User.objects.get(username=request.POST["userID"])
            except ObjectDoesNotExist:
                return render(
                    request, "portal/register.html", {"no_user": "ID does not exist"}
                )
            print(user.username, request.POST["password"])
            user.set_password(f'{request.POST["password"]}')
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
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
        try:
            file = pd.read_excel(request.body)
        except ValueError:
            return JsonResponse({"status": 239})
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
                            id = f"LL-{int(id) + 1}-{row['year']}"
                        case "PHY_SCI":
                            id = f"PS-{int(id) + 1}-{row['year']}"
                        case "EDU":
                            id = f"EDU-{int(id) + 1}-{row['year']}"
                        case "SOC_SCI":
                            id = f"SC-{int(id) + 1}-{row['year']}"
                        case "BUS":
                            id = f"BU-{int(id) + 1}-{row['year']}"
                        case "HEALTH_SCI":
                            id = f"HS-{int(id) + 1}-{row['year']}"
                        case _:
                            return JsonResponse({"status": 912})
                    try:
                        student = Student.student.create(
                            username=id,
                            first_name=row["first_name"].strip(),
                            last_name=row["last_name"].strip(),
                            phone_number=row["phone_number"],
                            national_id=row["nationalID"],
                            gender=row["gender"].strip(),
                            faculty=Faculty.objects.get(faculty=row["faculty"].strip()),
                            course=Course.objects.get(course=row["course"].strip()),
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
    else:
        return JsonResponse({"status": "POST method required"})


@permission_required("add_lecturer")
@login_required(login_url="login")
@csrf_exempt
def upload_lecturers(request):
    if request.method == "POST":
        try:
            file = pd.read_excel(request.body)
        except ValueError:
            return JsonResponse({"status": 239})
        file.to_csv("portal/static/portal/lecturers.csv", index=None, header=True)
        with open("portal/static/portal/lecturers.csv") as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    latest_lecturer = Lecturer.lecturer.latest("date_joined")
                    serial = latest_lecturer.username.split("-")
                    id = serial[1].strip()
                except (IndexError, Lecturer.DoesNotExist):
                    id = 0
                try:
                    match row["faculty"].strip():
                        case "LAW":
                            id = f'ELL-{int(id) + 1}-{row["year"]}'
                        case "PHY_SCI":
                            id = f'EPS-{int(id) + 1}-{row["year"]}'
                        case "EDU":
                            id = f'EEDU-{int(id) + 1}-{row["year"]}'
                        case "SOC_SCI":
                            id = f'ESC-{int(id) + 1}-{row["year"]}'
                        case "BUS":
                            id = f'EBU-{int(id) + 1}-{row["year"]}'
                        case "HEALTH_SCI":
                            id = f'EHS-{int(id) + 1}-{row["year"]}'
                        case _:
                            return JsonResponse({"status": 912})
                    try:
                        lecturer = Lecturer.lecturer.create(
                            username=id,
                            first_name=row["first_name"].strip(),
                            last_name=row["last_name"].strip(),
                            phone_number=row["phone_number"],
                            national_id=row["nationalID"],
                            gender=row["gender"].strip(),
                            department=Department.objects.get(
                                department=row["department"].strip()
                            ),
                            faculty=Faculty.objects.get(faculty=row["faculty"].strip()),
                        )
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
            serial = latest_lecturer.username.split("-")
            id = serial[1].strip()
        except (AttributeError, Lecturer.DoesNotExist, IndexError):
            id = 0
        try:
            match data["faculty"].strip():
                case "LAW":
                    id = f'ELL-{int(id) + 1}-{data["year"]}'
                case "PHY_SCI":
                    id = f'EPS-{int(id) + 1}-{data["year"]}'
                case "EDU":
                    id = f'EEDU-{int(id) + 1}-{data["year"]}'
                case "SOC_SCI":
                    id = f'ESC-{int(id) + 1}-{data["year"]}'
                case "BUS":
                    id = f'EBU-{int(id) + 1}-{data["year"]}'
                case "HEALTH_SCI":
                    id = f'EHS-{int(id) + 1}-{data["year"]}'
                case _:
                    return JsonResponse({"status": 912})
            try:
                Lecturer.lecturer.get(national_id=data["nationalID"])
                return JsonResponse({"status": 935})
            except Lecturer.DoesNotExist:
                try:
                    faculty = Faculty.objects.get(faculty=data["faculty"])
                    dept = Department.objects.get(department=data["department"])
                    lecturer = Lecturer.lecturer.create(
                        username=id,
                        first_name=data["first_name"].strip(),
                        last_name=data["last_name"].strip(),
                        phone_number=data["phone_number"],
                        national_id=data["nationalID"],
                        gender=data["gender"].strip(),
                        department=dept,
                        faculty=faculty,
                    )
                    lecturer.user_permissions.clear()
                    comrade = Group.objects.get(name="lec")
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
                    id = f'LL-{int(id) + 1}-{data["year"]}'
                case "PHY_SCI":
                    id = f'PS-{int(id) + 1}-{data["year"]}'
                case "EDU":
                    id = f'EDU-{int(id) + 1}-{data["year"]}'
                case "SOC_SCI":
                    id = f'SC-{int(id) + 1}-{data["year"]}'
                case "BUS":
                    id = f'BU-{int(id) + 1}-{data["year"]}'
                case "HEALTH_SCI":
                    id = f'HS-{int(id) + 1}-{data["year"]}'
                case _:
                    return JsonResponse({"status": 912})
            try:
                Student.student.get(national_id=data["nationalID"])
                return JsonResponse({"status": 935})
            except Student.DoesNotExist:
                faculty = Faculty.objects.get(faculty=data["faculty"])
                course =  Course.objects.get(course=data["course"])
                student = Student.student.create(
                    username=id,
                    first_name=data["first_name"].strip(),
                    last_name=data["last_name"].strip(),
                    phone_number=data["phone_number"],
                    national_id=data["nationalID"].strip(),
                    gender=data["gender"].strip(),
                    faculty=faculty,
                    course=course,
                )
                student.user_permissions.clear()
                comrade = Group.objects.get(name="comrade")
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
                "name": faculty.name(),
                "faculty": faculty.faculty
            }
        )
    return JsonResponse(faculties, safe=False)


@permission_required("add_department")
@login_required(login_url="login")
@csrf_exempt
def upload_departments(request):
    if request.method == "POST":
        try:
            file = pd.read_excel(request.body)
        except ValueError:
            return JsonResponse({"status": 239})
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
    else:
        return JsonResponse({"error": "POST method required."})


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
        try:
            file = pd.read_excel(request.body)
        except ValueError:
            return JsonResponse({"status": 239})
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
    else:
        return JsonResponse({"error": "POST method required"})


@permission_required("add_unit")
@login_required(login_url="login")
@csrf_exempt
def register_unit(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            try:
                try:
                    course = Course.objects.get(course=data["course"])
                    dept = Department.objects.get(department=data["department"])
                    unit =  Unit(
                         unit=data["unit"],
                         unit_code=data["unit_code"],
                         department=dept,
                         year_sem=data["period"]
                        )
                    unit.save()
                    unit.course.add(course)
                except KeyError:
                    return JsonResponse({"status": 900})
            except IntegrityError:
                return JsonResponse({"status": 935})
        except (Course.DoesNotExist, Department.DoesNotExist):
            return JsonResponse({"status": 905})
        return JsonResponse({"status": 200})
    else:
        return JsonResponse({"error": "POST method required"})

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


@permission_required("add_accomodation")
@login_required(login_url="login")
@csrf_exempt
def register_room(request):
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            try:
                try:
                    hostel = Residence.objects.get(hostel=data["hostel"])
                    Accomodation.objects.create(
                        house=hostel,
                        room=data["room"],
                        bed=data["bed"]
                    )
                except KeyError:
                    return JsonResponse({"status": 900})
            except IntegrityError:
                return JsonResponse({"status": 935})
        except Residence.DoesNotExist:
            return JsonResponse({"status": 905})
        return JsonResponse({"status": 200})
    else:
        return JsonResponse({"error": "POST method required"})


@permission_required("add_unit")
@login_required(login_url="login")
@csrf_exempt
def upload_units(request):
    if request.method == "PUT":
        try:
            file = pd.read_excel(request.body)
        except ValueError:
            return JsonResponse({"status": 239})
        file.to_csv("portal/static/portal/units.csv", index=None, header=True)
        with open("portal/static/portal/units.csv") as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    try:
                        try:
                            dept = Department.objects.get(department=row["department"])
                            unit = Unit(
                                department=dept,
                                unit=row["unit"],
                                unit_code=row["unit_code"],
                                year_sem=row["year_sem"],
                            )
                            unit.save()
                            course = Course.objects.get(course=row["course"])
                            unit.course.add(course)
                        except KeyError:
                            return JsonResponse({"status": 900})
                    except IntegrityError:
                        return JsonResponse({"status": 935})
                except Course.DoesNotExist:
                    return JsonResponse({"status": 905})
        return JsonResponse({"status": 200})
    else:
        return JsonResponse({"error": "POST method required"})


@permission_required("add_lecturer")
@login_required(login_url="login")
@csrf_exempt
def add_unit(request):
    if request.method == "PUT":
        data = json.loads(request.body)
        try:
            course = Course.objects.get(course=data["course"])
        except Course.DoesNotExist:
            return JsonResponse({"status": 935})
        try:
            unit = Unit.objects.get(unit_code=data["unit"])
            unit.course.add(course)
        except Unit.DoesNotExist:
            return JsonResponse({"status": 405})
        return JsonResponse({"status": 200})
    else:
        return JsonResponse({"error": "POST method required"})


@permission_required("add_lecturer")
@login_required(login_url="login")
@csrf_exempt
def withdraw_unit(request):
    if request.method == "PUT":
        data = json.loads(request.body)
        try:
            course = Course.objects.get(course=data["course"])
        except Course.DoesNotExist:
            return JsonResponse({"status": 935})
        try:
            unit = Unit.objects.get(unit_code=data["unit"])
        except:
            return JsonResponse({"status": 405})
        unit.course.remove(course)
        return JsonResponse({"status": 200})
    else:
        return JsonResponse({"error": "PUT method required"})


@login_required(login_url="login")
@csrf_exempt
def add_dept_unit(request):
    if request.method == "PUT":
        data = json.loads(request.body)
        try:
            dept = Department.objects.get(department=data["department"])
        except Department.DoesNotExist:
            return JsonResponse({"status": 935})
        try:
            unit = Unit.objects.get(unit_code=data["unit"])
            unit.department = dept
            unit.save()
        except:
            return JsonResponse({"status": 405})
        return JsonResponse({"status": 200})
    else:
        return JsonResponse({"error": "PUT method required"})


@login_required(login_url="login")
@csrf_exempt
def remove_dept_unit(request):
    if request.method == "PUT":
        data = json.loads(request.body)
        try:
            unit = Unit.objects.get(unit_code=data["unit"])
            unit.department = None
            unit.save()
        except:
            return JsonResponse({"status": 405})
        return JsonResponse({"status": 200})
    else:
        return JsonResponse({"error": "PUT method required"})


@permission_required("change_lecturer")
@login_required(login_url="login")
@csrf_exempt
def make_hod(request):
    if request.method == "PUT":
        data = json.loads(request.body)
        hod = Lecturer.lecturer.get(username=data["lecturer"])
        perms = Group.objects.get(name="hod")
        if data["status"] == False:
            hod.groups.add(perms)
            hod.is_hod = True
            hod.save()
        else:
            hod.groups.remove(perms)
            hod.is_hod = False
            hod.save()
        return JsonResponse({"status": 200})


@login_required(login_url="login")
def faculty_departments(request, faculty):
    faculty = Faculty.objects.get(faculty=faculty)
    return JsonResponse([dept.department for dept in faculty.school.all()], safe=False)

@login_required(login_url="login")
def faculty_courses(request, faculty):
    faculty = Faculty.objects.get(faculty=faculty)
    return JsonResponse([course.course for course in faculty.division.all()], safe=False)


@login_required(login_url="login")
@csrf_exempt
def dept_details(request):
    hod = Lecturer.lecturer.get(username=request.user.username)
    dept = Department.objects.get(department=hod.department.department)
    return JsonResponse(dept.serialize())


@login_required(login_url="login")
@csrf_exempt
def assign_unit(request):
    if request.method == "PUT":
        data = json.loads(request.body)
        try:
            unit = Unit.objects.get(unit_code=data["unit"])
        except Unit.DoesNotExist:
            return JsonResponse({"status": 935})
        try:
            lec = Lecturer.lecturer.get(username=data["lecturer"])
            lec.units.add(unit)
            lec.save()
        except Lecturer.DoesNotExist:
            return JsonResponse({"status": 935})
        return JsonResponse({"status": 200})
    else:
        return JsonResponse({"error": "PUT method required"})


@login_required(login_url="login")
@csrf_exempt
def remove_unit(request, unit, lec):
    if request.method == "PUT":
        remove_unit = Unit.objects.get(unit_code=unit)
        lec = Lecturer.objects.get(username=lec)
        lec.units.remove(remove_unit)
        lec.save()
        return JsonResponse({"status": 200})
    else:
        return JsonResponse({"error": "PUT method required"})


@login_required(login_url="login")
def lec_details(request, lec):
    lecturer = Lecturer.lecturer.get(username=lec)
    return JsonResponse(lecturer.serialize())


@login_required(login_url="login")
def unit_details(request, unit):
    unit = Unit.objects.get(unit_code=unit)
    return JsonResponse(unit.serialize())


@login_required(login_url="login")
@csrf_exempt
def unit_registration(request):
    student = Student.student.get(username=request.user.username)
    if request.method == 'PUT':
        data = json.loads(request.body)
        unit = Unit.objects.get(unit_code=data)
        student.units.add(unit)
        student.save()

    period = academic_year(request)
    year_sem = float(period["year"] + float(f"0.{period['sem']}"))
    return JsonResponse({
        "all_units":[
            {"unit_code": unit.unit_code, "unit": unit.unit}
            for unit in student.course.topics.filter(year_sem=year_sem)
        ],
        "registered_units":[
            {"unit_code": unit.unit_code, "unit": unit.unit}
            for unit in student.units.filter(year_sem=year_sem)
        ]}
    )


@login_required(login_url="login")
@csrf_exempt
def upload_rooms(request):
    if request.method == "POST":
        try:
            file = pd.read_excel(request.body)
        except ValueError:
            return JsonResponse({"status": 239})
        file.to_csv('portal/static/portal/rooms.csv', header=True, index=False)
        with open("portal/static/portal/rooms.csv") as rooms:
            reader = csv.DictReader(rooms)
            for row in reader:
                try:
                    dorm = Residence.objects.get(hostel=row["hostel"])
                except Residence.DoesNotExist:
                    return JsonResponse({"status":912})
                try:
                    exists = Accomodation.objects.get(
                        house=dorm,
                        room=row["room"],
                        bed=row["bed"])
                    return JsonResponse({"status":935})
                except Accomodation.DoesNotExist:
                    try:
                        Accomodation.objects.create(
                            house=dorm,
                            room=row["room"],
                            bed=row["bed"]
                        )
                    except IntegrityError:
                        return JsonResponse({"status": 935})
        return JsonResponse({"status":200})
    else:
        return JsonResponse({"status":100})
    

@login_required(login_url="login")
@csrf_exempt
def accomodation_registration(request):
    student = Student.student.get(username=request.user.username)
    if request.method == "POST":
        data = json.loads(request.body)
        print(data)
        house = data["house"].upper()
        try:
            dorm = Residence.objects.get(hostel=house)
        except Residence.DoesNotExist:
            return JsonResponse({"status": 340})
        try:
            room = Accomodation.objects.get(house=dorm, room=data["room"], bed=data["bed"])
        except Accomodation.DoesNotExist:
            return JsonResponse({"status":560})
        Student.student.filter(username=request.user.username).update(residence=room)
        return JsonResponse({"status" : 200})
    try:
        return JsonResponse(student.residence.serialize(), safe=False)
    except AttributeError:
        return JsonResponse({"status":300}, safe=False)
    

@login_required(login_url="login")
def lecturer_units(request):
    lec = Lecturer.lecturer.get(username=request.user.username)
    return JsonResponse(lec.serialize())


@login_required(login_url="login")
def department_lecturers(request, department):
    dept = Department.objects.get(department=department)
    return JsonResponse([{"username":lec.username, "is_hod":lec.is_hod} for lec in dept.sector.all()], safe=False)


@login_required(login_url="login")
def department_units(request, department):
    dept = Department.objects.get(department=department)
    return JsonResponse([{"unit":unit.unit, "unit_code":unit.unit_code} for unit in dept.syllabus.order_by("year_sem")], safe=False)


@login_required(login_url="login")
def course_units(request, course):
    course = Course.objects.get(course=course)
    return JsonResponse([{"unit":unit.unit, "unit_code":unit.unit_code} for unit in course.topics.order_by("year_sem")], safe=False)


def academic_year(request):
    user = User.objects.get(username=request.user.username)
    if 7 <= int(datetime.datetime.now().strftime("%m")) <= 12:
        year = (
            int(datetime.datetime.now().strftime("%y")) - int(user.username.split("-")[2]) + 1
        )
        sem = 1
    elif 1 <= int(datetime.datetime.now().strftime("%m")) <= 4:
        year = int(datetime.datetime.now().strftime("%y")) - int(
            user.username.split("-")[2]
        )
        sem = 2
    return {"year":year, "sem":sem}