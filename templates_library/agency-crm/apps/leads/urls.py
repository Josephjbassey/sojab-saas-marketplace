from django.urls import path
from . import views

app_name = 'leads'

urlpatterns = [
    path('', views.list_view, name='list'),
    path('<uuid:pk>/', views.detail_view, name='detail'),
    path('<uuid:pk>/status/', views.update_status, name='update_status'),
]
