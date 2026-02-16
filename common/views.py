from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from races.models import Race


def home(request: HttpRequest) -> HttpResponse:
    latest_race = Race.objects.order_by('-date').prefetch_related("results__driver").first()

    context = {
        'latest_race': latest_race,
    }

    return render(request, 'home.html', context)