import pytest
from apps.accounts.models import User
from apps.templates_catalog.models import TemplateCategory, SaaSTemplate, TemplatePackage
from apps.purchases.models import TemplatePurchase

@pytest.fixture
def user(db):
    return User.objects.create_user(
        username='billinguser',
        email='billing@example.com',
        password='password123'
    )

@pytest.fixture
def category(db):
    return TemplateCategory.objects.create(name='Billing', slug='billing')

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
        name='Commercial',
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
        status='pending'
    )
