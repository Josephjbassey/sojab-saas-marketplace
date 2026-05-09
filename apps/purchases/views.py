from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.templates_catalog.models import TemplatePackage
from .models import TemplatePurchase
from apps.billing.services import get_payment_service
from apps.notifications.services import notify_user
from apps.audit.services import log_action
from apps.audit.models import AuditLog
from apps.emails.services import send_template_email, build_email_context

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

        user_orgs = request.user.memberships.select_related('organization')
        organization_id = request.POST.get('organization_id')

        # Multi-org users must explicitly choose an organization to avoid misattribution.
        if organization_id:
            selected_membership = user_orgs.filter(organization_id=organization_id).first()
            if not selected_membership:
                messages.error(request, 'Invalid organization selected.')
                purchase.delete()
                return redirect('purchases:checkout', package_id=package_id)
            purchase.organization = selected_membership.organization
            purchase.save(update_fields=['organization'])
        elif user_orgs.count() == 1:
            purchase.organization = user_orgs.first().organization
            purchase.save(update_fields=['organization'])
        elif user_orgs.count() > 1:
            messages.error(request, 'Please select an organization to continue checkout.')
            purchase.delete()
            return redirect('purchases:checkout', package_id=package_id)

        # Process dummy payment
        payment_service = get_payment_service()
        result = payment_service.create_payment(purchase, package.price)

        if result.success:
            confirmation = payment_service.confirm_payment(purchase)
            if confirmation.success:
                # Notifications & Audit & Email
                notify_user(
                    request.user,
                    "Purchase Successful",
                    f"You have successfully purchased {template.name}.",
                    organization=purchase.organization
                )
                log_action(
                    request.user,
                    AuditLog.ACTION_PAYMENT_COMPLETED,
                    resource=purchase,
                    organization=purchase.organization,
                    request=request,
                    message=f"Purchased {template.name}"
                )
                send_template_email(
                    "Your Purchase Confirmation",
                    [request.user.email],
                    "purchase_confirmation",
                    build_email_context(request.user, purchase=purchase)
                )

                messages.success(request, 'Purchase completed successfully!')
                return redirect('purchases:success', purchase_id=purchase.id)

        # Payment failed
        payment_service.mark_purchase_failed(purchase, 'Payment processing failed')
        log_action(
            request.user,
            AuditLog.ACTION_PAYMENT_FAILED,
            resource=purchase,
            organization=purchase.organization,
            request=request,
            message=f"Purchase failed for {template.name}"
        )
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
        # Notifications & Audit & Email
        notify_user(
            request.user,
            "Purchase Confirmed",
            f"Your purchase for {purchase.template.name} has been confirmed.",
            organization=purchase.organization
        )
        log_action(
            request.user,
            AuditLog.ACTION_PAYMENT_COMPLETED,
            resource=purchase,
            organization=purchase.organization,
            request=request,
            message=f"Purchase confirmed for {purchase.template.name}"
        )
        send_template_email(
            "Your Purchase Confirmation",
            [request.user.email],
            "purchase_confirmation",
            build_email_context(request.user, purchase=purchase)
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
