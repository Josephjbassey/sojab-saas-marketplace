from django.db import models
from apps.common.models import BaseModel
from apps.purchases.models import TemplatePurchase

class PaymentTransaction(BaseModel):
    PROVIDER_CHOICES = [
        ('dummy', 'Dummy'),
        ('paystack', 'Paystack'),
        ('stripe', 'Stripe'),
        ('flutterwave', 'Flutterwave'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    purchase = models.ForeignKey(
        TemplatePurchase,
        on_delete=models.CASCADE,
        related_name='transactions'
    )
    provider = models.CharField(max_length=20, choices=PROVIDER_CHOICES)
    external_id = models.CharField(max_length=255, blank=True, help_text="ID from the payment gateway")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    raw_response = models.JSONField(null=True, blank=True, help_text="Full response from the gateway")

    def __str__(self):
        return f"{self.provider} - {self.external_id} ({self.status})"

class WebhookEvent(BaseModel):
    provider = models.CharField(max_length=20)
    event_type = models.CharField(max_length=255)
    payload = models.JSONField()
    processed = models.BooleanField(default=False)
    processed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Webhook {self.provider} - {self.event_type}"
