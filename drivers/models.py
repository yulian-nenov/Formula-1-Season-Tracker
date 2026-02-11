from django.core.validators import MinLengthValidator, MaxValueValidator
from django.db import models

from common.models import BaseStats


class Driver(BaseStats):
    name = models.CharField(
        max_length=100,
        unique=True,
        validators=[
            MinLengthValidator(3),
        ]
    )

    number = models.PositiveIntegerField(
        unique=True,
        validators=[
            MaxValueValidator(99),
        ]
    )

    nationality = models.CharField(
        max_length=2,
        help_text='Enter country code.',
    )

    age = models.PositiveIntegerField()

    rookie_status = models.BooleanField(
        default=False,
        blank=True,
    )

    team = models.ForeignKey(
        'teams.Team',
        on_delete=models.CASCADE,
        related_name='drivers',
    )

    image = models.URLField()
