from django.contrib import admin
from .models import Organization, Membership

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active', 'created_at')
    search_fields = ('name', 'slug')
    list_filter = ('is_active',)
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('id', 'created_at', 'updated_at')

@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'organization', 'role', 'created_at')
    search_fields = ('user__email', 'organization__name')
    list_filter = ('role', 'organization')
    readonly_fields = ('id', 'created_at', 'updated_at')
