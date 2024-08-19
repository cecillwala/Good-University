from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group


# Create your models here

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
                return super().save(self, *args, **kwargs)

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
        return {
            "department": self.department,
            "lecturers": [lecturer.username for lecturer in self.sector.all()],
            "units": [{"unit":unit.unit, "unit_code":unit.unit_code} for unit in self.syllabus.all()]
        }

class Course(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.DO_NOTHING, related_name="division", null=True)
    course = models.CharField(max_length=100, null=True, unique=True)

    def serialize(self):
        return {"course": self.course, 
                "units": [unit.serialize() for unit in self.topics.order_by("year_sem")]
            }


class Unit(models.Model):
    department = models.ForeignKey(Department, on_delete=models.DO_NOTHING, related_name="syllabus")
    unit_code = models.CharField(max_length=20)
    unit = models.CharField(max_length=100)
    course = models.ManyToManyField(Course, related_name="topics", null=True)
    year_sem = models.FloatField()

    def serialize(self):
        return {"unit_code": self.unit_code, 
                "unit": self.unit,
                "yr/sem": self.year_sem,
                "courses": [course.course for course in self.course.all()],
                "professors": [professor.username for professor in self.professor.all()],
                "students": [student.username for student in self.apprentice.all()]
                }



class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        HR = "HR", "HR"
        STUDENT = "STUDENT", "Student"
        LECTURER = "LECTURER", "Lecturer"

    base_role = Role.ADMIN
    role = models.CharField(max_length=20, choices=Role.choices)
    national_id = models.IntegerField(null=True, unique=True)
    gender = models.CharField(max_length=40, null=True)
    phone_number = models.IntegerField(null=True)
    faculty = models.ForeignKey(
        Faculty, on_delete=models.DO_NOTHING, null=True, related_name="sector"
    )

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
            "faculty": self.faculty,
        }


class StudentManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.STUDENT)


class Student(User):
    base_role = User.Role.STUDENT
    student = StudentManager()

    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING, null=True, related_name="study")
    units = models.ManyToManyField(Unit, related_name="apprentice", null=True)
    residence = models.CharField(max_length=100, null=True)

    def serialize(self):
        return {
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "gender": self.gender,
            "phone_number": self.phone_number,
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

    department = models.ForeignKey(Department, on_delete=models.DO_NOTHING, null=True, related_name="sector")
    units = models.ManyToManyField(Unit, related_name="professor", null=True, blank=True)
    office = models.CharField(max_length=50, null=True, blank=True)

    def serialize(self):
        return {
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "gender": self.gender,
            "phone_number": self.phone_number,
            "department": self.department.department,
            "faculty": self.faculty.faculty,
            "units": [unit.serialize() for unit in self.units.all()]
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



