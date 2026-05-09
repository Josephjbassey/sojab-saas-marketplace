from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from apps.audit.services import log_action
from apps.audit.models import AuditLog

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            log_action(user, AuditLog.ACTION_REGISTER, resource=user, request=request, message="User registered")
            login(request, user)
            return redirect('marketplace:dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})
