from django.urls import path
from . import views

app_name = 'billing'

urlpatterns = [
    path('paystack/webhook/', views.paystack_webhook, name='paystack_webhook'),
    path('paystack/callback/', views.paystack_callback, name='paystack_callback'),
]
