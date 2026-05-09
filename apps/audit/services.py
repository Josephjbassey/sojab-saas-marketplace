from .models import AuditLog

def log_action(actor, action, resource=None, organization=None, message="", metadata=None, request=None):
    """
    Standardized service to log an audit event.
    """
    resource_type = ""
    resource_id = ""

    if resource:
        resource_type = resource.__class__.__name__
        resource_id = str(getattr(resource, 'pk', ''))

    ip_address = None
    user_agent = ""

    if request:
        # Simple IP resolution
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0]
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
