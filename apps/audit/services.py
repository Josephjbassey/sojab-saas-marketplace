from django.contrib.contenttypes.models import ContentType
from .models import AuditLog

def log_action(actor=None, action=None, resource=None, organization=None, message="", metadata=None, request=None):
    """
    Service function to log an audit event.
    """
    if metadata is None:
        metadata = {}

    resource_type = None
    resource_id = None

    if resource:
        resource_type = resource.__class__.__name__
        # Try to get id or pk
        resource_id = str(getattr(resource, 'id', getattr(resource, 'pk', '')))

    ip_address = None
    user_agent = None

    if request:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0]
        else:
            ip_address = request.META.get('REMOTE_ADDR')

        user_agent = request.META.get('HTTP_USER_AGENT')

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
