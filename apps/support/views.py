import logging
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import CustomizationRequestForm
from .models import CustomizationRequest
from apps.templates_catalog.models import SaaSTemplate
from apps.notifications.services import notify_user
from apps.audit.services import log_action
from apps.audit.models import AuditLog
from apps.emails.services import send_template_email, build_email_context

logger = logging.getLogger(__name__)

def template_to_saas_customization(request):
    what_we_build = [
        "Django backend", "PostgreSQL database", "Wagtail CMS", "Auth system",
        "Admin dashboard", "Client dashboard", "Payment integration",
        "Email notifications", "Deployment setup"
    ]
    process_steps = [
        "Choose or provide a licensed template",
        "Define the business workflow",
        "Customize branding and pages",
        "Build backend and dashboard",
        "Connect payments/CMS",
        "Deploy and hand over"
    ]
    packages = [
        "Frontend Integration", "Backend Setup",
        "Full SaaS Launch", "Ongoing Maintenance"
    ]

    return render(request, 'support/template_to_saas_customization.html', {
        'what_we_build': what_we_build,
        'process_steps': process_steps,
        'packages': packages,
    })

@login_required
def customization_request_create(request, template_slug):
    template = get_object_or_404(SaaSTemplate, slug=template_slug, is_active=True)

    if request.method == 'POST':
        form = CustomizationRequestForm(request.POST, template=template)
        if form.is_valid():
            custom_request = form.save(commit=False)
            custom_request.user = request.user
            custom_request.template = template

            # Deterministic organization selection (e.g. by creation date)
            user_orgs = request.user.memberships.order_by('created_at')
            if user_orgs.exists():
                custom_request.organization = user_orgs.first().organization

            custom_request.save()

            # Post-save side effects (Notifications, Audit, Email) in safe block
            try:
                notify_user(
                    request.user,
                    "Request Received",
                    f"We received your request for {template.name}.",
                    organization=custom_request.organization
                )
                log_action(
                    request.user,
                    AuditLog.ACTION_CUSTOMIZATION_REQUEST_CREATED,
                    resource=custom_request,
                    organization=custom_request.organization,
                    request=request
                )
                send_template_email(
                    "Customization Request Received",
                    [request.user.email],
                    "customization_request_received",
                    build_email_context(request.user, request_obj=custom_request)
                )
            except Exception as e:
                logger.exception(
                    f"Error processing side effects for CustomizationRequest {custom_request.id} (User: {request.user.id})"
                )

            return render(request, 'support/success.html', {'template': template})
    else:
        form = CustomizationRequestForm(template=template)

    return render(request, 'support/customization_request_form.html', {
        'form': form,
        'template': template
    })

@login_required
def request_list(request):
    requests = CustomizationRequest.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'support/request_list.html', {
        'requests': requests
    })

@login_required
def request_detail(request, pk):
    custom_request = get_object_or_404(CustomizationRequest, pk=pk, user=request.user)
    return render(request, 'support/request_detail.html', {
        'request_obj': custom_request
    })
