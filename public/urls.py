from django.contrib import admin
from django.urls import path
from .views import welcome_tario

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', welcome_tario)
]