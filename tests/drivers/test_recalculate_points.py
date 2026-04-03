from datetime import datetime, timezone
from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase

from drivers.models import Driver
from drivers.tasks import recalculate_driver_stats_task
from races.models import Result, Race
from teams.models import Team
from tracks.models import Track

@patch('races.models.recalculate_driver_stats_task')
class RecalculateDriverStatsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')

        self.track = Track.objects.create(
            name='Test Track',
            country='Test Country',
            length_km=5.00,
        )

        self.team = Team.objects.create(
            name='Test Team',
            principal='Test Principal',
            base_country='Test Country',
            engine_supplier='Test Supplier',
            team_color='#F47600',
            logo_image_url='https://test.com',
            owner=self.user,
        )

        self.driver = Driver.objects.create(
            name='Test Driver',
            number=33,
            nationality='DE',
            age=25,
            team=self.team,
            image='https://test.com',
        )

        self.race = Race.objects.create(
            name='Test Race',
            round_number=1,
            weather='Sunny',
            track=self.track,
            laps=50,
            date=datetime(2025, 1, 1, 15, 0, tzinfo=timezone.utc),
        )

    def _create_result(self, finishing_position, status, points, qualifying_position):
        result = Result.objects.create(
                race=self.race,
                driver=self.driver,
                qualifying_position=qualifying_position,
                finishing_position=finishing_position,
                points_awarded=points,
                status=status,
            )
        return result

    def test_recalculate_stats__points_and_wins(self, mock_task):
        self._create_result(finishing_position=1, status='Finished', points=25, qualifying_position=2)
        recalculate_driver_stats_task(self.driver.pk)
        self.driver.refresh_from_db()
        self.assertEqual(self.driver.total_points, 25)
        self.assertEqual(self.driver.wins, 1)
