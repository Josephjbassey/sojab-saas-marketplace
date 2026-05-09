from django.db import models
from django.conf import settings
from apps.common.models import BaseModel
from apps.templates_catalog.models import SaaSTemplate, TemplatePackage

class TemplatePurchase(BaseModel):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='purchases')
    organization = models.ForeignKey(
        'organizations.Organization',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='purchases'
    )
    template = models.ForeignKey(SaaSTemplate, on_delete=models.PROTECT, related_name='purchases')
    package = models.ForeignKey(TemplatePackage, on_delete=models.PROTECT, related_name='purchases')
    
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    transaction_id = models.CharField(max_length=255, blank=True, help_text="Transaction ID from payment gateway")
    
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Purchase {self.id} - {self.user.email} - {self.template.name} ({self.status})"
