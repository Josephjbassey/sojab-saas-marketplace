from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Lead

@login_required
def list_view(request):
    leads = Lead.objects.all().order_by('-created_at')

    # Simple search
    q = request.GET.get('q')
    if q:
        leads = leads.filter(title__icontains=q)

    if request.headers.get('HX-Request'):
        return render(request, 'leads/_list_results.html', {'leads': leads})

    return render(request, 'leads/list.html', {'leads': leads})

@login_required
def detail_view(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    return render(request, 'leads/detail.html', {'lead': lead})

@login_required
def update_status(request, pk):
    if request.method == 'POST':
        lead = get_object_or_404(Lead, pk=pk)
        new_status = request.POST.get('status')
        if new_status in dict(Lead.STATUS_CHOICES):
            lead.status = new_status
            lead.save()

        if request.headers.get('HX-Request'):
            return render(request, 'leads/_status_badge.html', {'lead': lead})

    return HttpResponse(status=400)
