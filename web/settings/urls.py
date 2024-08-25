from django.urls import path
from .views import dynamic_page_view, NotificationSeenView, NotificationAllSeenView, NotificationList

app_name = 'settings'

urlpatterns = [
    path('page/<slug:slug>/', dynamic_page_view, name='dynamic_page'),
    path('notification/list/', NotificationList.as_view(), name='notification_list'),
    path('notification/seen/', NotificationSeenView.as_view(), name='notification_seen'),
    path('notification/all-seen/', NotificationAllSeenView.as_view(), name='notification_all_seen'),
]
