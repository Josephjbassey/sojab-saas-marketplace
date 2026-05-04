from django.contrib import admin
from .models import TemplatePurchase

@admin.register(TemplatePurchase)
class TemplatePurchaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'template', 'package', 'amount_paid', 'status', 'created_at')
    list_filter = ('status', 'template', 'package')
    search_fields = ('user__email', 'transaction_id', 'id')
    readonly_fields = ('id', 'created_at', 'updated_at')
