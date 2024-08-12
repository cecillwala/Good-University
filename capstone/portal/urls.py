from . import views
from django.urls import path

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("register", views.register_view, name="register"),
    path("faculties", views.faculties_view, name="faculties"),
    path("upload_depts", views.upload_departments, name="upload_departments"),
    path("register_dept", views.register_department, name="register_dept"),
    path("upload_students", views.upload_students, name="upload"),
    path("faculty_details", views.faculty_details, name="faculty_details"),
    path("upload_lecturers", views.upload_lecturers, name="upload_lecturers"),
    path("register_student", views.register_student, name="register_student"),
    path("register_lecturer", views.register_lecturer, name="register_lecturer"),
    path("upload_courses", views.upload_courses, name="upload_departments"),
    path("register_courses", views.register_course, name="register_dept"),
]
