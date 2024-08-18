from . import views
from django.urls import path

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("register", views.register_view, name="register"),
    path("faculties", views.faculties_view, name="faculties"),
    path("add_unit", views.add_unit, name="add_unit"),
    path("remove_unit", views.remove_unit, name="remove_unit"),
    path("upload_students", views.upload_students, name="upload"),
    path("upload_departments", views.upload_departments, name="upload_departments"),
    path("register_department", views.register_department, name="register_dept"),
    path("faculty_details", views.faculty_details, name="faculty_details"),
    path("upload_lecturers", views.upload_lecturers, name="upload_lecturers"),
    path("register_student", views.register_student, name="register_student"),
    path("register_lecturer", views.register_lecturer, name="register_lecturer"),
    path("upload_courses", views.upload_courses, name="upload_departments"),
    path("register_course", views.register_course, name="register_dept"),
    path("upload_units", views.upload_units, name="upload_units"),
    path("make_hod", views.make_hod, name="hod"),
    path("dept_details", views.dept_details, name="dept_details"),
    path("assign_unit", views.assign_unit, name="assign_unit")
]
