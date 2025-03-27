from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

def welcome_tario(request):
    return render(request, 'welcome_tario.html')

class HomeView(LoginRequiredMixin, TemplateView):
    """Home page view (requires login)."""
    template_name = 'home.html'

class DashboardView(LoginRequiredMixin, TemplateView):
    """Dashboard view (requires login)."""
    template_name = 'dashboard.html'