from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Client

@login_required
def list_view(request):
    clients = Client.objects.all().order_by('name')
    return render(request, 'clients/list.html', {'clients': clients})

@login_required
def detail_view(request, pk):
    client = get_object_or_404(Client, pk=pk)
    return render(request, 'clients/detail.html', {'client': client})
