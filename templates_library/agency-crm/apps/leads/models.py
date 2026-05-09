from django.db import models
from django.core.exceptions import ValidationError
from apps.common.models import BaseModel
from apps.organizations.models import Organization
from apps.clients.models import Client

class Lead(BaseModel):
    STATUS_CHOICES = (
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('qualified', 'Qualified'),
        ('proposal', 'Proposal Sent'),
        ('won', 'Won'),
        ('lost', 'Lost'),
    )

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='leads')
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    value = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def clean(self):
        super().clean()
        if self.client and self.client.organization != self.organization:
            raise ValidationError({
                'client': f"Client '{self.client.name}' must belong to the same organization as the lead."
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
