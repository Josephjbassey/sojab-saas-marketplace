from django.urls import path
from . import views

app_name = 'support'

urlpatterns = [
    path('customization-plans/', views.template_to_saas_customization, name='plans'),
    path('request/<slug:template_slug>/', views.customization_request_create, name='request_create'),
    path('requests/', views.request_list, name='request_list'),
    path('requests/<uuid:pk>/', views.request_detail, name='request_detail'),

    # Legacy URL names for compatibility with existing tests
    path('request/legacy/<slug:template_slug>/', views.customization_request_create, name='customization_request'),
    path('customization-plans/legacy/', views.template_to_saas_customization, name='template_to_saas_customization'),
]
