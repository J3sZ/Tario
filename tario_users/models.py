from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from tenants.models import Tenant  # Importa el modelo Tenant

class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    paid_until = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
  

    # Relación con el inquilino (tenant)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='users')

    def __str__(self):
        return self.username