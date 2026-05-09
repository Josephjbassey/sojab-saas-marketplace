from django.db import models
from django.conf import settings
from django.utils import timezone
from apps.common.models import BaseModel
from apps.organizations.models import Organization

class Notification(BaseModel):
    TYPE_IN_APP = 'in_app'
    TYPE_EMAIL = 'email'

    TYPE_CHOICES = [
        (TYPE_IN_APP, 'In-App'),
        (TYPE_EMAIL, 'Email'),
    ]

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='notifications'
    )

    notification_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default=TYPE_IN_APP
    )

    title = models.CharField(max_length=255)
    message = models.TextField()
    action_url = models.CharField(max_length=512, blank=True)

    read_at = models.DateTimeField(null=True, blank=True)
    metadata = models.JSONField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} for {self.recipient.email}"

    @property
    def is_read(self):
        return self.read_at is not None

    def mark_as_read(self):
        if not self.read_at:
            self.read_at = timezone.now()
            self.save(update_fields=['read_at', 'updated_at'])

    def mark_as_unread(self):
        if self.read_at:
            self.read_at = None
            self.save(update_fields=['read_at', 'updated_at'])
