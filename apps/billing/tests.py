import pytest
import json
import hmac
import hashlib
from unittest.mock import patch, MagicMock
from django.conf import settings
from django.urls import reverse
from .services import PaystackPaymentProvider, get_payment_service
from .models import PaymentTransaction, WebhookEvent

@pytest.mark.django_db
class TestPaystackProvider:
    @patch('requests.post')
    def test_create_payment_success(self, mock_post, purchase):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'status': True,
            'data': {
                'reference': 'test_ref_123',
                'authorization_url': 'https://checkout.paystack.com/123'
            }
        }
        mock_post.return_value = mock_response

        provider = PaystackPaymentProvider()
        result = provider.create_payment(purchase, purchase.amount_paid)

        assert result.success is True
        assert result.transaction_id == 'test_ref_123'
        assert result.authorization_url == 'https://checkout.paystack.com/123'
        assert PaymentTransaction.objects.filter(external_id='test_ref_123').exists()

    @patch('requests.get')
    def test_verify_payment_success(self, mock_get, purchase):
        purchase.transaction_id = 'test_ref_123'
        purchase.save()

        PaymentTransaction.objects.create(
            purchase=purchase,
            provider='paystack',
            external_id='test_ref_123',
            amount=purchase.amount_paid,
            status='pending'
        )

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'status': True,
            'data': {
                'status': 'success',
                'reference': 'test_ref_123'
            }
        }
        mock_get.return_value = mock_response

        provider = PaystackPaymentProvider()
        result = provider.confirm_payment(purchase)

        assert result.success is True
        purchase.refresh_from_db()
        assert purchase.status == 'paid'

    def test_webhook_signature_verification(self):
        provider = PaystackPaymentProvider()
        provider.secret_key = 'test_secret'

        payload = {'event': 'charge.success', 'data': {'reference': 'ref123'}}
        payload_json = json.dumps(payload, separators=(',', ':'))

        signature = hmac.new(
            b'test_secret',
            payload_json.encode('utf-8'),
            hashlib.sha512
        ).hexdigest()

        assert provider._verify_signature(payload, signature) is True
        assert provider._verify_signature(payload, 'wrong_sig') is False

@pytest.mark.django_db
class TestBillingViews:
    def test_paystack_webhook_endpoint(self, client, purchase):
        purchase.transaction_id = 'ref123'
        purchase.save()

        tx = PaymentTransaction.objects.create(
            purchase=purchase,
            provider='paystack',
            external_id='ref123',
            amount=purchase.amount_paid,
            status='pending'
        )

        payload = {'event': 'charge.success', 'data': {'reference': 'ref123'}}
        payload_json = json.dumps(payload, separators=(',', ':'))

        # We need to mock the service to bypass signature check or use real one
        with patch.object(PaystackPaymentProvider, '_verify_signature', return_value=True):
            with patch('apps.billing.views.get_payment_service') as mock_get_service:
                provider = PaystackPaymentProvider()
                provider.secret_key = 'test'
                mock_get_service.return_value = provider

                response = client.post(
                    reverse('billing:paystack_webhook'),
                    data=payload_json,
                    content_type='application/json',
                    HTTP_X_PAYSTACK_SIGNATURE='valid'
                )

                assert response.status_code == 200
                purchase.refresh_from_db()
                assert purchase.status == 'paid'
                assert WebhookEvent.objects.filter(event_type='charge.success').exists()
