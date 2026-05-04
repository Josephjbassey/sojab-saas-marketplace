"""
Payment service abstraction layer.

All payment processing goes through this service. Currently uses a dummy
processor for MVP. Swap in Stripe/Paystack by implementing the methods
below with real gateway calls.
"""
import uuid
from decimal import Decimal
from apps.purchases.models import TemplatePurchase


class PaymentResult:
    """Standardized result from any payment operation."""
    def __init__(self, success: bool, transaction_id: str = '', error: str = ''):
        self.success = success
        self.transaction_id = transaction_id
        self.error = error


class DummyPaymentService:
    """
    Stubbed payment processor for MVP.
    
    Replace this class with StripePaymentService or PaystackPaymentService
    when ready to go live.
    """

    @staticmethod
    def create_payment(purchase: TemplatePurchase, amount: Decimal) -> PaymentResult:
        """Simulate creating a payment intent / charge."""
        transaction_id = f"dummy_{uuid.uuid4().hex[:12]}"
        purchase.transaction_id = transaction_id
        purchase.save(update_fields=['transaction_id', 'updated_at'])
        return PaymentResult(success=True, transaction_id=transaction_id)

    @staticmethod
    def confirm_payment(purchase: TemplatePurchase) -> PaymentResult:
        """Simulate confirming/capturing a payment."""
        purchase.status = 'paid'
        purchase.save(update_fields=['status', 'updated_at'])
        return PaymentResult(success=True, transaction_id=purchase.transaction_id)

    @staticmethod
    def mark_purchase_paid(purchase: TemplatePurchase) -> None:
        """Mark a purchase as paid (used by webhooks in real integrations)."""
        purchase.status = 'paid'
        purchase.save(update_fields=['status', 'updated_at'])

    @staticmethod
    def mark_purchase_failed(purchase: TemplatePurchase, error: str = '') -> None:
        """Mark a purchase as failed."""
        purchase.status = 'failed'
        purchase.notes = error
        purchase.save(update_fields=['status', 'notes', 'updated_at'])

    @staticmethod
    def refund_purchase(purchase: TemplatePurchase) -> PaymentResult:
        """Simulate refunding a payment."""
        purchase.status = 'refunded'
        purchase.save(update_fields=['status', 'updated_at'])
        return PaymentResult(success=True, transaction_id=purchase.transaction_id)


def get_payment_service():
    """
    Factory function to get the active payment service.
    
    Switch this to return StripePaymentService() or PaystackPaymentService()
    when integrating real payments.
    """
    from django.conf import settings
    if getattr(settings, 'DUMMY_PAYMENTS_ENABLED', True):
        return DummyPaymentService()
    # Future: return StripePaymentService() or PaystackPaymentService()
    return DummyPaymentService()
