from django.core.validators import MinLengthValidator
from django.db import models

from common.models import BaseTimeStamp
from teams.choices import TeamColorChoices


class Team(BaseTimeStamp):
    name = models.CharField(
        max_length=100,
        unique=True,
        validators=[
            MinLengthValidator(3)
        ]
    )

    principal = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(3)
        ]
    )

    base_country = models.CharField(
        max_length=50,
    )

    engine_supplier = models.CharField(
        max_length=50,
    )

    team_color = models.CharField(
        max_length=15,
        choices=TeamColorChoices.choices,
    )

    logo_image_url = models.URLField()

    def __str__(self):
        return self.name


class CarModel(models.Model):
    name = models.CharField(
        unique=True,
        max_length=100,
    )

    year = models.PositiveIntegerField()

    team = models.OneToOneField(
        "Team",
        on_delete=models.CASCADE,
        related_name='car',
    )

    power_unit = models.CharField(
        max_length=100,
    )

    in_use = models.BooleanField(
        null=True,
        blank=True,
        default=False,
    )
