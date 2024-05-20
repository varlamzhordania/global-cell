from django.conf import settings

from settings.models import Notification


def Default(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user=request.user, is_active=True)
        return {
            'notifications': notifications,
            'unseen_notifications': notifications.filter(has_seen=False),
            'asset_version': settings.STATIC_VERSION
        }
    else:
        return {
            'asset_version': settings.STATIC_VERSION
        }
