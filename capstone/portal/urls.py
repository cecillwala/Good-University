from . import views
from django.urls import path

urlpatterns = [
    path(" ", views.index, name="index"),
    path("", views.emp_index, name="emp_index"),
    path("login", views.login_view, name="login"),
    path("register", views.register_view, name="register"),
    path("upload_students", views.upload_students, name="upload"),
    path("register_student", views.register_student, name="register_student"),
    path("upload_lecturers", views.register_lecturers, name="upload-lecturers"),
]