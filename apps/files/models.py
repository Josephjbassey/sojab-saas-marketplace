import os
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from apps.common.models import BaseModel
from apps.organizations.models import Organization

def validate_file_size(value):
    # Default limit: 50MB
    filesize = value.size
    limit = getattr(settings, 'MAX_UPLOAD_SIZE', 52428800)
    if filesize > limit:
        raise ValidationError(f"The maximum file size is {limit/1024/1024}MB")

class ManagedFile(BaseModel):
    PURPOSE_CHOICES = [
        ('template_screenshot', 'Template Screenshot'),
        ('client_brand_asset', 'Client Brand Asset'),
        ('delivery_zip', 'Delivery ZIP'),
        ('invoice', 'Invoice'),
        ('document', 'Document'),
        ('other', 'Other'),
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
