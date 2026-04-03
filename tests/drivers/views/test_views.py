from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class DriverViewsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')

    def test_unauthenticated_user_redirected_to_login(self):
        response = self.client.get(reverse('drivers:create'))
        self.assertRedirects(response, f"{reverse('accounts:login')}?next={reverse('drivers:create')}")

    def test_user_without_permission__raises_403(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('drivers:create'))
        self.assertEqual(response.status_code, 403)