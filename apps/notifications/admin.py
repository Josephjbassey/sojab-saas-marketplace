from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'recipient', 'organization', 'notification_type', 'is_read', 'created_at')
    list_filter = ('notification_type', 'read_at', 'organization', 'created_at')
    search_fields = ('title', 'message', 'recipient__email', 'recipient__username')
    readonly_fields = ('id', 'created_at', 'updated_at')
    raw_id_fields = ('recipient', 'organization')
