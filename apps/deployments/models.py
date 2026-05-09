from django.db import models
from django.conf import settings
from apps.common.models import BaseModel
from apps.templates_catalog.models import SaaSTemplate
from apps.purchases.models import TemplatePurchase

class ClientProject(BaseModel):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('archived', 'Archived'),
        ('suspended', 'Suspended'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='client_projects')
    organization = models.ForeignKey(
        'organizations.Organization',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='client_projects'
    )
    template = models.ForeignKey(SaaSTemplate, on_delete=models.PROTECT, related_name='client_projects')
    purchase = models.ForeignKey(TemplatePurchase, on_delete=models.PROTECT, related_name='client_projects')
    
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    project_url = models.URLField(blank=True, help_text="The live URL of the client's project")
    repository_url = models.URLField(blank=True, help_text="The repository URL for the client's project")

    def __str__(self):
        return f"{self.name} ({self.user.email})"

class DeploymentRequest(BaseModel):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('building', 'Building'),
        ('deployed', 'Deployed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]

    project = models.ForeignKey(ClientProject, on_delete=models.CASCADE, related_name='deployment_requests')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='deployment_requests')
    organization = models.ForeignKey(
        'organizations.Organization',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='deployment_requests'
    )
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_notes = models.TextField(blank=True)
    delivery_link = models.URLField(blank=True, help_text="Link to the codebase (ZIP, GitHub repo, etc.)")

    def __str__(self):
        return f"Deployment Request for {self.project.name} - {self.status}"
