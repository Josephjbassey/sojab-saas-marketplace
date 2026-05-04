import pytest
from apps.accounts.models import User
from apps.templates_catalog.models import TemplateCategory, SaaSTemplate, TemplatePackage, TemplateFeature
from apps.purchases.models import TemplatePurchase
from apps.support.models import CustomizationRequest
from apps.deployments.models import ClientProject


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123',
        first_name='Test',
        last_name='User',
    )


@pytest.fixture
def admin_user(db):
    return User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='adminpass123',
    )


@pytest.fixture
def category(db):
    return TemplateCategory.objects.create(
        name='SaaS Boilerplates',
        slug='saas-boilerplates',
        description='Ready-made SaaS starter kits',
    )


@pytest.fixture
def saas_template(db, category):
    return SaaSTemplate.objects.create(
        category=category,
        name='Titan Boilerplate',
        slug='titan-boilerplate',
        description='A robust boilerplate for SaaS apps.',
        short_description='Build SaaS fast.',
        is_active=True,
        is_featured=True,
    )


@pytest.fixture
def template_package(db, saas_template):
    return TemplatePackage.objects.create(
        template=saas_template,
        name='Personal License',
        license_type='personal',
        price=99.00,
        is_active=True,
    )


@pytest.fixture
def commercial_package(db, saas_template):
    return TemplatePackage.objects.create(
        template=saas_template,
        name='Commercial License',
        license_type='commercial',
        price=299.00,
        is_active=True,
    )


@pytest.fixture
def purchase(db, user, saas_template, template_package):
    return TemplatePurchase.objects.create(
        user=user,
        template=saas_template,
        package=template_package,
        amount_paid=template_package.price,
        status='paid',
        transaction_id='dummy_abc123',
    )


@pytest.fixture
def customization_request(db, user, saas_template):
    return CustomizationRequest.objects.create(
        user=user,
        template=saas_template,
        subject='Add custom auth',
        description='I need OAuth2 support.',
        budget_expectation=500.00,
    )


@pytest.fixture
def client_project(db, user, saas_template, purchase):
    return ClientProject.objects.create(
        user=user,
        template=saas_template,
        purchase=purchase,
        name='My SaaS Project',
        status='active',
    )


@pytest.fixture
def authenticated_client(client, user):
    client.login(username='testuser', password='testpass123')
    return client
