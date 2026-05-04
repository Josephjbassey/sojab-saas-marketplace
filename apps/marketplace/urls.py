from django.urls import path
from . import views

app_name = 'marketplace'

urlpatterns = [
    path('dashboard/', views.dashboard_home, name='dashboard'),
    path('dashboard/purchases/', views.purchase_history, name='purchase_history'),
]
