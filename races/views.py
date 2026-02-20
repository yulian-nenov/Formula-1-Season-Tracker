from django.db.models import Sum
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from drivers.models import Driver
from races.forms import RaceCreateForm, RaceEditForm, RaceDeleteForm, ResultCreateForm, ResultEditForm, ResultDeleteForm
from races.models import Race, Result, Track
from teams.models import Team


# Tracks

def track_list(request: HttpRequest) -> HttpResponse:
    tracks = Track.objects.all()

    context = {
        'tracks': tracks
    }

    return render(request, 'races/tracks/track-list.html', context)

def track_details(request: HttpRequest, pk: int) -> HttpResponse:
    track = Track.objects.prefetch_related('race_track').get(pk=pk)
    latest_winner = (
        Result.objects
        .filter(
            race__track=track,
            finishing_position=1
        ).order_by('-race__date')
        .first()
        )

    context = {
        'track': track,
        'latest_winner': latest_winner,
    }

    return render(request, 'races/tracks/track-details.html', context)

# Races

def race_list(request: HttpRequest) -> HttpResponse:
    races_with_results = Race.objects.prefetch_related('results')

    context = {
        'races_with_results': races_with_results
    }


    return render(request, 'races/race-list.html', context)

def race_details(request: HttpRequest, pk: int) -> HttpResponse:
    race = get_object_or_404(
        Race.objects.prefetch_related('results'),
        pk=pk
    )

    context = {
        'race': race
    }

    return render(request, 'races/race-details.html', context)

def race_create(request: HttpRequest) -> HttpResponse:
    form = RaceCreateForm(request.POST or None, request.FILES or None)

    if request.method == 'POST' and form.is_valid():
        form.save()

        return redirect('races:race_list')

    context = {
        'form': form,
        'page_title': 'Create Race',
        'model': 'Race',
    }

    return render( request, 'races/race-form.html', context)

def race_edit(request: HttpRequest, pk: int) -> HttpResponse:
    race = Race.objects.get(pk=pk)
    form = RaceEditForm(request.POST or None, request.FILES or None, instance=race)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('races:race_details', pk=pk)

    context = {
        'form': form,
        'page_title': 'Edit Race',
        'model': 'Race',
    }

    return render(request, 'races/race-form.html', context)

def race_delete(request: HttpRequest, pk: int) -> HttpResponse:
    race = Race.objects.get(pk=pk)
    form = RaceDeleteForm(request.POST or None, request.FILES or None, instance=race)

    if request.method == 'POST' and form.is_valid():
        race.delete()

        return redirect('races:race_list')

    context = {
        'form': form,
        'page_title': 'Delete Race',
        'model': 'Race',
    }

    return render(request, 'races/race-form.html', context)

# Results

def result_add(request: HttpRequest) -> HttpResponse:
    form = ResultCreateForm(request.POST or None, request.FILES or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('races:race_list')

    context = {
        'form': form,
        'page_title': 'Add Result',
        'model': 'Result',
    }

    return render(request, 'races/race-form.html', context)

def result_edit(request: HttpRequest, pk: int) -> HttpResponse:
    result = Result.objects.get(pk=pk)
    form = ResultEditForm(request.POST or None, request.FILES or None, instance=result)

    if request.method == 'POST' and form.is_valid():
        form.save()

        return redirect('races:race_details', result.race.pk)

    context = {
        'form': form,
        'page_title': 'Edit Result',
        'model': 'Result',
    }

    return render(request, 'races/race-form.html', context)

def result_delete(request: HttpRequest, pk: int) -> HttpResponse:
    result = Result.objects.get(pk=pk)
    form = ResultDeleteForm(request.POST or None, request.FILES or None, instance=result)

    if request.method == 'POST' and form.is_valid():
        result.delete()

        return redirect('races:race_list')

    context = {
        'form': form,
        'page_title': 'Delete Result',
        'model': 'Result',
    }

    return render(request, 'races/race-form.html', context)

# Standings

def standings(request: HttpRequest) -> HttpResponse:
    drivers = Driver.objects.all().order_by('-total_points', 'name')
    teams = Team.objects.annotate(
        points=Sum('drivers__total_points', default=0)
    ).order_by('-points', 'name')

    context = {
        'drivers': drivers,
        'teams': teams,
    }

    return render(request, 'races/results/standings.html', context)
