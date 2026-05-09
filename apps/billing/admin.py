from django.contrib import admin
from .models import SubscriptionPlan, Subscription, PaymentTransaction, WebhookEvent

@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'currency', 'interval', 'is_active')
    list_filter = ('interval', 'is_active', 'currency')
    search_fields = ('name', 'slug', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('id', 'created_at', 'updated_at')

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'organization', 'plan', 'status', 'current_period_end')
    list_filter = ('status', 'plan', 'provider', 'cancel_at_period_end')
    search_fields = ('user__email', 'organization__name', 'provider_subscription_id')
    readonly_fields = ('id', 'created_at', 'updated_at')
    raw_id_fields = ('user', 'organization', 'plan')

@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ('purchase', 'provider', 'external_id', 'amount', 'status', 'created_at')
    list_filter = ('provider', 'status', 'created_at')
    search_fields = ('external_id', 'purchase__transaction_id', 'purchase__user__email')
    readonly_fields = ('id', 'created_at', 'updated_at')
    raw_id_fields = ('purchase',)

@admin.register(WebhookEvent)
class WebhookEventAdmin(admin.ModelAdmin):
    list_display = ('provider', 'event_type', 'processed', 'processed_at', 'created_at')
    list_filter = ('provider', 'processed', 'created_at')
    search_fields = ('event_type',)
    readonly_fields = ('id', 'created_at', 'updated_at')
