from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views.generic import CreateView, DetailView
from django.urls import reverse_lazy

from accounts.forms import RegisterForm


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "accounts/account_form.html"
    context_object_name = "form"
    success_url = reverse_lazy("accounts:login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Create Account'
        return context

class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'accounts/profile_detail.html'
