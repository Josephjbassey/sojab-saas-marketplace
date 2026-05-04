from django.urls import path
from . import views

app_name = 'purchases'

urlpatterns = [
    path('checkout/<uuid:package_id>/', views.checkout, name='checkout'),
    path('confirm/<uuid:purchase_id>/', views.confirm_purchase, name='confirm'),
    path('success/<uuid:purchase_id>/', views.purchase_success, name='success'),
]
