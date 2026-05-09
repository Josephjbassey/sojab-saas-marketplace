import pytest
from decimal import Decimal
from django.contrib.auth import get_user_model
from apps.templates_catalog.models import SaaSTemplate, TemplateCategory
from apps.purchases.models import TemplatePurchase
from .models import PaymentTransaction
from .services import get_payment_service

User = get_user_model()

@pytest.fixture
def purchase_setup(db):
    user = User.objects.create_user(username="buyer", email="buyer@example.com")
    category = TemplateCategory.objects.create(name="Web")
    template = SaaSTemplate.objects.create(name="Template", category=category)
    package = template.packages.create(name="Standard", price=Decimal('100.00'), license_type='commercial')
    purchase = TemplatePurchase.objects.create(
        user=user,
        template=template,
        package=package,
        amount_paid=package.price,
        status='pending'
    )
    return purchase

@pytest.mark.django_db
class TestBillingArchitecture:
    def test_dummy_provider_creates_transaction(self, purchase_setup):
        service = get_payment_service()
        result = service.create_payment(purchase_setup, purchase_setup.amount_paid)

        assert result.success
        assert purchase_setup.transaction_id.startswith('dummy_')

        tx = PaymentTransaction.objects.get(purchase=purchase_setup)
        assert tx.status == 'pending'
        assert tx.amount == purchase_setup.amount_paid
        assert tx.provider == 'dummy'

    def test_confirm_payment_updates_status(self, purchase_setup):
        service = get_payment_service()
        service.create_payment(purchase_setup, purchase_setup.amount_paid)
        service.confirm_payment(purchase_setup)

        purchase_setup.refresh_from_db()
        assert purchase_setup.status == 'paid'

        tx = PaymentTransaction.objects.get(purchase=purchase_setup)
        assert tx.status == 'paid'

    def test_mark_purchase_failed(self, purchase_setup):
        service = get_payment_service()
        service.create_payment(purchase_setup, purchase_setup.amount_paid)
        service.mark_purchase_failed(purchase_setup, "Card declined")

        purchase_setup.refresh_from_db()
        assert purchase_setup.status == 'failed'
        assert purchase_setup.notes == "Card declined"

        tx = PaymentTransaction.objects.get(purchase=purchase_setup)
        assert tx.status == 'failed'

    def test_refund_simulation(self, purchase_setup):
        service = get_payment_service()
        service.create_payment(purchase_setup, purchase_setup.amount_paid)
        service.confirm_payment(purchase_setup)
        service.refund_purchase(purchase_setup)

        purchase_setup.refresh_from_db()
        assert purchase_setup.status == 'refunded'

        tx = PaymentTransaction.objects.get(purchase=purchase_setup)
        assert tx.status == 'refunded'
