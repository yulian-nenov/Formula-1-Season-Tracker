from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


# Tracks

def track_list(request: HttpRequest) -> HttpResponse:
    return render(request, 'races/tracks/track-list.html')

def track_details(request: HttpRequest, pk: int) -> HttpResponse:
    return render(request, 'races/tracks/track-details.html')

# Races

def race_list(request: HttpRequest) -> HttpResponse:
    return render(request, 'races/race-list.html')

def race_details(request: HttpRequest, pk: int) -> HttpResponse:
    return render(request, 'races/race-details.html')

def race_create(request: HttpRequest, pk: int) -> HttpResponse:
    return render( request, 'races/race-create.html')

def race_edit(request: HttpRequest, pk: int) -> HttpResponse:
    return render(request, 'races/race-edit.html')

def race_delete(request: HttpRequest, pk: int) -> HttpResponse:
    return render(request, 'races/race-delete.html')

# Results

def result_add(request: HttpRequest, pk: int) -> HttpResponse:
    return render(request, 'races/results/result-add.html')

def result_edit(request: HttpRequest, pk: int) -> HttpResponse:
    return render(request, 'races/results/result-edit.html')

def result_delete(request: HttpRequest, pk: int) -> HttpResponse:
    return render(request, 'races/results/result-delete.html')

# Standings

def standings(request: HttpRequest) -> HttpResponse:
    return render(request, 'races/results/standings.html')
