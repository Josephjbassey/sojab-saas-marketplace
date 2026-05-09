from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'recipient', 'organization', 'notification_type', 'is_read', 'created_at')
    list_filter = ('notification_type', 'read_at', 'organization')
    search_fields = ('title', 'message', 'recipient__email', 'recipient__username')
    readonly_fields = ('created_at', 'updated_at')

    def is_read(self, obj):
        return obj.is_read
    is_read.boolean = True
    is_read.short_description = 'Read'
