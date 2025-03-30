import logging

from django.shortcuts import get_object_or_404, render
from django.db import transaction
from rest_framework.generics import ListAPIView
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Notification, DynamicPage
from .serializers import NotificationSerializer

logger = logging.getLogger(__name__)


def dynamic_page_view(request, slug, *args, **kwargs):
    page = get_object_or_404(
        DynamicPage.objects.prefetch_related('media'),
        translations__slug=slug,
        is_active=True
    )

    context = {
        "Title": page.title,
        "page": page,
    }

    return render(request, 'pages/main/dynamic_pages.html', context)


class NotificationList(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user, is_active=True)


class NotificationSeenView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        notification_id = request.data.get('id')
        if not notification_id:
            return Response({'success': False, 'error': 'No ID provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            notification = get_object_or_404(Notification, id=notification_id, user=request.user)
            notification.mark_as_seen()
            return Response({'success': True}, status=status.HTTP_200_OK)
        except Notification.DoesNotExist:
            return Response({'success': False, 'error': 'Notification not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error marking notification as seen: {e}")
            return Response(
                {'success': False, 'error': 'Internal server error'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class NotificationAllSeenView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        try:
            notifications = Notification.objects.filter(user=request.user, has_seen=False)
            if notifications.exists():
                notifications.update(has_seen=True)
            return Response({'success': True}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error marking all notifications as seen: {e}")
            return Response(
                {'success': False, 'error': 'Internal server error'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
