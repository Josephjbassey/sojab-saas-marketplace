import json
import logging
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from apps.purchases.models import TemplatePurchase
from .services import get_payment_service
from .models import WebhookEvent

logger = logging.getLogger(__name__)

@csrf_exempt
@require_POST
def paystack_webhook(request):
    """Handle Paystack webhook notifications."""
    signature = request.META.get('HTTP_X_PAYSTACK_SIGNATURE')
    if not signature:
        return HttpResponse(status=400)

    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponse(status=400)

    # Log the event
    event_type = payload.get('event', 'unknown')
    webhook_event = WebhookEvent.objects.create(
        provider='paystack',
        event_type=event_type,
        payload=payload
    )

    # Process event
    payment_service = get_payment_service()
    if hasattr(payment_service, 'handle_webhook_event'):
        success = payment_service.handle_webhook_event(payload, signature)
        if success:
            webhook_event.processed = True
            webhook_event.save()
            return HttpResponse(status=200)

    return HttpResponse(status=400)

def paystack_callback(request):
    """Handle Paystack redirect after payment."""
    reference = request.GET.get('reference')
    if not reference:
        messages.error(request, "Invalid payment reference.")
        return redirect('marketplace:dashboard')

    purchase = get_object_or_404(TemplatePurchase, transaction_id=reference)

    if purchase.status == 'paid':
        return redirect('purchases:success', purchase_id=purchase.id)

    # Verify payment status immediately
    payment_service = get_payment_service()
    result = payment_service.confirm_payment(purchase)

    if result.success:
        messages.success(request, "Payment verified successfully!")
        return redirect('purchases:success', purchase_id=purchase.id)
    else:
        messages.error(request, f"Payment verification failed: {result.error}")
        return redirect('marketplace:dashboard')
