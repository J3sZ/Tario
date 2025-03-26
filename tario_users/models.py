from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Campos adicionales (opcional)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    tenant = models.ForeignKey('tenants.Tenant', on_delete=models.CASCADE, null=True, blank=True)  
    domain_name = models.CharField(max_length=100, blank=True, null=True)
    tenant_name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'tario_users_customuser'


    def __str__(self):
        return self.username