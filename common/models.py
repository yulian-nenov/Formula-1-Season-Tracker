from django.db import models

class BaseStats(models.Model):
    total_points = models.PositiveIntegerField(
        default=0,
    )

    podiums = models.PositiveIntegerField(
        default=0,
    )

    dnfs = models.PositiveIntegerField(
        default=0,
    )

    wins = models.PositiveIntegerField(
        default=0,
    )

    class Meta:
        abstract = True
