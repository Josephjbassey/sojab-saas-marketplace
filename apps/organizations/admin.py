from django.contrib import admin
from .models import Organization, Membership

class MembershipInline(admin.TabularInline):
    model = Membership
    extra = 1
    autocomplete_fields = ['user']

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'owner', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'slug', 'owner__email', 'owner__username')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('id', 'created_at', 'updated_at')
    inlines = [MembershipInline]
    raw_id_fields = ('owner',)

@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'organization', 'role', 'created_at')
    list_filter = ('role', 'organization', 'created_at')
    search_fields = ('user__email', 'user__username', 'organization__name')
    readonly_fields = ('id', 'created_at', 'updated_at')
    raw_id_fields = ('user', 'organization')
