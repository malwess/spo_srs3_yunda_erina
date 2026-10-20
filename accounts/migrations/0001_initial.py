# Миграция 0001: таблицы Department, Course и StudentProfile

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
                    "name",
                    models.CharField(
                        max_length=200, unique=True, verbose_name="Название"
                    ),
                ),
            ],
            options={
                "verbose_name": "Факультет",
                "verbose_name_plural": "Факультеты",
                "ordering": ["name"],
            },
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
                ("title", models.CharField(max_length=200, verbose_name="Название")),
                ("description", models.TextField(blank=True, verbose_name="Описание")),
                (
                    "department",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="courses",
                        to="accounts.department",
                        verbose_name="Факультет",
                    ),
                ),
            ],
            options={
                "verbose_name": "Курс",
                "verbose_name_plural": "Курсы",
                "ordering": ["id"],
            },
        ),
        migrations.CreateModel(
            name="StudentProfile",
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
                    "group_name",
                    models.CharField(
                        blank=True, max_length=50, verbose_name="Учебная группа"
                    ),
                ),
                (
                    "courses",
                    models.ManyToManyField(
                        blank=True,
                        related_name="students",
                        to="accounts.course",
                        verbose_name="Курсы",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="profile",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Пользователь",
                    ),
                ),
            ],
            options={
                "verbose_name": "Профиль студента",
                "verbose_name_plural": "Профили студентов",
            },
        ),
    ]
