import logging
from django.db import transaction
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from .models import Notification

logger = logging.getLogger(__name__)


@require_POST
@login_required
def notification_seen_view(request):
    id = request.POST.get('id')
    print(request.POST)
    if not id:
        return JsonResponse({'success': False, 'error': 'No ID provided'}, status=400)

    try:
        notification = get_object_or_404(Notification, id=id, user=request.user)
        notification.mark_as_seen()
        return JsonResponse({'success': True}, status=200)
    except Notification.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Notification not found'}, status=404)
    except Exception as e:
        logger.error(f"Error marking notification as seen: {e}")
        return JsonResponse({'success': False, 'error': 'Internal server error'}, status=500)


@require_POST
@login_required
@transaction.atomic
def notification_all_seen_view(request):
    try:
        notifications = Notification.objects.filter(user=request.user, has_seen=False)
        if notifications.exists():
            notifications.update(has_seen=True)
        return JsonResponse({'success': True}, status=200)
    except Exception as e:
        logger.error(f"Error marking all notifications as seen: {e}")
        return JsonResponse({'success': False, 'error': 'Internal server error'}, status=500)
