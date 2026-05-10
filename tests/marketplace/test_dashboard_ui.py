import pytest
from django.urls import reverse
from apps.accounts.models import User
from apps.organizations.models import Organization, Membership
from apps.purchases.models import TemplatePurchase
from apps.templates_catalog.models import SaaSTemplate, TemplateCategory, TemplatePackage
from apps.generator.models import GeneratedProject
from apps.notifications.models import Notification

TEST_PASSWORD = 'password'

@pytest.fixture
def user(db):
    return User.objects.create_user(username='testuser', email='test@example.com', password=TEST_PASSWORD)

@pytest.fixture
def other_user(db):
    return User.objects.create_user(username='otheruser', email='other@example.com', password=TEST_PASSWORD)

@pytest.fixture
def organization(db):
    return Organization.objects.create(name='Test Org', slug='test-org')

@pytest.fixture
def template(db):
    category = TemplateCategory.objects.create(name='Test Cat', slug='test-cat')
    return SaaSTemplate.objects.create(name='Test Template', slug='test-template', category=category, description='Desc')

@pytest.fixture
def package(db, template):
    return TemplatePackage.objects.create(template=template, name='Starter', price=49.00)

@pytest.mark.django_db
class TestDashboardUI:
    def test_dashboard_requires_login(self, client):
        response = client.get(reverse('marketplace:dashboard'))
        assert response.status_code == 302
        assert 'login' in response.url

    def test_dashboard_renders_for_logged_in_user(self, client, user):
        client.login(username='testuser', password=TEST_PASSWORD)
        response = client.get(reverse('marketplace:dashboard'))
        assert response.status_code == 200
        assert b'System Dashboard' in response.content

    def test_organization_isolation(self, client, user, other_user, organization):
        # Membership for user
        Membership.objects.create(user=user, organization=organization, role='member')

        # Log in as other user
        client.login(username='otheruser', password=TEST_PASSWORD)

        # Try to view organization list (should be empty for other_user)
        response = client.get(reverse('organizations:list'))
        assert response.status_code == 200
        assert organization.name.encode() not in response.content

        # Try to view organization detail directly
        response = client.get(reverse('organizations:detail', args=[organization.slug]))
        assert response.status_code == 302 # Redirected because of permission check

    def test_notification_list_renders(self, client, user):
        Notification.objects.create(recipient=user, title='Test Notification', message='Hello')
        client.login(username='testuser', password=TEST_PASSWORD)
        response = client.get(reverse('notifications:list'))
        assert response.status_code == 200
        assert b'Test Notification' in response.content

    def test_purchase_detail_isolation(self, client, user, other_user, package):
        template = package.template
        purchase = TemplatePurchase.objects.create(user=user, template=template, package=package, amount_paid=49.00, status='paid')

        client.login(username='otheruser', password=TEST_PASSWORD)
        response = client.get(reverse('purchases:detail', args=[purchase.pk]))
        assert response.status_code == 404

        client.login(username='testuser', password=TEST_PASSWORD)
        response = client.get(reverse('purchases:detail', args=[purchase.pk]))
        assert response.status_code == 200
        assert template.name.encode() in response.content

    def test_generated_project_detail_renders(self, client, user, package):
        template = package.template
        purchase = TemplatePurchase.objects.create(user=user, template=template, package=package, amount_paid=49.00, status='paid')
        project = GeneratedProject.objects.create(user=user, purchase=purchase, template=template, project_name='My Project')

        client.login(username='testuser', password=TEST_PASSWORD)
        response = client.get(reverse('generator:detail', args=[project.pk]))
        assert response.status_code == 200
        assert b'My Project' in response.content
