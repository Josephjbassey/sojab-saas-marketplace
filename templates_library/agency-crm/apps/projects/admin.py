from django.contrib import admin
from .models import Project
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'client', 'status', 'organization')
    list_filter = ('status', 'organization')
