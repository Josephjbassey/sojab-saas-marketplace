from django.urls import path
from .views import customization_request_create

app_name = 'support'

urlpatterns = [
    path('customize/<slug:template_slug>/', customization_request_create, name='customization_request'),
]
