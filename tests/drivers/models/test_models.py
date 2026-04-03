from django.test import TestCase

from drivers.models import Driver


class DriverModelTests(TestCase):
    def test_driver_str_method(self):
        driver = Driver(name='Test Driver')
        self.assertEqual(str(driver), 'Test Driver')
