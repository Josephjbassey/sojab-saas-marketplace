from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import CustomizationRequestForm
from apps.templates_catalog.models import SaaSTemplate

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
            # In a real app, send email notification here
            return render(request, 'support/success.html', {'template': template})
    else:
        form = CustomizationRequestForm(template=template)
    
    return render(request, 'support/customization_request_form.html', {
        'form': form,
        'template': template
    })
