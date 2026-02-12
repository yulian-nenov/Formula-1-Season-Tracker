from django.core.validators import MaxValueValidator
from django.db import models

from races.choices import WeatherChoices, StatusChoices


class Track(models.Model):
    name = models.CharField(
        max_length=100,
    )

    country = models.CharField(
        max_length=100,
    )

    image_url = models.URLField(
        null=True,
        blank=True,
    )

    length_km = models.DecimalField(
        max_digits=3,
        decimal_places=2
    )

class Race(models.Model):
    name = models.CharField(
        max_length=100,
    )

    round_number = models.PositiveIntegerField(
        validators=[
            MaxValueValidator(24)
        ],
    )

    weather = models.CharField(
        max_length=50,
        choices=WeatherChoices.choices
    )

    track = models.ForeignKey(
        "Track",
        on_delete=models.CASCADE,
        related_name="race_track",
    )

    laps = models.PositiveIntegerField()

    date = models.DateField()

    drivers = models.ManyToManyField(
        "drivers.Driver",
        through="Result",
        related_name="races",
    )


class Result(models.Model):
    race = models.ForeignKey(
        Race,
        on_delete=models.CASCADE,
        related_name="results",
    )

    driver = models.ForeignKey(
        "drivers.Driver",
        on_delete=models.CASCADE,
        related_name="results",
    )

    qualifying_position = models.PositiveIntegerField(
        validators=[
            MaxValueValidator(20)
        ]
    )
    finishing_position = models.PositiveIntegerField(
        validators=[
            MaxValueValidator(20)
        ]
    )

    points_awarded = models.PositiveIntegerField(
        default=0,
        blank=True,
        validators=[
            MaxValueValidator(25)
        ]
    )

    fastest_lap = models.BooleanField(
        default=False,
        blank=True,
    )

    status = models.CharField(
        max_length=50,
        choices=StatusChoices.choices,
    )

    class Meta:
        unique_together = [
            ("race", "driver"),
            ("race", "finishing_position")
        ]