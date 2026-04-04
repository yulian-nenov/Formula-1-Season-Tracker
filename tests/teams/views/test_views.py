from django.contrib.auth.models import User, Permission
from django.test import TestCase, Client
from django.urls import reverse

from teams.models import Team, CarModel


class TeamCreateViewTests(TestCase):
    VALID_TEAM_CAR_DATA = {
            'team-name': 'Test',
            'team-principal': 'Test principal',
            'team-base_country': 'Test country',
            'team-engine_supplier': 'Test supplier',
            'team-team_color': '#F47600',
            'team-logo_image_url': 'https://test.com',

            'car-name': 'Test car',
            'car-year': 2020,
            'car-power_unit': 'Test power',
            'car-in_use': True,
        }

    VALID_TEAM_DATA = {
        'name': 'Test',
        'principal': 'Test principal',
        'base_country': 'Test country',
        'engine_supplier': 'Test supplier',
        'team_color': '#F47600',
        'logo_image_url': 'https://test.com',
    }

    def setUp(self):
        self.user = User.objects.create_user(
            username="test",
            email="test@test.com",
            password="12test34",
        )

    def test_unauthenticated_user_redirected_to_login(self):
        response = self.client.get(reverse('teams:create'))
        self.assertRedirects(response, f"{reverse('accounts:login')}?next={reverse('teams:create')}")

    def test_create_team__user_without_permission__returns_403(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('teams:create'))
        self.assertEqual(response.status_code, 403)

    def test_create_team_and_redirect__valid(self):
        self.user.user_permissions.add(Permission.objects.get(codename="add_team"))
        self.client.force_login(self.user)

        response = self.client.post(reverse('teams:create'), data=self.VALID_TEAM_CAR_DATA)

        self.assertRedirects(response, reverse('teams:list'))
        self.assertEqual(Team.objects.count(), 1)
        self.assertEqual(CarModel.objects.count(), 1)

    def test_invalid_form(self):
        self.user.user_permissions.add(Permission.objects.get(codename="add_team"))
        self.client.force_login(self.user)

        response= self.client.get(reverse('teams:create'), data={})

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())

    def test_team_edit_view_owner_can_edit__success(self):
        self.user.user_permissions.add(Permission.objects.get(codename="change_team"))
        self.client.force_login(self.user)

        initial_team = Team.objects.create(**self.VALID_TEAM_DATA)
        initial_team.owner = self.user
        initial_team.save()

        form_data = {
            **self.VALID_TEAM_CAR_DATA,
            'team-name': 'Updated name',
        }

        response = self.client.post(reverse('teams:edit', kwargs={'pk': initial_team.pk}), data=form_data)
        self.assertRedirects(response, reverse('teams:details', kwargs={'pk': initial_team.pk}))
        initial_team.refresh_from_db()
        self.assertEqual(initial_team.name, form_data['team-name'])

    def test_team_edit_non_owner_but_permission__raises_403(self):
        self.user.user_permissions.add(Permission.objects.get(codename="change_team"))
        self.client.force_login(self.user)

        team = Team.objects.create(**self.VALID_TEAM_DATA)

        form_data = {
            **self.VALID_TEAM_CAR_DATA,
            'team-name': 'Updated name',
        }

        response = self.client.post(reverse('teams:edit', kwargs={'pk': team.pk}), data=form_data)

        self.assertEqual(response.status_code, 403)

    def test_owner_delete_team__success(self):
        self.user.user_permissions.add(Permission.objects.get(codename="delete_team"))
        self.client.force_login(self.user)

        team = Team.objects.create(**self.VALID_TEAM_DATA, owner=self.user)

        response = self.client.post(reverse('teams:delete', kwargs={'pk': team.pk}))

        self.assertRedirects(response, reverse('teams:list'))
        self.assertEqual(Team.objects.count(), 0)
