from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.purchases.models import TemplatePurchase
from apps.support.models import CustomizationRequest
from apps.generator.models import GeneratedProject
from apps.deployments.models import ClientProject
from apps.notifications.services import get_unread_count

@login_required
def dashboard_home(request):
    recent_purchases = TemplatePurchase.objects.filter(user=request.user).order_by('-created_at')[:5]

    # Combined view of GeneratedProject and ClientProject for backward compatibility with existing tests
    active_generated = GeneratedProject.objects.filter(user=request.user).order_by('-created_at')[:5]
    active_deployments = ClientProject.objects.filter(user=request.user).order_by('-created_at')[:5]

    recent_requests = CustomizationRequest.objects.filter(user=request.user).order_by('-created_at')[:5]
    unread_count = get_unread_count(request.user)
    
    return render(request, 'marketplace/dashboard/home.html', {
        'recent_purchases': recent_purchases,
        'active_projects': active_generated,
        'active_deployments': active_deployments,
        'recent_requests': recent_requests,
        'unread_count': unread_count,
    })

@login_required
def purchase_history(request):
    purchases = TemplatePurchase.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'marketplace/dashboard/purchase_history.html', {
        'purchases': purchases
    })
