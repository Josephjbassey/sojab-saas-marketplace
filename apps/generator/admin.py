from django.contrib import admin
from .models import GeneratedProject, ProjectConfiguration

class ProjectConfigurationInline(admin.StackedInline):
    model = ProjectConfiguration
    can_delete = False
    verbose_name_plural = 'Configuration'

@admin.register(GeneratedProject)
class GeneratedProjectAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'status', 'user', 'organization', 'template', 'created_at')
    list_filter = ('status', 'template', 'organization', 'created_at')
    search_fields = ('project_name', 'slug', 'user__email', 'user__username', 'admin_notes')
    prepopulated_fields = {'slug': ('project_name',)}
    readonly_fields = ('id', 'created_at', 'updated_at')
    inlines = [ProjectConfigurationInline]
    raw_id_fields = ('purchase', 'template', 'user', 'organization')

    fieldsets = (
        (None, {
            'fields': ('project_name', 'slug', 'status', 'purchase', 'template', 'user', 'organization')
        }),
        ('Delivery Info', {
            'fields': ('github_repo_url', 'zip_file', 'deployment_url')
        }),
        ('Admin', {
            'fields': ('admin_notes', 'id', 'created_at', 'updated_at')
        }),
    )

@admin.register(ProjectConfiguration)
class ProjectConfigurationAdmin(admin.ModelAdmin):
    list_display = ('generated_project', 'brand_name', 'payment_provider', 'deployment_target')
    list_filter = ('payment_provider', 'deployment_target', 'cms_enabled')
    search_fields = ('brand_name', 'generated_project__project_name')
    readonly_fields = ('id', 'created_at', 'updated_at')
    raw_id_fields = ('generated_project',)
