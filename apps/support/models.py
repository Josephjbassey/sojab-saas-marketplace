from django.db import models
from django.conf import settings
from apps.common.models import BaseModel
from apps.templates_catalog.models import SaaSTemplate
from apps.purchases.models import TemplatePurchase

class CustomizationRequest(BaseModel):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewing', 'Reviewing'),
        ('quoted', 'Quoted'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='customization_requests')
    organization = models.ForeignKey('organizations.Organization', on_delete=models.SET_NULL, null=True, blank=True, related_name='customization_requests')
    template = models.ForeignKey(SaaSTemplate, on_delete=models.CASCADE, related_name='customization_requests')
    purchase = models.ForeignKey(TemplatePurchase, on_delete=models.SET_NULL, null=True, blank=True, related_name='customization_requests')
    
    subject = models.CharField(max_length=255)
    description = models.TextField()
    budget_expectation = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_notes = models.TextField(blank=True)

    def __str__(self):
        return f"Customization Request for {self.template.name} - {self.user.email} ({self.status})"
