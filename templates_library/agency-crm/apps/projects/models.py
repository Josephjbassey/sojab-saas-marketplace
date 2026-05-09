from django.db import models
from apps.common.models import BaseModel
from apps.organizations.models import Organization
from apps.clients.models import Client

class Project(BaseModel):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold'),
        ('cancelled', 'Cancelled'),
    ]

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='projects')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='projects')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return self.name
