import uuid
import requests
import hmac
import hashlib
from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Optional, Dict, Any
from django.conf import settings
from django.utils import timezone
from apps.purchases.models import TemplatePurchase


class PaymentResult:
    """Standardized result from any payment operation."""
    def __init__(self, success: bool, transaction_id: str = '', error: str = '', authorization_url: str = ''):
        self.success = success
        self.transaction_id = transaction_id
        self.error = error
        self.authorization_url = authorization_url


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


class PaystackPaymentProvider(BasePaymentProvider):
    """
    Paystack payment adapter.
    """
    BASE_URL = "https://api.paystack.co"

    def __init__(self):
        self.secret_key = getattr(settings, 'PAYSTACK_SECRET_KEY', '')
        self.headers = {
            "Authorization": f"Bearer {self.secret_key}",
            "Content-Type": "application/json",
        }

    def create_payment(self, purchase: TemplatePurchase, amount: Decimal) -> PaymentResult:
        """Initialize a Paystack transaction."""
        url = f"{self.BASE_URL}/transaction/initialize"

        # Paystack amount is in kobo/cents
        amount_kobo = int(amount * 100)

        payload = {
            "email": purchase.user.email,
            "amount": amount_kobo,
            "callback_url": getattr(settings, 'PAYSTACK_CALLBACK_URL', ''),
            "metadata": {
                "purchase_id": str(purchase.id),
                "user_id": str(purchase.user.id),
            }
        }

        try:
            response = requests.post(url, json=payload, headers=self.headers, timeout=10)
            data = response.json()

            if response.status_code == 200 and data.get('status'):
                transaction_id = data['data']['reference']
                auth_url = data['data']['authorization_url']

                purchase.transaction_id = transaction_id
                purchase.save(update_fields=['transaction_id', 'updated_at'])

                from .models import PaymentTransaction
                PaymentTransaction.objects.create(
                    purchase=purchase,
                    provider='paystack',
                    external_id=transaction_id,
                    amount=amount,
                    status='pending'
                )

                return PaymentResult(
                    success=True,
                    transaction_id=transaction_id,
                    authorization_url=auth_url
                )
            else:
                return PaymentResult(success=False, error=data.get('message', 'Failed to initialize Paystack transaction'))
        except Exception as e:
            return PaymentResult(success=False, error=str(e))

    def confirm_payment(self, purchase: TemplatePurchase) -> PaymentResult:
        """Verify a Paystack transaction status."""
        if not purchase.transaction_id:
            return PaymentResult(success=False, error="No transaction reference found")

        url = f"{self.BASE_URL}/transaction/verify/{purchase.transaction_id}"

        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            data = response.json()

            if response.status_code == 200 and data.get('status'):
                remote_status = data['data']['status']

                if remote_status == 'success':
                    purchase.status = 'paid'
                    purchase.save(update_fields=['status', 'updated_at'])

                    from .models import PaymentTransaction
                    tx = PaymentTransaction.objects.filter(external_id=purchase.transaction_id).last()
                    if tx:
                        tx.status = 'paid'
                        tx.save(update_fields=['status', 'updated_at'])

                    return PaymentResult(success=True, transaction_id=purchase.transaction_id)
                else:
                    return PaymentResult(success=False, error=f"Paystack status: {remote_status}")
            else:
                return PaymentResult(success=False, error=data.get('message', 'Verification failed'))
        except Exception as e:
            return PaymentResult(success=False, error=str(e))

    def refund_purchase(self, purchase: TemplatePurchase) -> PaymentResult:
        """Paystack refund implementation (stubbed for foundation)."""
        return PaymentResult(success=False, error="Refund not yet implemented for Paystack")

    def handle_webhook_event(self, payload: Dict[str, Any], signature: str) -> bool:
        """Handle incoming Paystack webhook."""
        # Verify signature
        if not self._verify_signature(payload, signature):
            return False

        event_type = payload.get('event')
        data = payload.get('data', {})
        reference = data.get('reference')

        if event_type == 'charge.success':
            from .models import PaymentTransaction
            tx = PaymentTransaction.objects.filter(external_id=reference).select_related('purchase').last()
            if tx and tx.status == 'paid':
                return True # Already processed

            if tx:
                tx.status = 'paid'
                tx.save(update_fields=['status', 'updated_at'])

                purchase = tx.purchase
                purchase.status = 'paid'
                purchase.save(update_fields=['status', 'updated_at'])

                # Side effects like notifications/licenses handled here or via signals
                return True

        return True

    def _verify_signature(self, payload_dict: Dict[str, Any], signature: str) -> bool:
        """Verify the Paystack webhook signature."""
        import json
        payload_bytes = json.dumps(payload_dict, separators=(',', ':')).encode('utf-8')
        secret = self.secret_key.encode('utf-8')

        expected_signature = hmac.new(secret, payload_bytes, hashlib.sha512).hexdigest()
        return hmac.compare_digest(expected_signature, signature)


def get_payment_service() -> BasePaymentProvider:
    """
    Factory function to get the active payment service.
    """
    provider_name = getattr(settings, 'ACTIVE_PAYMENT_PROVIDER', 'dummy')

    if provider_name == 'paystack':
        return PaystackPaymentProvider()
    return DummyPaymentProvider()

def create_subscription_record(user, plan, organization=None, provider='', provider_subscription_id=''):
    """
    Initializes a subscription record.
    """
    from .models import Subscription
    from django.utils import timezone
    from datetime import timedelta

    now = timezone.now()
    # Default period of 30 days for new records (to be updated by provider)
    period_end = now + timedelta(days=30)

    return Subscription.objects.create(
        user=user,
        organization=organization,
        plan=plan,
        provider=provider,
        provider_subscription_id=provider_subscription_id,
        status=Subscription.STATUS_TRIALING,
        current_period_start=now,
        current_period_end=period_end
    )

def mark_subscription_active(subscription):
    """
    Sets a subscription to active.
    """
    from .models import Subscription
    subscription.status = Subscription.STATUS_ACTIVE
    subscription.save(update_fields=['status', 'updated_at'])
    return subscription

def cancel_subscription_record(subscription, at_period_end=True):
    """
    Marks a subscription as cancelled.
    """
    from .models import Subscription
    if at_period_end:
        subscription.cancel_at_period_end = True
        subscription.save(update_fields=['cancel_at_period_end', 'updated_at'])
    else:
        subscription.status = Subscription.STATUS_CANCELLED
        subscription.save(update_fields=['status', 'updated_at'])
    return subscription

def expire_subscription_record(subscription):
    """
    Marks a subscription as expired.
    """
    from .models import Subscription
    subscription.status = Subscription.STATUS_EXPIRED
    subscription.save(update_fields=['status', 'updated_at'])
    return subscription
