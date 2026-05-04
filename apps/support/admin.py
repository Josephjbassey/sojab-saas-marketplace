from django.contrib import admin
from .models import CustomizationRequest

@admin.register(CustomizationRequest)
class CustomizationRequestAdmin(admin.ModelAdmin):
    list_display = ('subject', 'user', 'template', 'status', 'budget_expectation', 'created_at')
    list_filter = ('status', 'template')
    search_fields = ('user__email', 'subject', 'description')
    readonly_fields = ('created_at', 'updated_at')
