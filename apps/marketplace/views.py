from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.purchases.models import TemplatePurchase
from apps.support.models import CustomizationRequest
from apps.deployments.models import ClientProject

@login_required
def dashboard_home(request):
    recent_purchases = TemplatePurchase.objects.filter(user=request.user).order_by('-created_at')[:5]
    active_projects = ClientProject.objects.filter(user=request.user).order_by('-created_at')
    recent_requests = CustomizationRequest.objects.filter(user=request.user).order_by('-created_at')[:5]
    
    return render(request, 'marketplace/dashboard/home.html', {
        'recent_purchases': recent_purchases,
        'active_projects': active_projects,
        'recent_requests': recent_requests,
    })

@login_required
def purchase_history(request):
    purchases = TemplatePurchase.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'marketplace/dashboard/purchase_history.html', {
        'purchases': purchases
    })
