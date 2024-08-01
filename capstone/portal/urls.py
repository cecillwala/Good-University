from . import views
from django.urls import path

urlpatterns = [
    path(" ", views.index, name="index"),
    path("", views.emp_index, name="emp_index"),
    path("login", views.login_view, name="login"),
    path("register", views.register_view, name="register"),
    path("upload", views.upload_students, name="upload")
]