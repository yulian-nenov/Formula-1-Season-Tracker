from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    profile_picture = models.ImageField(
        upload_to='profile/',
        default='profile/default.png',
    )
    favorite_tracks = models.ManyToManyField(
        'tracks.Track',
        blank=True,
        related_name='favorite_tracks',
    )
