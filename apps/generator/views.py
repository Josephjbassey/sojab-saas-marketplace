from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import GeneratedProject

@login_required
def project_list(request):
    projects = GeneratedProject.objects.filter(user=request.user).select_related(
        'template', 'organization', 'purchase'
    ).order_by('-created_at')
    return render(request, 'generator/list.html', {
        'projects': projects
    })

@login_required
def project_detail(request, pk):
    project = get_object_or_404(GeneratedProject, pk=pk, user=request.user)
    return render(request, 'generator/detail.html', {
        'project': project
    })
