import pytest
from decimal import Decimal
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.templates_catalog.models import SaaSTemplate, TemplateCategory, TemplatePackage
from .models import TemplatePurchase

User = get_user_model()

@pytest.fixture
def checkout_setup(db, client):
    user = User.objects.create_user(username="buyer", email="buyer@example.com", password="password")
    client.login(username="buyer", password="password")
    category = TemplateCategory.objects.create(name="Web")
    template = SaaSTemplate.objects.create(name="Template", category=category)
    package = template.packages.create(name="Standard", price=Decimal('100.00'), license_type='commercial')
    return {
        'user': user,
        'package': package,
        'client': client
    }

@pytest.mark.django_db
class TestPurchaseFlow:
    def test_checkout_process_success(self, checkout_setup):
        package = checkout_setup['package']
        client = checkout_setup['client']
        url = reverse('purchases:checkout', kwargs={'package_id': package.id})

        response = client.post(url)
        assert response.status_code == 302

        purchase = TemplatePurchase.objects.get(user=checkout_setup['user'], package=package)
        assert purchase.status == 'paid'
        assert purchase.transactions.filter(status='paid').exists()

    def test_duplicate_purchase_prevention(self, checkout_setup):
        package = checkout_setup['package']
        client = checkout_setup['client']

        # First purchase
        client.post(reverse('purchases:checkout', kwargs={'package_id': package.id}))

        # Try again
        response = client.get(reverse('purchases:checkout', kwargs={'package_id': package.id}))
        assert response.status_code == 302  # Should redirect to success
