from django.contrib.auth.hashers import make_password
from django.contrib.auth.management import create_permissions
from django.db import migrations

DEPARTMENTS = ["Информационные технологии", "Прикладная математика"]

COURSES = [
    ("Веб-программирование", "Информационные технологии",
     "HTML, CSS, JavaScript и основы создания веб-приложений."),
    ("Программирование на Python", "Информационные технологии",
     "Синтаксис языка, функции, модули и работа с файлами."),
    ("Базы данных", "Информационные технологии",
     "Реляционная модель, SQL-запросы и проектирование таблиц."),
    ("Разработка веб-приложений на Django", "Информационные технологии", ""),
    ("Математическое моделирование", "Прикладная математика",
     "Построение и анализ математических моделей процессов."),
]


def create_data(apps, schema_editor):
    for app_config in apps.get_app_configs():
        app_config.models_module = True
        create_permissions(app_config, apps=apps, verbosity=0)
        app_config.models_module = None

    Department = apps.get_model("accounts", "Department")
    Course = apps.get_model("accounts", "Course")
    StudentProfile = apps.get_model("accounts", "StudentProfile")
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")
    User = apps.get_model("auth", "User")

    departments = {name: Department.objects.create(name=name) for name in DEPARTMENTS}
    courses = [
        Course.objects.create(title=t, department=departments[d], description=desc)
        for t, d, desc in COURSES
    ]

    students = Group.objects.create(name="Студенты")
    students.permissions.set(Permission.objects.filter(
        content_type__app_label="accounts",
        codename__in=["view_course", "view_department"],
    ))

    methodists = Group.objects.create(name="Методисты")
    methodists.permissions.set(Permission.objects.filter(
        content_type__app_label="accounts",
        codename__in=[
            "view_course", "add_course", "change_course",
            "view_department", "add_department", "change_department",
        ],
    ))

    User.objects.create(
        username="admin", password=make_password("Mai2026Django!"),
        is_staff=True, is_superuser=True,
    )
    student = User.objects.create(
        username="student1", password=make_password("Kuznetsova2026!"),
    )
    student.groups.add(students)
    profile = StudentProfile.objects.create(user=student, group_name="М3О-236БВ-25")
    profile.courses.set(courses[:3])

    methodist = User.objects.create(
        username="methodist1", password=make_password("Metodist2026!"),
        is_staff=True,
    )
    methodist.groups.add(methodists)


def delete_data(apps, schema_editor):
    apps.get_model("auth", "User").objects.filter(
        username__in=["admin", "student1", "methodist1"]).delete()
    apps.get_model("auth", "Group").objects.filter(
        name__in=["Студенты", "Методисты"]).delete()
    apps.get_model("accounts", "Department").objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
        ("auth", "0012_alter_user_first_name_max_length"),
        ("contenttypes", "0002_remove_content_type_name"),
    ]

    operations = [
        migrations.RunPython(create_data, delete_data),
    ]
