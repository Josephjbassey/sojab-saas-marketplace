from django.db import models
from django.core.exceptions import ValidationError
from apps.common.models import BaseModel
from apps.organizations.models import Organization
from apps.clients.models import Client

class Project(BaseModel):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold'),
        ('cancelled', 'Cancelled'),
    )

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='projects')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='projects')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    def clean(self):
        super().clean()
        if self.client.organization != self.organization:
            raise ValidationError({
                'client': f"Client '{self.client.name}' must belong to the same organization as the project."
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
