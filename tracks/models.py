from django.core.validators import MinValueValidator
from django.db import models

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
        decimal_places=2,
        validators=[
            MinValueValidator(1),
        ]
    )

    def __str__(self):
        return self.name
