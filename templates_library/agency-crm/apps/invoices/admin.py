from django.contrib import admin
from .models import Invoice
@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('number', 'client', 'amount', 'due_date', 'status', 'organization')
    list_filter = ('status', 'organization')
