from django.test import TestCase

from teams.forms import TeamCreateForm, CarCreateForm
from teams.models import Team


class TeamFormTests(TestCase):
    VALID_TEAM_DATA = {
            'name': 'Test',
            'principal': 'Test principal',
            'base_country': 'Test country',
            'engine_supplier': 'Test supplier',
            'team_color': '#F47600',
            'logo_image_url': 'https://test.com',
        }

    def test_team_create_form_success(self):
        form = TeamCreateForm(data=self.VALID_TEAM_DATA)
        self.assertTrue(form.is_valid())

    def test_team_create_form_invalid_color_raises_error(self):
        form_data = {
            'name': 'Test',
            'principal': 'Test principal',
            'base_country': 'Test country',
            'engine_supplier': 'Test supplier',
            'team_color': '#00000', # invalid, not in choices
            'logo_image_url': 'https://test.com',
        }

        form = TeamCreateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('team_color', form.errors)

    def test_car_model_create_form_success(self):
        team = Team.objects.create(**self.VALID_TEAM_DATA)

        form_data = {
            'name': 'Test',
            'year': 2026,
            'power_unit': 'Test unit',
            'in_use': True,
            'team': team,
        }

        form = CarCreateForm(data=form_data)
        self.assertTrue(form.is_valid())
