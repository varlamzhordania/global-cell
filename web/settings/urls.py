from django.urls import path
from .views import NotificationSeenView, NotificationAllSeenView, NotificationList

app_name = 'settings'

urlpatterns = [
    path('notification/list/', NotificationList.as_view(), name='notification_list'),
    path('notification/seen/', NotificationSeenView.as_view(), name='notification_seen'),
    path('notification/all-seen/', NotificationAllSeenView.as_view(), name='notification_all_seen'),
]
