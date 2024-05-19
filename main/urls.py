from django.urls import path
from django.views.generic import TemplateView
from .views import home_view, dashboard_view, phones_create, phones_list, financial_view, delete_payment_method_view, \
    settings_view

app_name = 'main'

urlpatterns = [
    path('', home_view, name="home"),
    path('dashboard/', dashboard_view, name="dashboard"),
    path('phones/create/', phones_create, name="phones_create"),
    path('phones/list/', phones_list, name="phones_list"),
    path('financial/', financial_view, name="financial"),
    path('payment_method/delete/<int:pk>/', delete_payment_method_view, name="payment_method_delete"),
    path('settings/', settings_view, name="settings"),
    path("400/", TemplateView.as_view(template_name="400.html"), name="400"),
    path("404/", TemplateView.as_view(template_name="404.html"), name="404"),
    path("500/", TemplateView.as_view(template_name="500.html"), name="500"),
]
