from django.contrib import admin
from .models import ManagedFile

@admin.register(ManagedFile)
class ManagedFileAdmin(admin.ModelAdmin):
    list_display = ('original_filename', 'purpose', 'owner', 'organization', 'size', 'created_at')
    list_filter = ('purpose', 'created_at', 'organization')
    search_fields = ('original_filename', 'owner__email', 'organization__name')
    readonly_fields = ('size', 'content_type', 'created_at', 'updated_at')
    raw_id_fields = ('owner', 'organization')
