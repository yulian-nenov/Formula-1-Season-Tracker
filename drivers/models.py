from django.core.validators import MinLengthValidator, MaxValueValidator
from django.db import models

from drivers.validators import AvailableSlotValidator


class Driver(models.Model):
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

    total_points = models.PositiveIntegerField(
        default=0,
        blank=True,
    )

    podiums = models.PositiveIntegerField(
        default=0,
        blank=True,
    )

    dnfs = models.PositiveIntegerField(
        default=0,
        blank=True,
    )

    wins = models.PositiveIntegerField(
        default=0,
        blank=True,
    )

    team = models.ForeignKey(
        'teams.Team',
        on_delete=models.CASCADE,
        related_name='drivers',
        validators=[
            AvailableSlotValidator(max_value=2, message='A team can have a maximum of 2 drivers!'),
        ]
    )

    image = models.URLField()
