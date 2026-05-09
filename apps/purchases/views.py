from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.templates_catalog.models import TemplatePackage
from .models import TemplatePurchase
from apps.billing.services import get_payment_service
from apps.notifications.services import notify_user


@login_required
def checkout(request, package_id):
    """Show checkout page for a selected package."""
    package = get_object_or_404(TemplatePackage, id=package_id, is_active=True)
    template = package.template

    # Check for existing pending/paid purchase of same package by user
    existing = TemplatePurchase.objects.filter(
        user=request.user,
        package=package,
        status__in=['pending', 'paid']
    ).first()

    if existing and existing.status == 'paid':
        messages.info(request, 'You already own this license.')
        return redirect('purchases:success', purchase_id=existing.id)

    if request.method == 'POST':
        # Create purchase record
        purchase = TemplatePurchase.objects.create(
            user=request.user,
            template=template,
            package=package,
            amount_paid=package.price,
            status='pending',
        )

        # Process dummy payment
        payment_service = get_payment_service()
        result = payment_service.create_payment(purchase, package.price)

        if result.success:
            confirmation = payment_service.confirm_payment(purchase)
            if confirmation.success:
                notify_user(
                    user=request.user,
                    title="Purchase Successful",
                    message=f"Thank you for purchasing the {package.name} license for {template.name}.",
                    metadata={"purchase_id": str(purchase.id)}
                )
                messages.success(request, 'Purchase completed successfully!')
                return redirect('purchases:success', purchase_id=purchase.id)

        # Payment failed
        payment_service.mark_purchase_failed(purchase, 'Payment processing failed')
        messages.error(request, 'Payment failed. Please try again.')
        return redirect('purchases:checkout', package_id=package_id)

    return render(request, 'purchases/checkout.html', {
        'package': package,
        'template': template,
        'existing_pending': existing,
    })


@login_required
def confirm_purchase(request, purchase_id):
    """Confirm a pending purchase (for async payment flows)."""
    purchase = get_object_or_404(TemplatePurchase, id=purchase_id, user=request.user)

    if purchase.status == 'paid':
        return redirect('purchases:success', purchase_id=purchase.id)

    if purchase.status != 'pending':
        messages.error(request, 'This purchase cannot be confirmed.')
        return redirect('marketplace:dashboard')

    payment_service = get_payment_service()
    result = payment_service.confirm_payment(purchase)

    if result.success:
        notify_user(
            user=request.user,
            title="Purchase Confirmed",
            message=f"Your purchase of the {purchase.package.name} license for {purchase.template.name} has been confirmed.",
            metadata={"purchase_id": str(purchase.id)}
        )
        messages.success(request, 'Purchase confirmed!')
        return redirect('purchases:success', purchase_id=purchase.id)

    messages.error(request, 'Could not confirm payment.')
    return redirect('marketplace:dashboard')


@login_required
def purchase_success(request, purchase_id):
    """Show purchase success page."""
    purchase = get_object_or_404(TemplatePurchase, id=purchase_id, user=request.user)
    return render(request, 'purchases/success.html', {
        'purchase': purchase,
    })
