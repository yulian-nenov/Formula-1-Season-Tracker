from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db import models

from accounts.validators import MaxSizeValidator


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    profile_picture = models.ImageField(
        upload_to='profile/',
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(['png', 'jpg', 'jpeg']),
            MaxSizeValidator(max_size=3),
        ],
    )
    favorite_tracks = models.ManyToManyField(
        'tracks.Track',
        blank=True,
        related_name='favorite_tracks',
    )
