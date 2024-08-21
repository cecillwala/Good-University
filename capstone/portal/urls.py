from . import views
from django.urls import path

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("register", views.register_view, name="register"),
    path("faculties", views.faculties_view, name="faculties"),
    path("add_course_unit", views.add_unit, name="add_unit"),
    path("remove_course_unit", views.withdraw_unit, name="remove_unit"),
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
    path("assign_unit", views.assign_unit, name="assign_unit"),
    path("lec_details/<str:lec>", views.lec_details, name="lec_details"),
    path("unit_details/<str:unit>", views.unit_details, name="unit_details"),
    path("remove_unit/<str:unit>/<str:lec>", views.remove_unit, name="remove_unit"),
    path("unit_registration", views.unit_registration, name="unit_registration"),
    path("upload_rooms", views.upload_rooms, name="upload_rooms"),
    path("accom_registration", views.accomodation_registration, name="accom_registration"),
    path("lec_units", views.lecturer_units, name="lec_units"),
    path("faculty_departments/<str:faculty>", views.faculty_departments, name="faculty_departments"),
    path("faculty_courses/<str:faculty>", views.faculty_courses, name="faculty_courses"),
    path("department_lecturers/<str:department>", views.department_lecturers, name="dept_lecs"),
    path("department_units/<str:department>", views.department_units, name="dept_units"),
    path("course_units/<str:course>", views.course_units, name="course_units"),
    path('remove_dept_unit', views.remove_dept_unit, name="remove_dept_unit"),
    path('add_dept_unit', views.add_dept_unit, name="remove_dept_unit"),
]
