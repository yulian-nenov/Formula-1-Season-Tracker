from django.contrib.auth.models import User, Permission
from django.test import TestCase

from drivers.forms import DriverCreateForm, DriverEditForm
from drivers.models import Driver
from teams.models import Team


class DriverFormTests(TestCase):
    VALID_TEAM_DATA = {
        'name': 'Team 1',
        'principal': 'Test Principal',
        'base_country': 'Test Country',
        'engine_supplier': 'Test Supplier',
        'team_color': '#F47600',
        'logo_image_url': 'https://test.com',
    }

    VALID_DRIVER_DATA = {
        'name': 'Test Driver',
        'number': 33,
        'nationality': 'DE',
        'age': 33,
        'image': 'https://test.com',
    }

    def setUp(self):
        self.user = User.objects.create_user(username='test', email='test@test.com', password='12test34')
        self.user.user_permissions.add(Permission.objects.get(codename='add_driver'))
        self.team1 = Team.objects.create(**self.VALID_TEAM_DATA, owner=self.user)
        self.driver1 = Driver.objects.create(**self.VALID_DRIVER_DATA, team=self.team1)

    def test_team_with_three_drivers__raised_validation(self):
        driver_two_data = {**self.VALID_DRIVER_DATA, 'name': 'Driver 2', 'number': 31, 'team':self.team1}
        driver2 = Driver.objects.create(**driver_two_data)
        form_data = {**self.VALID_DRIVER_DATA, 'name': 'Driver 3', 'number': 34, 'team':self.team1.pk}

        form = DriverCreateForm(data=form_data, user=self.user)

        self.assertFalse(form.is_valid())
        self.assertIn('team', form.errors)

    def test_edit_driver__team_with_two_drivers__success(self):
        driver_two_data = {**self.VALID_DRIVER_DATA, 'name': 'Driver 2', 'number': 31, 'team': self.team1}
        driver2 = Driver.objects.create(**driver_two_data)

        form_data = {**self.VALID_DRIVER_DATA, 'name': 'Driver 3', 'number': 34, 'team': self.team1.pk}

        form = DriverEditForm(data=form_data, user=self.user, instance=driver2)

        self.assertTrue(form.is_valid())

    def test_create_driver__show_only_owned_teams__success(self):
        other_user = User.objects.create_user(username='other', email='other@other.com', password='12other34')
        other_team = Team.objects.create(**{**self.VALID_TEAM_DATA, 'owner': other_user, 'name': 'Other Team'})

        form = DriverCreateForm(user=self.user)

        self.assertIn(self.team1, form.fields['team'].queryset)
        self.assertNotIn(other_team, form.fields['team'].queryset)
