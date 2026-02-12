from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from teams.models import Team


# Create your views here.

def team_list(request: HttpRequest) -> HttpResponse:
    return render(request, 'teams/list.html')

def team_details(request: HttpRequest, pk: int) -> HttpResponse:
    return render(request, 'teams/detail.html')

def team_create(request: HttpRequest, pk: int) -> HttpResponse:
    return render(request, 'teams/create-team.html')

def team_edit(request: HttpRequest, pk: int) -> HttpResponse:
    return render(request, 'teams/edit-team.html')

def team_delete(request: HttpRequest, pk: int) -> HttpResponse:
    return render(request, 'teams/delete-team.html')

