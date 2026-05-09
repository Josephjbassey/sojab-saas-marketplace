from django.contrib import admin
from .models import AuditLog

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('action', 'actor', 'organization', 'resource_type', 'created_at')
    list_filter = ('action', 'resource_type', 'organization', 'created_at')
    search_fields = ('message', 'actor__email', 'actor__username', 'resource_id')
    readonly_fields = [f.name for f in AuditLog._meta.get_fields()]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
