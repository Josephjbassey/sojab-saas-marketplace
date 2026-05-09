import pytest
from django.contrib.auth import get_user_model
from apps.organizations.models import Organization, Membership
from .models import Notification
from .services import create_notification, notify_user, notify_organization_admins, get_unread_count

User = get_user_model()

@pytest.mark.django_db
class TestNotifications:
    def test_create_notification(self, user):
        notif = create_notification(user, "Test Title", "Test Message")
        assert notif.recipient == user
        assert notif.title == "Test Title"
        assert notif.notification_type == Notification.TYPE_IN_APP
        assert notif.is_read is False

    def test_mark_as_read(self, user):
        notif = create_notification(user, "Title", "Msg")
        notif.mark_as_read()
        assert notif.is_read is True
        assert notif.read_at is not None

    def test_unread_count(self, user):
        create_notification(user, "T1", "M1")
        create_notification(user, "T2", "M2")
        assert get_unread_count(user) == 2

        notif = Notification.objects.first()
        notif.mark_as_read()
        assert get_unread_count(user) == 1

    def test_notify_organization_admins(self, user, organization):
        # Create another user as admin
        admin_user = User.objects.create_user(email="admin@example.com", username="admin", password="password")
        Membership.objects.create(user=admin_user, organization=organization, role=Membership.ROLE_ADMIN)

        # Original user is owner (from fixture)
        Membership.objects.get_or_create(user=user, organization=organization, role=Membership.ROLE_OWNER)

        notifs = notify_organization_admins(organization, "Org Alert", "Something happened")
        assert len(notifs) == 2
        assert Notification.objects.filter(title="Org Alert").count() == 2
