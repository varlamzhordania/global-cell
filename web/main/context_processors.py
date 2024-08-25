from django.conf import settings

from settings.models import Notification


def Default(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user=request.user, is_active=True, has_seen=False)
        return {
            'unseen_notifications': notifications,
            'asset_version': settings.STATIC_VERSION,
            'debug': settings.DEBUG
        }
    else:
        return {
            'asset_version': settings.STATIC_VERSION,
            'debug': settings.DEBUG
        }
