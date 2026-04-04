from django.test import TestCase

from teams.models import Team


class TeamModelTest(TestCase):
    def test_team_str_method(self):
        team = Team(name="Test Team")
        self.assertEqual(str(team), "Test Team")
