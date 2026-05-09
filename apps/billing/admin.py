from django.contrib import admin

# Register your models here.

from .models import SubscriptionPlan, Subscription

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
