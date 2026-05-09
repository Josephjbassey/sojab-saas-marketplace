from .models import Notification
from apps.organizations.models import Membership

def create_notification(recipient, title, message, notification_type=Notification.TYPE_IN_APP, organization=None, action_url='', metadata=None):
    """
    Creates a notification for a specific user.
    """
    return Notification.objects.create(
        recipient=recipient,
        organization=organization,
        notification_type=notification_type,
        title=title,
        message=message,
        action_url=action_url,
        metadata=metadata
    )

def notify_user(user, title, message, organization=None, action_url='', metadata=None):
    """
    Helper to notify a user (defaults to in-app).
    """
    return create_notification(
        recipient=user,
        title=title,
        message=message,
        organization=organization,
        action_url=action_url,
        metadata=metadata
    )

def notify_organization_admins(organization, title, message, action_url='', metadata=None):
    """
    Sends a notification to all admins and owners of an organization.
    """
    admin_memberships = Membership.objects.filter(
        organization=organization,
        role__in=[Membership.ROLE_OWNER, Membership.ROLE_ADMIN]
    ).select_related('user')

    notifications = []
    for membership in admin_memberships:
        notifications.append(
            create_notification(
                recipient=membership.user,
                title=title,
                message=message,
                organization=organization,
                action_url=action_url,
                metadata=metadata
            )
        )
    return notifications

def get_unread_count(user):
    """
    Returns the count of unread notifications for a user.
    """
    return Notification.objects.filter(recipient=user, read_at__isnull=True).count()
