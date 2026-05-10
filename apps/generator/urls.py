from django.urls import path
from . import views

app_name = 'generator'

urlpatterns = [
    path('', views.project_list, name='list'),
    path('<uuid:pk>/', views.project_detail, name='detail'),
]
