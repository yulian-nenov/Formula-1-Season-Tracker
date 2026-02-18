from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from races.forms import RaceCreateForm, RaceEditForm, RaceDeleteForm
from races.models import Race


# Tracks

def track_list(request: HttpRequest) -> HttpResponse:
    return render(request, 'races/tracks/track-list.html')

def track_details(request: HttpRequest, pk: int) -> HttpResponse:
    return render(request, 'races/tracks/track-details.html')

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

def result_add(request: HttpRequest, ) -> HttpResponse:
    return render(request, 'races/results/result-add.html')

def result_edit(request: HttpRequest, pk: int) -> HttpResponse:
    return render(request, 'races/results/result-edit.html')

def result_delete(request: HttpRequest, pk: int) -> HttpResponse:
    return render(request, 'races/results/result-delete.html')

# Standings

def standings(request: HttpRequest) -> HttpResponse:
    return render(request, 'races/results/standings.html')
