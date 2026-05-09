from typing import Any, Dict, Optional
from django.contrib.auth import get_user_model
from apps.notifications.models import Notification
from apps.organizations.models import Organization, Membership

User = get_user_model()

def create_notification(
    recipient: User,
    title: str,
    message: str,
    notification_type: str = Notification.TYPE_IN_APP,
    organization: Optional[Organization] = None,
    action_url: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> Notification:
    """
    Base function to create a notification record.
    """
    return Notification.objects.create(
        recipient=recipient,
        title=title,
        message=message,
        notification_type=notification_type,
        organization=organization,
        action_url=action_url,
        metadata=metadata or {}
    )

def notify_user(
    user: User,
    title: str,
    message: str,
    notification_type: str = Notification.TYPE_IN_APP,
    action_url: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> Notification:
    """
    Helper to notify a specific user.
    """
    return create_notification(
        recipient=user,
        title=title,
        message=message,
        notification_type=notification_type,
        action_url=action_url,
        metadata=metadata
    )

def notify_organization_admins(
    organization: Organization,
    title: str,
    message: str,
    notification_type: str = Notification.TYPE_IN_APP,
    action_url: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None
):
    """
    Helper to notify all admins and the owner of an organization.
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
                notification_type=notification_type,
                organization=organization,
                action_url=action_url,
                metadata=metadata
            )
        )
    return notifications

def get_unread_count(user: User) -> int:
    """
    Returns the count of unread in-app notifications for a user.
    """
    return Notification.objects.filter(
        recipient=user,
        notification_type=Notification.TYPE_IN_APP,
        read_at__isnull=True
    ).count()
