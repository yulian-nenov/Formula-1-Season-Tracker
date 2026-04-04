from unittest.mock import patch

from django.test import TestCase

from races.models import Result


class ResultModelTests(TestCase):
    @patch('races.models.recalculate_driver_stats_task')
    def test_display_finishing_position_with_dnf_status(self, mock_task):
        result = Result(
            status='DNF',
            finishing_position=None,
        )
        self.assertEqual(result.status, 'DNF')

    @patch('races.models.recalculate_driver_stats_task')
    def test_display_finishing_position_with_status_finished(self, mock_task):
        result = Result(status='FINISHED', finishing_position=3)
        self.assertEqual(result.display_finishing_position, 'P3')