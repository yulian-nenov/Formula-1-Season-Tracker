from django.db import models


class TeamColorChoices(models.TextChoices):
    CYAN = '#00D7B6', 'Cyan'
    NAVY = '#003773', 'Navy'
    GREEN = '#037A68', 'Green'
    GRAY = '#8F9296', 'Gray'
    PAPAYA = '#F47600', 'Papaya'
    PINK = '#F282B4', 'Pink'
    RED = '#ED1131', 'Red'
    BLUE = '#00A0DE', 'Blue'
