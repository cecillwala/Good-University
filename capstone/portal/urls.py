from . import views
from django.urls import path

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("register", views.register_view, name="register"),
    path("upload_students", views.upload_students, name="upload"),
    path("register_student", views.register_student, name="register_student"),
    path("upload_lecturers", views.upload_lecturers, name="upload_lecturers"),
    path("register_lecturer", views.register_lecturer, name="register_lecturer")
]
