from django.contrib import admin
from .models import ManagedFile

@admin.register(ManagedFile)
class ManagedFileAdmin(admin.ModelAdmin):
    list_display = ('original_filename', 'purpose', 'owner', 'organization', 'size', 'created_at')
    list_filter = ('purpose', 'created_at')
    search_fields = ('original_filename', 'owner__email', 'organization__name')
    readonly_fields = ('created_at', 'updated_at', 'size')

    def save_model(self, request, obj, form, change):
        if not obj.owner and not change:
            obj.owner = request.user
        super().save_model(request, obj, form, change)
