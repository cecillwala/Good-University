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
    department = models.CharField(max_length=60, null=True)
    faculty = models.CharField(max_length=100, null=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
            return super().save(*args, **kwargs)

    def serialize(self):
        return {
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "gender": self.gender,
            "phone_number": self.phone_number,
            "department": self.department,
            "faculty": self.faculty,
        }


class StudentManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.STUDENT)


class Student(User):
    base_role = User.Role.STUDENT
    student = StudentManager()

    course = models.CharField(max_length=150, null=True)
    residence = models.CharField(max_length=100, null=True)

    def serialize(self):
        return {
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "gender": self.gender,
            "phone_number": self.phone_number,
            "department": self.department,
            "faculty": self.faculty,
            "course": self.course,
            "residence": self.residence,
        }

    class Meta:
        verbose_name = "Student"


class LecturerManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.LECTURER)


class Lecturer(User):
    base_role = User.Role.LECTURER
    lecturer = LecturerManager()

    office = models.CharField(max_length=50, null=True)

    def serialize(self):
        return {
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "gender": self.gender,
            "phone_number": self.phone_number,
            "department": self.department,
            "faculty": self.faculty,
            "office": self.office,
        }

    class Meta:
        verbose_name = "Lecturer"


class HRManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.HR)


class HR(User):
    base_role = User.Role.HR
    hr = HRManager()

    class Meta:
        verbose_name = "HR"


class Faculty(models.Model):
    class Faculties(models.TextChoices):
        PHY_SCI = "PHY_SCI", "Physical Science"
        SOC_SCI = "SOC_SCI", "Social Science"
        HEALTH_SCI = "HEALTH_SCI", "Health Science"
        EDU = "EDU", "Education"
        BUS = "BUS", "Business"
        LAW = "LAW", "Law"

    faculty = models.CharField(
        max_length=100, null=True, unique=True, choices=Faculties.choices
    )

    def save(self, *args, **kwargs):
        for label in Faculty.Faculties:
            if self.faculty.capitalize() in label.label:
                self.faculty = label
                return super().save(*args, **kwargs)

    def name(self):
        for label in Faculty.Faculties:
            if label == self.faculty:
                return label.label
        return None


class Department(models.Model):
    faculty = models.ForeignKey(
        Faculty, on_delete=models.DO_NOTHING, related_name="school"
    )
    department = models.CharField(max_length=100, null=True, unique=True)

    def serialize(self):
        return {"department": self.department}


class Course(models.Model):
    faculty = models.ForeignKey(
        Faculty, on_delete=models.DO_NOTHING, related_name="division", null=True
    )
    course = models.CharField(max_length=100, null=True, unique=True)

    def serialize(self):
        return {"course": self.course}


class Unit(models.Model):
    course = models.ManyToManyField(Course, related_name="program", symmetrical=False)
    unit_code = models.CharField(max_length=20, unique=True)
    unit = models.CharField(max_length=100, unique=True)

    def serialize(self):
        return {"unit_code": self.unit_code, "unit": self.unit}
