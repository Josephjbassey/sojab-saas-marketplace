import pytest
from apps.accounts.models import User
from apps.templates_catalog.models import TemplateCategory, SaaSTemplate, TemplatePackage
from apps.purchases.models import TemplatePurchase

@pytest.fixture
def user(db):
    return User.objects.create_user(
        username='licenseuser',
        email='license@example.com',
        password='password123'
    )

@pytest.fixture
def category(db):
    return TemplateCategory.objects.create(name='SaaS', slug='saas')

@pytest.fixture
def saas_template(db, category):
    return SaaSTemplate.objects.create(
        category=category,
        name='Titan',
        slug='titan',
        is_active=True
    )

@pytest.fixture
def package(db, saas_template):
    return TemplatePackage.objects.create(
        template=saas_template,
        name='Personal',
        price=100.00,
        is_active=True
    )

@pytest.fixture
def purchase(db, user, saas_template, package):
    return TemplatePurchase.objects.create(
        user=user,
        template=saas_template,
        package=package,
        amount_paid=100.00,
        status='paid'
    )

@pytest.fixture
def organization(db, user):
    from apps.organizations.models import Organization, Membership
    org = Organization.objects.create(name="Test Org", slug="test-org", owner=user)
    Membership.objects.create(user=user, organization=org, role=Membership.ROLE_OWNER)
    return org
