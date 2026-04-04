import datetime
from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase

from drivers.models import Driver
from races.forms import ResultCreateForm
from races.models import Race
from teams.models import Team
from tracks.models import Track


@patch('races.models.recalculate_driver_stats_task')
class ResultFormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')

        self.track = Track.objects.create(
            name='Test Track',
            country='Test',
            image_url='https://test.com',
            length_km=2
        )

        self.team = Team.objects.create(
            name='Test Team',
            principal='Test Principal',
            base_country='Test',
            engine_supplier='Test',
            team_color='#F47600',
            logo_image_url='https://test.com',
        )

        self.driver = Driver.objects.create(
            name='Test Driver',
            owner=self.user,
            number=1,
            nationality='GB',
            age=25,
            team=self.team,
            image='https://test.com',
        )

        self.race = Race.objects.create(
            name='Test Race',
            round_number=1,
            weather='Mixed',
            track=self.track,
            laps=50,
            date=datetime.datetime(2025, 1, 1, 15, 0),
        )

        self.base_form_data = {
            'race': self.race.pk,
            'driver': self.driver.pk,
            'qualifying_position': 1,
            'finishing_position': 1,
            'points_awarded': 25,
            'fastest_lap': False,
            'status': 'Finished',
        }

    def test_finishing_position_with_non_finished_status__raises_error(self, mock_task):
        form_data = {**self.base_form_data,
                     'status': 'DNF',
                     'finishing_position': 1,
                     }
        form = ResultCreateForm(data=form_data, user=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)

    def test_finishing_position_null_with_finished_status__raises_error(self, mock_task):
        form_data = {**self.base_form_data, 'status': 'Finished', 'finishing_position': None}
        form = ResultCreateForm(data=form_data, user=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)

    def test_finishing_position_with_finished_status__success(self, mock_task):
        form_data = {**self.base_form_data}
        form = ResultCreateForm(data=form_data, user=self.user)
        self.assertTrue(form.is_valid())

    def test_driver_queryset_only_shows_own_drivers__success(self, mock_task):
        other_user = User.objects.create_user(username='other', password='test')
        other_driver = Driver.objects.create(
            name='Other Driver',
            owner=other_user,
            number=2,
            nationality='DE',
            age=30,
            team=self.team,
            image='https://test.com',
        )

        form = ResultCreateForm(user=self.user)

        self.assertIn(self.driver, form.fields['driver'].queryset)
        self.assertNotIn(other_driver, form.fields['driver'].queryset)