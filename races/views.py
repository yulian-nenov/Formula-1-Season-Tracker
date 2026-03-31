from django.db.models import Sum
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from drivers.models import Driver
from races.forms import RaceCreateForm, RaceEditForm, RaceDeleteForm, ResultCreateForm, ResultEditForm, ResultDeleteForm
from races.models import Race, Result
from teams.models import Team

# Races

class RaceListView(ListView):
    model = Race
    queryset = Race.objects.prefetch_related('results').order_by('-date')
    context_object_name = 'races_with_results'

class RaceDetailView(DetailView):
    model = Race
    context_object_name = 'race'

class RaceCreateView(CreateView):
    model = Race
    form_class = RaceCreateForm
    template_name = 'races/race-form.html'
    success_url = reverse_lazy('races:race_list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Create Race'
        context['model'] = 'Race'
        return context

class RaceUpdateView(UpdateView):
    model = Race
    form_class = RaceEditForm
    template_name = 'races/race-form.html'

    def get_success_url(self):
        return reverse_lazy('races:race_details', kwargs={'pk': self.object.pk})

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Update Race'
        context['model'] = 'Race'
        return context

class RaceDeleteView(DeleteView):
    model = Race
    template_name = 'races/race-form.html'
    success_url = reverse_lazy('races:race_list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        context['form'] = RaceDeleteForm(instance=self.object)
        context['page_title'] = 'Delete Race'
        context['model'] = 'Race'

        return context

# Results

class ResultCreateView(CreateView):
    model = Result
    form_class = ResultCreateForm
    template_name = 'races/race-form.html'
    success_url = reverse_lazy('races:race_list')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Create Result'
        context['model'] = 'Result'
        return context

class ResultUpdateView(UpdateView):
    model = Result
    form_class = ResultEditForm
    template_name = 'races/race-form.html'

    def get_success_url(self):
        return reverse_lazy('races:race_details', kwargs={'pk': self.object.race.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Create Result'
        context['model'] = 'Result'
        return context

class ResultDeleteView(DeleteView):
    model = Result
    template_name = 'races/race-form.html'

    def get_success_url(self):
        return reverse_lazy('races:race_details', kwargs={'pk': self.object.race.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['form'] = ResultDeleteForm(instance=self.object)
        context['page_title'] = 'Delete Result'
        context['model'] = 'Result'

        return context

# Standings

class StandingsView(View):
    template_name = 'races/results/standings.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        drivers = Driver.objects.all().order_by('-total_points', 'name')
        teams = Team.objects.annotate(
            points=Sum('drivers__total_points', default=0)
        ).order_by('-points', 'name')

        context = {
            'drivers': drivers,
            'teams': teams,
        }

        return render(request, self.template_name, context)
