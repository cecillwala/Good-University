from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


# Create your models here

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", 'Admin'
        HR = "HR", 'HR'
        STUDENT = "STUDENT", 'Student'
        LECTURER = "LECTURER", 'Lecturer'

    base_role = Role.STUDENT
    role = models.CharField(max_length=20, choices=Role, default=base_role)
    national_id = models.IntegerField(null=True)
    gender = models.CharField(max_length=40, null=True)
    phone_number = models.IntegerField(null=True)


class Student(User):
    base_role = User.Role.STUDENT


class Lecturer(User):
    base_role = User.Role.LECTURER


class HR(User):
    base_role = User.Role.HR


class Admin(User):
    base_role = User.Role.ADMIN