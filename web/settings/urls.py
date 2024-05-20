from django.urls import path
from .views import notification_seen_view, notification_all_seen_view

app_name = 'settings'

urlpatterns = [
    path('notification/seen/', notification_seen_view, name='notification_seen'),
    path('notification/seen/all/', notification_all_seen_view, name='notification_all_seen'),
]
