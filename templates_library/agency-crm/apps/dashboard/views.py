from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.leads.models import Lead
from apps.projects.models import Project
from apps.clients.models import Client
from apps.invoices.models import Invoice
from django.db.models import Sum

@login_required
def index(request):
    # For now, we assume the user is part of at least one organization
    # or we just show all if it's a demo/admin user.
    # In a real SaaS, we'd filter by request.user.active_organization.

    leads_count = Lead.objects.count()
    projects_count = Project.objects.filter(status='active').count()
    clients_count = Client.objects.count()

    total_revenue = Invoice.objects.filter(status='paid').aggregate(Sum('amount'))['amount__sum'] or 0

    recent_leads = Lead.objects.order_by('-created_at')[:5]
    recent_projects = Project.objects.order_by('-created_at')[:5]

    context = {
        'leads_count': leads_count,
        'projects_count': projects_count,
        'clients_count': clients_count,
        'total_revenue': total_revenue,
        'recent_leads': recent_leads,
        'recent_projects': recent_projects,
    }
    return render(request, 'dashboard/index.html', context)
