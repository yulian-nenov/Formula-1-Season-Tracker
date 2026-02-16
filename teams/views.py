from django.db.models import Sum
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

from races.models import Race
from teams.forms import TeamDeleteForm, CarDeleteForm, CarCreateForm, TeamCreateForm, TeamEditForm, CarEditForm
from teams.models import Team, CarModel


# Create your views here.

def team_list(request: HttpRequest) -> HttpResponse:
    teams = Team.objects.annotate(
        wins=Sum('drivers__wins', default=0),
    )

    context = {
        'teams': teams
    }

    return render(request, 'teams/list.html', context)

def team_details(request: HttpRequest, pk: int) -> HttpResponse:
    team = Team.objects.annotate(
        points=Sum('drivers__total_points', default=0),
        wins=Sum('drivers__wins', default=0),
        dnfs=Sum('drivers__dnfs', default=0),
        podiums=Sum('drivers__podiums', default=0),
    ).get(pk=pk)

    recent_races = (
        Race.objects
        .filter(results__driver__team=team)
        .distinct()
        .order_by("-date")[:3]
        .prefetch_related("results__driver")
    )

    context = {
        'team': team,
        'recent_races': recent_races
    }

    return render(request, 'teams/detail.html', context)

def team_create(request: HttpRequest) -> HttpResponse:
    team_form = TeamCreateForm(request.POST or None, request.FILES or None, prefix='team')
    car_form = CarCreateForm(request.POST or None, request.FILES or None, prefix='car')

    if request.method == "POST":
        if team_form.is_valid() and car_form.is_valid():
            team = team_form.save()

            car = car_form.save(commit=False)
            car.team = team
            car.save()

            return redirect("teams:list")

    context = {
        "team_form": team_form,
        "car_form": car_form,
        "page_title": "Create Team",
        "button_text": "Create Team"
    }

    return render(request, "shared/form.html", context)

def team_edit(request: HttpRequest, pk: int) -> HttpResponse:
    team = Team.objects.get(pk=pk)

    try:
        car = team.car
    except CarModel.DoesNotExist:
        car = None

    team_form = TeamEditForm(request.POST or None, instance=team, prefix='team')
    car_form = CarEditForm(request.POST or None, instance=car, prefix='car')

    if request.method == "POST":
        if team_form.is_valid() and car_form.is_valid():
            team_form.save()

            car = car_form.save(commit=False)
            car.team = team
            car_form.save()

            return redirect("teams:list")

    context = {
        "team_form": team_form,
        "car_form": car_form,
        "page_title": "Edit Team",
        "button_text": "Edit Team"
    }

    return render(request, "shared/form.html", context)


def team_delete(request: HttpRequest, pk: int) -> HttpResponse:
    team = Team.objects.get(pk=pk)
    car = team.car

    team_form = TeamDeleteForm(request.POST or None, instance=team, prefix='team')
    car_form = CarDeleteForm(request.POST or None, instance=car, prefix='car')


    if request.method == "POST":
        team.delete()
        return redirect("teams:list")

    context = {
        "team_form": team_form,
        "car_form": car_form,
        "page_title": "Delete Team",
        "button_text": "Delete Team"
    }

    return render(request, 'shared/form.html', context)
