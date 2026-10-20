from django.contrib.auth.models import User
from django.db import models


class Department(models.Model):
    name = models.CharField("Название", max_length=200, unique=True)

    class Meta:
        verbose_name = "Факультет"
        verbose_name_plural = "Факультеты"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Course(models.Model):
    title = models.CharField("Название", max_length=200)
    description = models.TextField("Описание", blank=True)
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="courses",
        verbose_name="Факультет",
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ["id"]

    def __str__(self):
        return self.title


class StudentProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name="Пользователь",
    )
    group_name = models.CharField("Учебная группа", max_length=50, blank=True)
    courses = models.ManyToManyField(
        Course,
        blank=True,
        related_name="students",
        verbose_name="Курсы",
    )

    class Meta:
        verbose_name = "Профиль студента"
        verbose_name_plural = "Профили студентов"

    def __str__(self):
        return f"Профиль {self.user.username}"
