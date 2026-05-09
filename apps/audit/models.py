from django.db import models
from django.conf import settings
from apps.common.models import BaseModel
from apps.organizations.models import Organization

class AuditLog(BaseModel):
    ACTION_CREATE = 'create'
    ACTION_UPDATE = 'update'
    ACTION_DELETE = 'delete'
    ACTION_LOGIN = 'login'
    ACTION_LOGOUT = 'logout'
    ACTION_REGISTER = 'register'
    ACTION_PASSWORD_CHANGE = 'password_change'
    ACTION_PERMISSION_GRANTED = 'permission_granted'
    ACTION_PERMISSION_REVOKED = 'permission_revoked'
    ACTION_PAYMENT_INITIATED = 'payment_initiated'
    ACTION_PAYMENT_COMPLETED = 'payment_completed'
    ACTION_PAYMENT_FAILED = 'payment_failed'
    ACTION_CUSTOMIZATION_REQUEST_CREATED = 'customization_request_created'
    ACTION_DEPLOYMENT_REQUEST_CREATED = 'deployment_request_created'
    ACTION_FILE_UPLOADED = 'file_uploaded'
    ACTION_FILE_DELETED = 'file_deleted'

    ACTION_CHOICES = [
        (ACTION_CREATE, 'Create'),
        (ACTION_UPDATE, 'Update'),
        (ACTION_DELETE, 'Delete'),
        (ACTION_LOGIN, 'Login'),
        (ACTION_LOGOUT, 'Logout'),
        (ACTION_REGISTER, 'Register'),
        (ACTION_PASSWORD_CHANGE, 'Password Change'),
        (ACTION_PERMISSION_GRANTED, 'Permission Granted'),
        (ACTION_PERMISSION_REVOKED, 'Permission Revoked'),
        (ACTION_PAYMENT_INITIATED, 'Payment Initiated'),
        (ACTION_PAYMENT_COMPLETED, 'Payment Completed'),
        (ACTION_PAYMENT_FAILED, 'Payment Failed'),
        (ACTION_CUSTOMIZATION_REQUEST_CREATED, 'Customization Request Created'),
        (ACTION_DEPLOYMENT_REQUEST_CREATED, 'Deployment Request Created'),
        (ACTION_FILE_UPLOADED, 'File Uploaded'),
        (ACTION_FILE_DELETED, 'File Deleted'),
    ]

    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='audit_logs'
    )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='audit_logs'
    )

    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    resource_type = models.CharField(max_length=100, blank=True)
    resource_id = models.CharField(max_length=255, blank=True)

    message = models.TextField(blank=True)
    metadata = models.JSONField(null=True, blank=True)

    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Audit Log"
        verbose_name_plural = "Audit Logs"

    def __str__(self):
        actor_email = self.actor.email if self.actor else "System"
        return f"{self.action} by {actor_email} on {self.created_at}"
