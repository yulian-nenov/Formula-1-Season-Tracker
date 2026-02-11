from django.db import models


class WeatherChoices(models.TextChoices):
    SUNNY = 'Sunny', 'Sunny'
    RAINY = 'Rainy', 'Rainy'
    MIXED = 'Mixed', 'Mixed'


class StatusChoices(models.TextChoices):
    FINISHED = 'Finished', 'Finished'
    DNF = 'DNF', 'Did Not Finish'
    DSQ = 'DSQ', 'Disqualified'
    DNS = 'DNS', 'Did Not Start'
