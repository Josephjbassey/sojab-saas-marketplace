from django.contrib import admin
from .models import ClientProject, DeploymentRequest

class DeploymentRequestInline(admin.TabularInline):
    model = DeploymentRequest
    extra = 1

@admin.register(ClientProject)
class ClientProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'template', 'status', 'created_at')
    list_filter = ('status', 'template')
    search_fields = ('name', 'user__email')
    inlines = [DeploymentRequestInline]

@admin.register(DeploymentRequest)
class DeploymentRequestAdmin(admin.ModelAdmin):
    list_display = ('project', 'user', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('project__name', 'user__email', 'delivery_link')
    readonly_fields = ('created_at', 'updated_at')
