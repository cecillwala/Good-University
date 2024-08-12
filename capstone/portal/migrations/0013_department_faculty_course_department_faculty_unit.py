# Generated by Django 5.0.6 on 2024-08-10 08:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("portal", "0012_lecturer_office_student_residence_user_department_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Department",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "department",
                    models.CharField(max_length=100, null=True, unique=True),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Faculty",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "faculty",
                    models.CharField(
                        choices=[
                            ("PHY_SCI", "Physical Science"),
                            ("SOC_SCI", "Social Science"),
                            ("HEALTH_SCI", "Health Science"),
                            ("EDU", "Education"),
                            ("BUS", "Business"),
                            ("LAW", "Law"),
                        ],
                        max_length=100,
                        null=True,
                        unique=True,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Course",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("course", models.CharField(max_length=100, null=True, unique=True)),
                (
                    "department",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="division",
                        to="portal.department",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="department",
            name="faculty",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="school",
                to="portal.faculty",
            ),
        ),
        migrations.CreateModel(
            name="Unit",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("unit_code", models.CharField(max_length=20, unique=True)),
                ("unit", models.CharField(max_length=100, unique=True)),
                (
                    "course",
                    models.ManyToManyField(related_name="program", to="portal.course"),
                ),
            ],
        ),
    ]
