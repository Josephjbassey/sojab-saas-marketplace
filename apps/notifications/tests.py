from django.urls import reverse
import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone
from apps.notifications.models import Notification
from apps.notifications.services import (
    create_notification,
    notify_user,
    notify_organization_admins,
    get_unread_count
)
from apps.organizations.models import Organization, Membership
from apps.templates_catalog.models import SaaSTemplate, TemplateCategory, TemplatePackage

User = get_user_model()

@pytest.fixture
def test_category(db):
    return TemplateCategory.objects.create(name="Web Apps", slug="web-apps")

@pytest.mark.django_db
class TestNotificationModels:
    def test_notification_creation(self):
        user = User.objects.create_user(username="recipient", email="recipient@example.com")
        notification = Notification.objects.create(
            recipient=user,
            title="Test Title",
            message="Test Message"
        )
        assert notification.title == "Test Title"
        assert notification.recipient == user
        assert notification.notification_type == Notification.TYPE_IN_APP
        assert notification.read_at is None
        assert not notification.is_read

    def test_mark_as_read_unread(self):
        user = User.objects.create_user(username="testuser", email="test@example.com")
        notification = Notification.objects.create(
            recipient=user,
            title="Test Title",
            message="Test Message"
        )

        notification.mark_as_read()
        assert notification.read_at is not None
        assert notification.is_read

        notification.mark_as_unread()
        assert notification.read_at is None
        assert not notification.is_read

@pytest.mark.django_db
class TestNotificationServices:
    def test_create_notification(self):
        user = User.objects.create_user(username="user1", email="user1@example.com")
        notification = create_notification(
            recipient=user,
            title="Service Title",
            message="Service Message",
            metadata={"key": "value"}
        )
        assert notification.title == "Service Title"
        assert notification.metadata == {"key": "value"}

    def test_notify_user(self):
        user = User.objects.create_user(username="user2", email="user2@example.com")
        notification = notify_user(user, "Hello", "World")
        assert notification.recipient == user
        assert notification.title == "Hello"

    def test_notify_organization_admins(self):
        owner_user = User.objects.create_user(username="owner", email="owner@example.com")
        admin_user = User.objects.create_user(username="admin", email="admin@example.com")
        member_user = User.objects.create_user(username="member", email="member@example.com")

        org = Organization.objects.create(name="Test Org", owner=owner_user)
        Membership.objects.create(user=owner_user, organization=org, role=Membership.ROLE_OWNER)
        Membership.objects.create(user=admin_user, organization=org, role=Membership.ROLE_ADMIN)
        Membership.objects.create(user=member_user, organization=org, role=Membership.ROLE_MEMBER)

        notifications = notify_organization_admins(org, "Admin Alert", "Something happened")

        assert len(notifications) == 2
        recipients = [n.recipient for n in notifications]
        assert owner_user in recipients
        assert admin_user in recipients
        assert member_user not in recipients

    def test_get_unread_count(self):
        user = User.objects.create_user(username="user3", email="user3@example.com")

        notify_user(user, "T1", "M1")
        notify_user(user, "T2", "M2")
        n3 = notify_user(user, "T3", "M3")
        n3.mark_as_read()

        other_user = User.objects.create_user(username="other", email="other@example.com")
        notify_user(other_user, "T4", "M4")

        assert get_unread_count(user) == 2

@pytest.mark.django_db
class TestNotificationIntegration:
    def test_customization_request_notification(self, client, test_category):
        user = User.objects.create_user(username="customer", email="customer@example.com", password="password")
        client.force_login(user)

        template = SaaSTemplate.objects.create(
            category=test_category,
            name="SaaS Pro",
            slug="saas-pro",
            is_active=True
        )

        url = reverse('support:customization_request', kwargs={'template_slug': template.slug})
        data = {
            'template': template.id,
            'subject': 'Test Subject',
            'description': 'Test Description',
            'budget_expectation': 1000
        }

        response = client.post(url, data)
        assert response.status_code == 200

        assert Notification.objects.filter(recipient=user, title="Customization Request Received").exists()
        assert get_unread_count(user) == 1

    def test_purchase_notification(self, client, test_category):
        user = User.objects.create_user(username="buyer", email="buyer@example.com", password="password")
        client.force_login(user)

        template = SaaSTemplate.objects.create(
            category=test_category,
            name="SaaS Pro",
            slug="saas-pro",
            is_active=True
        )
        package = TemplatePackage.objects.create(
            template=template,
            name="Personal",
            price=49.00,
            is_active=True
        )

        url = reverse('purchases:checkout', kwargs={'package_id': package.id})

        response = client.post(url)
        assert response.status_code == 302

        assert Notification.objects.filter(recipient=user, title="Purchase Successful").exists()
        assert get_unread_count(user) == 1
