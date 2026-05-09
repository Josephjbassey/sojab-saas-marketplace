from django.urls import path
from .views import health_live, health_ready, health_status

app_name = 'health'

urlpatterns = [
    path('', health_status, name='status'),
    path('live/', health_live, name='live'),
    path('ready/', health_ready, name='ready'),
]
