import pytest
from apps.accounts.models import User
from apps.organizations.models import Organization, Membership
from apps.templates_catalog.models import TemplateCategory, SaaSTemplate

@pytest.fixture
def user(db):
    import uuid
    username = f'testuser_{uuid.uuid4().hex[:8]}'
    return User.objects.create_user(
        username=username,
        email=f'{username}@example.com',
        password='testpass123',
    )

@pytest.fixture
def category(db):
    return TemplateCategory.objects.create(name='Cat', slug='cat')

@pytest.fixture
def saas_template(db, category):
    return SaaSTemplate.objects.create(category=category, name='T1', slug='t1')

@pytest.fixture
def organization(db, user):
    org = Organization.objects.create(name="Test Org", slug="test-org", owner=user)
    Membership.objects.get_or_create(user=user, organization=org, role=Membership.ROLE_OWNER)
    return org
