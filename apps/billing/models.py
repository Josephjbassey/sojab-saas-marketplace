from django.db import models
from django.conf import settings
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

class SubscriptionPlan(BaseModel):
    INTERVAL_DAILY = 'daily'
    INTERVAL_WEEKLY = 'weekly'
    INTERVAL_MONTHLY = 'monthly'
    INTERVAL_QUARTERLY = 'quarterly'
    INTERVAL_YEARLY = 'yearly'

    INTERVAL_CHOICES = [
        (INTERVAL_DAILY, 'Daily'),
        (INTERVAL_WEEKLY, 'Weekly'),
        (INTERVAL_MONTHLY, 'Monthly'),
        (INTERVAL_QUARTERLY, 'Quarterly'),
        (INTERVAL_YEARLY, 'Yearly'),
    ]

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    interval = models.CharField(max_length=20, choices=INTERVAL_CHOICES, default=INTERVAL_MONTHLY)

    features = models.JSONField(default=dict, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.get_interval_display()})"

class Subscription(BaseModel):
    STATUS_ACTIVE = 'active'
    STATUS_CANCELLED = 'cancelled'
    STATUS_PAST_DUE = 'past_due'
    STATUS_TRIALING = 'trialing'
    STATUS_EXPIRED = 'expired'

    STATUS_CHOICES = [
        (STATUS_ACTIVE, 'Active'),
        (STATUS_CANCELLED, 'Cancelled'),
        (STATUS_PAST_DUE, 'Past Due'),
        (STATUS_TRIALING, 'Trialing'),
        (STATUS_EXPIRED, 'Expired'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='subscriptions'
    )
    organization = models.ForeignKey(
        'organizations.Organization',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subscriptions'
    )
    plan = models.ForeignKey(
        SubscriptionPlan,
        on_delete=models.PROTECT,
        related_name='subscriptions'
    )

    provider = models.CharField(max_length=50, blank=True)
    provider_subscription_id = models.CharField(max_length=255, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_TRIALING)

    current_period_start = models.DateTimeField()
    current_period_end = models.DateTimeField()

    cancel_at_period_end = models.BooleanField(default=False)
    trial_ends_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.email} - {self.plan.name} ({self.status})"

    @property
    def is_active(self):
        return self.status in [self.STATUS_ACTIVE, self.STATUS_TRIALING]
