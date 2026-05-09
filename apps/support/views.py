from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import CustomizationRequestForm
from apps.templates_catalog.models import SaaSTemplate
from apps.notifications.services import notify_user
from apps.audit.services import log_action


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
            custom_request.save()

            # Send notification to the user
            notify_user(
                user=request.user,
                title="Customization Request Received",
                message=f"We have received your customization request for {template.name}. Our team will review it shortly.",
                metadata={"request_id": str(custom_request.id)}
            )

            # Log audit event
            log_action(
                actor=request.user,
                action='customization_request_created',
                resource=custom_request, organization=custom_request.organization,
                message=f"Customization request created for {template.name}",
                request=request,
                metadata={"request_id": str(custom_request.id)}
            )

            return render(request, 'support/success.html', {'template': template})
    else:
        form = CustomizationRequestForm(template=template)

    return render(request, 'support/customization_request_form.html', {
        'form': form,
        'template': template
    })
