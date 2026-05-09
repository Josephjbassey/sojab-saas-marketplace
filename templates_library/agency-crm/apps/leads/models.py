from django.db import models
from apps.common.models import BaseModel
from apps.organizations.models import Organization
from apps.clients.models import Client

class Lead(BaseModel):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('qualified', 'Qualified'),
        ('proposal', 'Proposal Sent'),
        ('won', 'Won'),
        ('lost', 'Lost'),
    ]

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='leads')
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    value = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return self.title
