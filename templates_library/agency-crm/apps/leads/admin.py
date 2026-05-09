from django.contrib import admin
from .models import Lead
@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('title', 'client', 'status', 'value', 'organization')
    list_filter = ('status', 'organization')
