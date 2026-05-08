from django.urls import path
from .views import customization_request_create, template_to_saas_customization

app_name = 'support'

urlpatterns = [
    path('template-to-saas-customization/', template_to_saas_customization, name='template_to_saas_customization'),
    path('customize/<slug:template_slug>/', customization_request_create, name='customization_request'),
]
