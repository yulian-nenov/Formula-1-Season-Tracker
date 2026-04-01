from django.shortcuts import render
from django.views.generic import TemplateView

from races.models import Race

class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        latest_race = Race.objects.order_by('-date').prefetch_related("results__driver").first()
        context['latest_race'] = latest_race

        return context

def custom_403(request, exception):
    return render(request, "403.html", status=403)