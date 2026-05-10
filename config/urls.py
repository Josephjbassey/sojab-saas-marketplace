from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail import urls as wagtail_urls

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('admin/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),

    path('templates/', include('apps.templates_catalog.urls', namespace='templates_catalog')),
    path('purchases/', include('apps.purchases.urls', namespace='purchases')),
    path('billing/', include('apps.billing.urls', namespace='billing')),
    path('support/', include('apps.support.urls', namespace='support')),
    path('health/', include('apps.health.urls', namespace='health')),
    path('auth/', include('apps.accounts.urls', namespace='accounts')),
    path('', include('apps.marketplace.urls', namespace='marketplace')),
    path('organizations/', include('apps.organizations.urls', namespace='organizations')),
    path('notifications/', include('apps.notifications.urls', namespace='notifications')),
    path('generator/', include('apps.generator.urls', namespace='generator')),
    path('', include(wagtail_urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
