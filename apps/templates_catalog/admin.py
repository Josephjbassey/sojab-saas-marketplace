from django.contrib import admin
from .models import TemplateCategory, SaaSTemplate, TemplatePackage, TemplateFeature, TemplateScreenshot

class TemplatePackageInline(admin.TabularInline):
    model = TemplatePackage
    extra = 1

class TemplateFeatureInline(admin.TabularInline):
    model = TemplateFeature
    extra = 1

class TemplateScreenshotInline(admin.TabularInline):
    model = TemplateScreenshot
    extra = 1

@admin.register(TemplateCategory)
class TemplateCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(SaaSTemplate)
class SaaSTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'is_active', 'is_featured', 'created_at')
    list_filter = ('category', 'is_active', 'is_featured')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [TemplatePackageInline, TemplateFeatureInline, TemplateScreenshotInline]

@admin.register(TemplatePackage)
class TemplatePackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'template', 'price', 'is_active')
    list_filter = ('template', 'is_active')
    search_fields = ('name', 'template__name')

@admin.register(TemplateFeature)
class TemplateFeatureAdmin(admin.ModelAdmin):
    list_display = ('name', 'template')
    list_filter = ('template',)

@admin.register(TemplateScreenshot)
class TemplateScreenshotAdmin(admin.ModelAdmin):
    list_display = ('template', 'caption', 'order')
    list_filter = ('template',)
