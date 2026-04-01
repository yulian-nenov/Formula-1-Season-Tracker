from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Sum, QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, DeleteView

from common.mixins import OwnerOnlyMixin
from races.models import Race
from teams.forms import TeamDeleteForm, CarDeleteForm, CarCreateForm, TeamCreateForm, TeamEditForm, CarEditForm
from teams.models import Team, CarModel


# Create your views here.

class TeamListView(ListView):
    model = Team
    context_object_name = 'teams'
    queryset = Team.objects.annotate(wins=Sum('drivers__wins', default=0),)

class TeamDetailsView(DetailView):
    model = Team
    context_object_name = 'team'
    pk_url_kwarg = 'pk'

    def get_queryset(self) -> QuerySet:
        return Team.objects.annotate(
            points=Sum('drivers__total_points', default=0),
            races=Sum('drivers__races', default=0),
            wins=Sum('drivers__wins', default=0),
            dnfs=Sum('drivers__dnfs', default=0),
            podiums=Sum('drivers__podiums', default=0),
        )

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)

        team = self.object

        recent_races = (
            Race.objects
            .filter(results__driver__team=team)
            .distinct()
            .order_by("-date")[:3]
            .prefetch_related("results__driver")
        )

        context['recent_races'] = recent_races
        return context

class TeamCreateView(LoginRequiredMixin, PermissionRequiredMixin, View):
    template_name = "teams/team-form.html"
    permission_required = 'teams.add_team'

    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            'team_form': TeamCreateForm(prefix='team'),
            'car_form': CarCreateForm(prefix='car'),
            'page_title': 'Create Team'
        }
        return render(request, self.template_name, context)

    def post(self, request: HttpRequest) -> HttpResponse:
        team_form = TeamCreateForm(request.POST or None, request.FILES or None, prefix='team')
        car_form = CarCreateForm(request.POST or None, request.FILES or None, prefix='car')

        if team_form.is_valid() and car_form.is_valid():
            team = team_form.save(commit=False)
            team.owner = request.user
            team.save()

            car = car_form.save(commit=False)
            car.team = team
            car.save()

            return redirect("teams:list")

        context = {
            "team_form": team_form,
            "car_form": car_form,
            "page_title": "Create Team"
        }

        return render(request, "teams/team-form.html", context)

@login_required
@permission_required('teams.change_team', raise_exception=True)
def team_edit(request: HttpRequest, pk: int) -> HttpResponse:
    team = Team.objects.get(pk=pk)

    if not request.user == team.owner and not request.user.is_superuser:
        raise PermissionDenied

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

            return redirect("teams:details", team.pk)

    context = {
        "team_form": team_form,
        "car_form": car_form,
        "page_title": "Edit Team",
    }

    return render(request, "teams/team-form.html", context)

class TeamDeleteView(LoginRequiredMixin, PermissionRequiredMixin, OwnerOnlyMixin, DeleteView):
    model = Team
    template_name = "teams/team-form.html"
    permission_required = 'teams.delete_team'
    success_url = reverse_lazy("teams:list")
    context_object_name = "team"

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)

        team = self.object
        try:
            car = team.car
        except CarModel.DoesNotExist:
            car = None

        context['team_form'] = TeamDeleteForm(instance=team, prefix='team')
        context['car_form'] = CarDeleteForm(instance=car, prefix='car')
        context['page_title'] = 'Delete Team'

        return context
