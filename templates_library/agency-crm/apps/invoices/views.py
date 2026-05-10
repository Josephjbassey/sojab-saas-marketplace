from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Invoice

@login_required
def list_view(request):
    invoices = Invoice.objects.all().order_by('-due_date')
    return render(request, 'invoices/list.html', {'invoices': invoices})

@login_required
def detail_view(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    return render(request, 'invoices/detail.html', {'invoice': invoice})
