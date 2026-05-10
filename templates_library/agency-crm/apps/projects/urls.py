from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('', views.list_view, name='list'),
    path('<uuid:pk>/', views.detail_view, name='detail'),
]
