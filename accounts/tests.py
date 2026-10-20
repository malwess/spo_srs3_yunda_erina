from django.contrib.auth.models import User
from django.test import TestCase


class AccessTests(TestCase):

    def test_profile_redirects_anonymous_user(self):
        response = self.client.get("/profile/")
        self.assertRedirects(response, "/accounts/login/?next=/profile/")

    def test_courses_redirect_anonymous_user(self):
        response = self.client.get("/courses/")
        self.assertRedirects(response, "/accounts/login/?next=/courses/")

    def test_login_page_uses_bootstrap(self):
        response = self.client.get("/accounts/login/")
        self.assertContains(response, "bootstrap.min.css")
        self.assertContains(response, "css/style.css")

    def test_student_sees_courses_table(self):
        self.client.login(username="student1", password="Kuznetsova2026!")
        response = self.client.get("/courses/")
        self.assertContains(response, "table table-striped table-hover")
        self.assertContains(response, "Базы данных")

    def test_groups_and_permissions(self):
        student = User.objects.get(username="student1")
        methodist = User.objects.get(username="methodist1")
        self.assertTrue(student.has_perm("accounts.view_course"))
        self.assertFalse(student.has_perm("accounts.change_course"))
        self.assertTrue(methodist.has_perm("accounts.change_course"))
        self.assertFalse(methodist.has_perm("accounts.delete_course"))

    def test_logout_redirects_to_login(self):
        self.client.login(username="student1", password="Kuznetsova2026!")
        response = self.client.post("/accounts/logout/")
        self.assertRedirects(response, "/accounts/login/")
