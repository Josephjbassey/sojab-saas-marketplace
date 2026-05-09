from django.db import models
from django.core.exceptions import ValidationError
from apps.common.models import BaseModel
from apps.organizations.models import Organization
from apps.clients.models import Client
from apps.projects.models import Project

class Invoice(BaseModel):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
        ('cancelled', 'Cancelled'),
    )

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='invoices')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='invoices')
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True)
    number = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')

    def clean(self):
        super().clean()
        if self.client:
            if self.client.organization != self.organization:
                raise ValidationError({
                    'client': f"Client '{self.client.name}' must belong to the same organization as the invoice."
                })
        if self.project:
            if self.project.organization != self.organization:
                raise ValidationError({
                    'project': f"Project '{self.project.name}' must belong to the same organization as the invoice."
                })
            if self.project.client != self.client:
                raise ValidationError({
                    'project': f"Project '{self.project.name}' must belong to the same client as the invoice."
                })

    def save(self, *args, **kwargs):
        validate = kwargs.pop('validate', True)
        if validate:
            self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Invoice {self.number}"
