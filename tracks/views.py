from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from races.models import Result
from tracks.forms import TrackCreateForm, TrackUpdateForm, TrackDeleteForm
from tracks.models import Track


# Create your views here.

class TrackListView(ListView):
    model = Track
    context_object_name = 'tracks'

class TrackDetailView(DetailView):
    model = Track
    context_object_name = 'track'

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)

        latest_winner = (
            Result.objects
            .filter(
                race__track=context['track'],
                finishing_position=1
            ).order_by('-race__date')
            .first()
        )

        context['latest_winner'] = latest_winner

        return context

class TrackCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Track
    form_class = TrackCreateForm
    permission_required = 'tracks.add_track'
    template_name = 'tracks/track_form.html'
    success_url = reverse_lazy('tracks:list')

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Create Track'
        return context

class TrackUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Track
    form_class = TrackUpdateForm
    permission_required = 'tracks.change_track'
    template_name = 'tracks/track_form.html'

    def get_success_url(self, **kwargs):
        return reverse_lazy('tracks:details', kwargs={'pk': self.object.pk})

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Update Track'
        return context

class TrackDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Track
    permission_required = 'tracks.delete_track'
    template_name = 'tracks/track_form.html'
    success_url = reverse_lazy('tracks:list')

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Delete Track'
        context['form'] = TrackDeleteForm(instance=self.object)
        return context

