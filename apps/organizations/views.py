from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import Organization, Membership
from .permissions import can_view_organization, can_manage_members

@login_required
def organization_list(request):
    memberships = request.user.memberships.all().select_related('organization')
    return render(request, 'organizations/list.html', {
        'memberships': memberships
    })

@login_required
def organization_detail(request, slug):
    organization = get_object_or_404(Organization, slug=slug, is_active=True)

    if not can_view_organization(request.user, organization):
        messages.error(request, "You do not have access to this organization.")
        return redirect('organizations:list')

    members = organization.memberships.all().select_related('user')
    can_manage = can_manage_members(request.user, organization)

    return render(request, 'organizations/detail.html', {
        'organization': organization,
        'members': members,
        'can_manage': can_manage
    })

@login_required
@require_POST
def switch_organization(request, slug):
    organization = get_object_or_404(Organization, slug=slug, is_active=True)

    if not can_view_organization(request.user, organization):
        messages.error(request, "You do not have access to this organization.")
        return redirect('marketplace:dashboard')

    request.session['active_organization_id'] = str(organization.id)
    messages.success(request, f"Switched to {organization.name}")
    return redirect('marketplace:dashboard')
