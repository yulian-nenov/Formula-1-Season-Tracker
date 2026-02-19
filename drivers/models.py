from django.core.validators import MinLengthValidator, MaxValueValidator
from django.db import models
from django.db.models import Sum

from drivers.validators import AvailableSlotValidator
from races.models import Result


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
        validators=[
            AvailableSlotValidator(max_value=2, message='A team can have a maximum of 2 drivers!'),
        ]
    )

    image = models.URLField()

    def __str__(self) -> str:
        return self.name

    def recalculate_driver_stats(self) -> None:
        results = self.results.all()

        self.total_points = (results.aggregate(total=Sum("points_awarded"))["total"] or 0)

        self.wins = results.filter(finishing_position=1).count()
        self.podiums = results.filter(finishing_position__lte=3).count()
        self.dnfs = results.filter(status="DNF").count()

        self.save()