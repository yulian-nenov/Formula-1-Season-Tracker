from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, MaxValueValidator
from django.db import models


class Driver(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        validators=[
            MinLengthValidator(3),
        ]
    )

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='drivers',
        null=True,
        blank=True,
    )

    number = models.PositiveIntegerField(
        unique=True,
        validators=[
            MaxValueValidator(99),
        ]
    )

    nationality = models.CharField(
        max_length=2,
    )

    age = models.PositiveIntegerField()

    rookie_status = models.BooleanField(
        default=False,
        null=True,
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
    )

    image = models.URLField()

    def __str__(self) -> str:
        return self.name
