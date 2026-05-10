from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Notification

@login_required
def notification_list(request):
    notifications = request.user.notifications.all().order_by('-created_at')
    return render(request, 'notifications/list.html', {
        'notifications': notifications
    })

@login_required
def mark_as_read(request, pk):
    notification = get_object_or_404(Notification, pk=pk, recipient=request.user)
    notification.mark_as_read()

    if request.headers.get('HX-Request'):
        return HttpResponse(status=204)

    return redirect('notifications:list')
