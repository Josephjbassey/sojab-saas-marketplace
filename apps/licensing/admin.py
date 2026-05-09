from django.contrib import admin
from .models import TemplateVersion, TemplateLicense

@admin.register(TemplateVersion)
class TemplateVersionAdmin(admin.ModelAdmin):
    list_display = ('template', 'version', 'release_date', 'is_active', 'is_latest')
    list_filter = ('is_active', 'is_latest', 'template', 'release_date')
    search_fields = ('version', 'template__name', 'changelog')
    readonly_fields = ('id', 'created_at', 'updated_at')

@admin.register(TemplateLicense)
class TemplateLicenseAdmin(admin.ModelAdmin):
    list_display = ('license_key', 'template', 'user', 'organization', 'license_type', 'status', 'issued_at')
    list_filter = ('license_type', 'status', 'template', 'issued_at')
    search_fields = ('license_key', 'user__email', 'user__username', 'organization__name', 'template__name')
    readonly_fields = ('license_key', 'issued_at', 'id', 'created_at', 'updated_at')
    raw_id_fields = ('template', 'purchase', 'user', 'organization')

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ('template', 'purchase', 'user', 'organization')
        return self.readonly_fields
