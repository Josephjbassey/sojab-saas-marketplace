from django.contrib import admin
from .models import Note, Notification, AuditLog

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'content_object', 'created_at')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'recipient', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('action', 'user', 'resource_type', 'created_at')
    list_filter = ('action', 'resource_type', 'created_at')
