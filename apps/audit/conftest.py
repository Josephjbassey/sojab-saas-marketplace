import pytest
from apps.accounts.models import User
from apps.templates_catalog.models import TemplateCategory, SaaSTemplate

@pytest.fixture
def user(db):
    user = User.objects.filter(username='testuser_notif').first()
    if not user:
        user = User.objects.create_user(
            username='testuser_notif',
            email='test@example.com',
            password='testpass123',
        )
    return user

@pytest.fixture
def category(db):
    return TemplateCategory.objects.create(name='Cat', slug='cat')

@pytest.fixture
def saas_template(db, category):
    return SaaSTemplate.objects.create(category=category, name='T1', slug='t1')

@pytest.fixture
def organization(db, user):
    from apps.organizations.models import Organization, Membership
    org = Organization.objects.create(name="Test Org", slug="test-org", owner=user)
    Membership.objects.get_or_create(user=user, organization=org, role=Membership.ROLE_OWNER)
    return org
