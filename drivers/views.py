from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from rest_framework import permissions
from rest_framework.generics import RetrieveUpdateDestroyAPIView

from common.mixins import OwnerOnlyMixin
from drivers.forms import DriverCreateForm, DriverEditForm, DriverDeleteForm
from drivers.models import Driver
from drivers.serializers import DriverSerializer
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


class DriverCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Driver
    form_class = DriverCreateForm
    permission_required = 'drivers.add_driver'
    template_name = 'drivers/driver-form.html'
    success_url = reverse_lazy('drivers:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Create Driver'
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        driver = form.save(commit=False)
        driver.owner = self.request.user
        driver.save()
        return super().form_valid(form)

class DriverUpdateView(LoginRequiredMixin, PermissionRequiredMixin, OwnerOnlyMixin, UpdateView):
    model = Driver
    form_class = DriverEditForm
    permission_required = 'drivers.change_driver'
    template_name = 'drivers/driver-form.html'
    context_object_name = 'driver'

    def get_success_url(self):
        return reverse_lazy('drivers:details', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Edit Driver'
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class DriverDeleteView(LoginRequiredMixin, PermissionRequiredMixin, OwnerOnlyMixin, DeleteView):
    model = Driver
    context_object_name = 'driver'
    permission_required = 'drivers.delete_driver'
    template_name = 'drivers/driver-form.html'
    success_url = reverse_lazy('drivers:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = DriverDeleteForm(instance=self.object)
        context['page_title'] = 'Delete Driver'
        return context

# RESTful API
class IsOwnerOrStaff(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.team.owner == request.user

class DriverDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrStaff]
