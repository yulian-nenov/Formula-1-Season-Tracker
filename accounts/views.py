from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy

from accounts.forms import RegisterForm, ProfileForm, UserForm
from accounts.models import Profile

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
    model = Profile
    template_name = 'accounts/profile_detail.html'
    context_object_name = 'profile'

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'accounts/update_form.html'

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.POST:
            context['user_form'] = UserForm(
                self.request.POST,
                instance=self.request.user
            )
        else:
            context['user_form'] = UserForm(instance=self.request.user)

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        user_form = context['user_form']

        if user_form.is_valid():
            user = user_form.save()
            self.object = form.save()
            return redirect('accounts:detail', pk=user.pk)
        else:
            return self.form_invalid(form)

class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'accounts/delete_form.html'
    success_url = reverse_lazy('accounts:login')

    def get_object(self, queryset=None):
        return self.request.user
