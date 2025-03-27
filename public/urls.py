from django.contrib import admin
from django.urls import path
from .views import welcome_tario, HomeView, DashboardView

app_name = 'public'

urlpatterns = [
    path('', welcome_tario),
    path('home/', HomeView.as_view(), name = 'home'),
    path('dashboard/', DashboardView.as_view(), name = 'dashboard'),
]