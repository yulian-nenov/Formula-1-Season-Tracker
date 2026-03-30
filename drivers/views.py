from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from drivers.forms import DriverCreateForm, DriverEditForm, DriverDeleteForm
from drivers.models import Driver
from races.models import Result

class DriverListView(ListView):
    model = Driver
    context_object_name = 'drivers'
    queryset = Driver.objects.all()

class DriverDetailsView(DetailView):
    model = Driver
    context_object_name = 'driver'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        driver = self.object
        recent_results = Result.objects.filter(driver=driver).order_by('-race__date')[:3]
        races_participated = driver.races.count()

        context['recent_results'] = recent_results
        context['races_participated'] = races_participated

        return context

class DriverCreateView(CreateView):
    model = Driver
    form_class = DriverCreateForm
    template_name = 'drivers/driver-form.html'
    success_url = reverse_lazy('drivers:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Create Driver'
        return context

class DriverUpdateView(UpdateView):
    model = Driver
    form_class = DriverEditForm
    template_name = 'drivers/driver-form.html'
    context_object_name = 'driver'

    def get_success_url(self):
        return reverse_lazy('drivers:details', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Edit Driver'
        return context

class DriverDeleteView(DeleteView):
    model = Driver
    context_object_name = 'driver'
    template_name = 'drivers/driver-form.html'
    success_url = reverse_lazy('drivers:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = DriverDeleteForm(instance=self.object)
        context['page_title'] = 'Delete Driver'
        return context