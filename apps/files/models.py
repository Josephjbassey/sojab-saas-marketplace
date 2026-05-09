import os
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from apps.common.models import BaseModel
from apps.organizations.models import Organization

def validate_file_size(value):
    # Default limit 50MB
    limit = 50 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 50 MiB.')

class ManagedFile(BaseModel):
    PURPOSE_TEMPLATE_SCREENSHOT = 'template_screenshot'
    PURPOSE_CLIENT_BRAND_ASSET = 'client_brand_asset'
    PURPOSE_DELIVERY_ZIP = 'delivery_zip'
    PURPOSE_INVOICE = 'invoice'
    PURPOSE_DOCUMENT = 'document'
    PURPOSE_OTHER = 'other'

    PURPOSE_CHOICES = [
        (PURPOSE_TEMPLATE_SCREENSHOT, 'Template Screenshot'),
        (PURPOSE_CLIENT_BRAND_ASSET, 'Client Brand Asset'),
        (PURPOSE_DELIVERY_ZIP, 'Delivery Zip'),
        (PURPOSE_INVOICE, 'Invoice'),
        (PURPOSE_DOCUMENT, 'Document'),
        (PURPOSE_OTHER, 'Other'),
    ]

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_files'
    )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_files'
    )

    file = models.FileField(
        upload_to='managed_files/%Y/%m/%d/',
        validators=[validate_file_size]
    )

    original_filename = models.CharField(max_length=255)
    content_type = models.CharField(max_length=100, blank=True)
    size = models.BigIntegerField(help_text="File size in bytes")

    purpose = models.CharField(
        max_length=50,
        choices=PURPOSE_CHOICES,
        default='other'
    )

    def save(self, *args, **kwargs):
        if not self.original_filename and self.file:
            self.original_filename = self.file.name
        if not self.size and self.file:
            self.size = self.file.size
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.original_filename} ({self.get_purpose_display()})"

    class Meta:
        verbose_name = "Managed File"
        verbose_name_plural = "Managed Files"
