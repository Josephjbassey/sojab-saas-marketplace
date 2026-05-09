from django.contrib import admin
from .models import AuditLog

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'actor', 'action', 'resource_type', 'organization')
    list_filter = ('action', 'resource_type', 'created_at')
    search_fields = ('message', 'actor__email', 'resource_id', 'metadata')
    readonly_fields = ('id', 'created_at', 'updated_at', 'actor', 'organization', 'action', 'resource_type', 'resource_id', 'message', 'metadata', 'ip_address', 'user_agent')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
