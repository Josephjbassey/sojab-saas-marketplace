import uuid
from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Optional
from apps.purchases.models import TemplatePurchase


class PaymentResult:
    """Standardized result from any payment operation."""
    def __init__(self, success: bool, transaction_id: str = '', error: str = ''):
        self.success = success
        self.transaction_id = transaction_id
        self.error = error


class BasePaymentProvider(ABC):
    """
    Abstract base class for payment providers.
    All adapters (Stripe, Paystack, etc.) must implement this interface.
    """

    @abstractmethod
    def create_payment(self, purchase: TemplatePurchase, amount: Decimal) -> PaymentResult:
        pass

    @abstractmethod
    def confirm_payment(self, purchase: TemplatePurchase) -> PaymentResult:
        pass

    @abstractmethod
    def refund_purchase(self, purchase: TemplatePurchase) -> PaymentResult:
        pass


class DummyPaymentProvider(BasePaymentProvider):
    """
    Stubbed payment processor for MVP.
    """

    def create_payment(self, purchase: TemplatePurchase, amount: Decimal) -> PaymentResult:
        """Simulate creating a payment intent / charge."""
        transaction_id = f"dummy_{uuid.uuid4().hex[:12]}"
        purchase.transaction_id = transaction_id
        purchase.save(update_fields=['transaction_id', 'updated_at'])

        from .models import PaymentTransaction
        PaymentTransaction.objects.create(
            purchase=purchase,
            provider='dummy',
            external_id=transaction_id,
            amount=amount,
            status='pending'
        )

        return PaymentResult(success=True, transaction_id=transaction_id)

    def confirm_payment(self, purchase: TemplatePurchase) -> PaymentResult:
        """Simulate confirming/capturing a payment."""
        purchase.status = 'paid'
        purchase.save(update_fields=['status', 'updated_at'])

        from .models import PaymentTransaction
        tx = PaymentTransaction.objects.filter(purchase=purchase).last()
        if tx:
            tx.status = 'paid'
            tx.save(update_fields=['status', 'updated_at'])

        return PaymentResult(success=True, transaction_id=purchase.transaction_id)

    def refund_purchase(self, purchase: TemplatePurchase) -> PaymentResult:
        """Simulate refunding a payment."""
        purchase.status = 'refunded'
        purchase.save(update_fields=['status', 'updated_at'])

        from .models import PaymentTransaction
        tx = PaymentTransaction.objects.filter(purchase=purchase).last()
        if tx:
            tx.status = 'refunded'
            tx.save(update_fields=['status', 'updated_at'])

        return PaymentResult(success=True, transaction_id=purchase.transaction_id)

    def mark_purchase_failed(self, purchase: TemplatePurchase, error: str = '') -> None:
        """Mark a purchase as failed."""
        purchase.status = 'failed'
        purchase.notes = error
        purchase.save(update_fields=['status', 'notes', 'updated_at'])

        from .models import PaymentTransaction
        tx = PaymentTransaction.objects.filter(purchase=purchase).last()
        if tx:
            tx.status = 'failed'
            tx.save(update_fields=['status', 'updated_at'])


def get_payment_service() -> DummyPaymentProvider:
    """
    Factory function to get the active payment service.
    """
    from django.conf import settings
    # We return DummyPaymentProvider for now.
    return DummyPaymentProvider()
