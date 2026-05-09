from .models import AuditLog
from django.contrib.auth import get_user_model
from typing import Optional, Any

User = get_user_model()

def log_action(actor: Optional[Any], action: str, resource: Optional[Any] = None, organization: Optional[Any] = None, message: str = "", metadata: Optional[dict] = None, request: Optional[Any] = None) -> AuditLog:
    """
    Standardized service to log an audit event.

    Args:
        actor: The user who performed the action (User instance or None).
        action: The type of event (AuditLog.ACTION_*).
        resource: Optional related model instance.
        organization: Optional related Organization instance.
        message: Optional descriptive message.
        metadata: Optional dictionary of extra data.
        request: Optional Django request object to capture IP and UA.

    Raises:
        ValueError: If action is missing or empty.
    """
    if not action:
        raise ValueError("Action is required for audit logging.")

    resource_type = ""
    resource_id = ""

    if resource:
        resource_type = resource.__class__.__name__
        resource_id = str(getattr(resource, 'pk', ''))

    ip_address = None
    user_agent = ""

    if request:
        # NOTE: HTTP_X_FORWARDED_FOR can be client-controlled (spoofing risk).
        # Logged IPs are "best effort" unless behind a trusted proxy.
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            # Prefer first entry in X-Forwarded-For
            ip_address = x_forwarded_for.split(',')[0].strip()
        else:
            ip_address = request.META.get('REMOTE_ADDR')

        user_agent = request.META.get('HTTP_USER_AGENT', '')

    return AuditLog.objects.create(
        actor=actor,
        organization=organization,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        message=message,
        metadata=metadata,
        ip_address=ip_address,
        user_agent=user_agent
    )
