from django.db import models
from django.conf import settings
from django.utils.text import slugify
from apps.common.models import BaseModel
from apps.organizations.models import Organization
from apps.purchases.models import TemplatePurchase
from apps.templates_catalog.models import SaaSTemplate

class GeneratedProject(BaseModel):
    STATUS_DRAFT = 'draft'
    STATUS_QUEUED = 'queued'
    STATUS_PREPARING = 'preparing'
    STATUS_DELIVERED = 'delivered'
    STATUS_FAILED = 'failed'
    STATUS_CANCELLED = 'cancelled'

    STATUS_CHOICES = [
        (STATUS_DRAFT, 'Draft'),
        (STATUS_QUEUED, 'Queued'),
        (STATUS_PREPARING, 'Preparing'),
        (STATUS_DELIVERED, 'Delivered'),
        (STATUS_FAILED, 'Failed'),
        (STATUS_CANCELLED, 'Cancelled'),
    ]

    purchase = models.OneToOneField(
        TemplatePurchase,
        on_delete=models.PROTECT,
        related_name='generated_project'
    )
    template = models.ForeignKey(
        SaaSTemplate,
        on_delete=models.PROTECT,
        related_name='generated_projects'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='generated_projects'
    )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='generated_projects'
    )

    project_name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_DRAFT
    )

    github_repo_url = models.URLField(max_length=512, blank=True)
    zip_file = models.FileField(upload_to='generated_projects/zips/', null=True, blank=True)
    deployment_url = models.URLField(max_length=512, blank=True)

    admin_notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Generated Project"
        verbose_name_plural = "Generated Projects"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.project_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.project_name} ({self.get_status_display()})"


class ProjectConfiguration(BaseModel):
    generated_project = models.OneToOneField(
        GeneratedProject,
        on_delete=models.CASCADE,
        related_name='configuration'
    )

    brand_name = models.CharField(max_length=255, blank=True)
    primary_color = models.CharField(
        max_length=20,
        blank=True,
        help_text="Hex code or CSS color name"
    )
    payment_provider = models.CharField(
        max_length=50,
        blank=True,
        help_text="Target payment provider (e.g., Stripe, Paystack)"
    )
    cms_enabled = models.BooleanField(default=True)
    deployment_target = models.CharField(
        max_length=100,
        blank=True,
        help_text="e.g., Vercel, Railway, Heroku"
    )

    extra_config = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"Config for {self.generated_project.project_name}"
