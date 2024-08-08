from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


# Create your models here


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        HR = "HR", "HR"
        STUDENT = "STUDENT", "Student"
        LECTURER = "LECTURER", "Lecturer"

    base_role = Role.ADMIN
    role = models.CharField(max_length=20, choices=Role.choices)
    national_id = models.IntegerField(null=True)
    gender = models.CharField(max_length=40, null=True)
    phone_number = models.IntegerField(null=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
            return super().save(*args, **kwargs)


class StudentManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.STUDENT)


class Student(User):
    base_role = User.Role.STUDENT
    student = StudentManager()

    course = models.CharField(max_length=150, null=True)


class LecturerManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.LECTURER)


class Lecturer(User):
    base_role = User.Role.LECTURER
    lecturer = LecturerManager()


class HRManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.HR)


class HR(User):
    base_role = User.Role.HR
    hr = HRManager()


class AdminManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.ADMIN)


class Admin(User):
    base_role = User.Role.ADMIN
    admin = AdminManager()
