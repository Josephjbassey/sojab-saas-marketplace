from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Project

@login_required
def list_view(request):
    projects = Project.objects.all().order_by('-created_at')
    return render(request, 'projects/list.html', {'projects': projects})

@login_required
def detail_view(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'projects/detail.html', {'project': project})
