from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('admin/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),

    path('dashboard/', include('apps.dashboard.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('leads/', include('apps.leads.urls')),
    path('clients/', include('apps.clients.urls')),
    path('projects/', include('apps.projects.urls')),
    path('invoices/', include('apps.invoices.urls')),

    re_path(r'', include(wagtail_urls)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
