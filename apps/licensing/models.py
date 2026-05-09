from django.db import models, transaction
from django.conf import settings
from apps.common.models import BaseModel
from apps.templates_catalog.models import SaaSTemplate
from apps.purchases.models import TemplatePurchase
from apps.organizations.models import Organization

class TemplateVersion(BaseModel):
    template = models.ForeignKey(
        SaaSTemplate,
        on_delete=models.CASCADE,
        related_name='versions'
    )
    version = models.CharField(max_length=50)
    release_date = models.DateField()
    changelog = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)
    is_latest = models.BooleanField(default=False)

    class Meta:
        ordering = ['-release_date', '-created_at']
        unique_together = ('template', 'version')
        verbose_name = "Template Version"
        verbose_name_plural = "Template Versions"

    def __str__(self):
        return f"{self.template.name} v{self.version}"

    def save(self, *args, **kwargs):
        with transaction.atomic():
            super().save(*args, **kwargs)
            if self.is_latest:
                # Ensure only one version is latest for this template
                TemplateVersion.objects.filter(
                    template=self.template,
                    is_latest=True
                ).exclude(pk=self.pk).update(is_latest=False)


class TemplateLicense(BaseModel):
    TYPE_PERSONAL = 'personal'
    TYPE_COMMERCIAL = 'commercial'
    TYPE_AGENCY = 'agency'

    TYPE_CHOICES = [
        (TYPE_PERSONAL, 'Personal'),
        (TYPE_COMMERCIAL, 'Commercial'),
        (TYPE_AGENCY, 'Agency'),
    ]

    STATUS_ACTIVE = 'active'
    STATUS_SUSPENDED = 'suspended'
    STATUS_EXPIRED = 'expired'
    STATUS_REVOKED = 'revoked'

    STATUS_CHOICES = [
        (STATUS_ACTIVE, 'Active'),
        (STATUS_SUSPENDED, 'Suspended'),
        (STATUS_EXPIRED, 'Expired'),
        (STATUS_REVOKED, 'Revoked'),
    ]

    license_key = models.CharField(max_length=255, unique=True)
    template = models.ForeignKey(
        SaaSTemplate,
        on_delete=models.CASCADE,
        related_name='licenses'
    )
    purchase = models.OneToOneField(
        TemplatePurchase,
        on_delete=models.CASCADE,
        related_name='license'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='template_licenses'
    )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='template_licenses'
    )

    license_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default=TYPE_PERSONAL
    )
    allowed_end_products = models.PositiveIntegerField(default=1)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_ACTIVE
    )

    issued_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['-issued_at']
        verbose_name = "Template License"
        verbose_name_plural = "Template Licenses"

    def __str__(self):
        return f"License {self.license_key[:8]}... for {self.template.name}"

    @property
    def is_active(self):
        return self.status == self.STATUS_ACTIVE
