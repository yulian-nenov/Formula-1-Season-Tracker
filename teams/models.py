from django.core.validators import MinLengthValidator, MinValueValidator
from django.db import models

from common.models import BaseStats
from teams.choices import TeamColorChoices


class Team(BaseStats):
    name = models.CharField(
        max_length=100,
        unique=True,
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

class CarModel(models.Model):
    name = models.CharField(
        max_length=100,
    )

    year = models.PositiveIntegerField(
        max_length=5,
    )

    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='cars',
    )

    power_unit = models.CharField(
        max_length=100,
    )

    is_being_used = models.BooleanField(
        null=True,
        blank=True,
        default=False,
    )
