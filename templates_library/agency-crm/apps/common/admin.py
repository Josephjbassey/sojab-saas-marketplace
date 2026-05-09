from django.contrib import admin
from .models import Note

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'content_object', 'created_at')
    list_filter = ('created_at', 'content_type')
    search_fields = ('content', 'user__username')
