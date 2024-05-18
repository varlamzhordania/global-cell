from django.contrib import admin
from .models import Device, Country, PaymentMethod
from django.utils.html import format_html
from django.shortcuts import redirect
from django.urls import path


# Register your models here.


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'account_name', 'account_number', 'bank_name', 'is_active', 'action')
    list_filter = ("is_active",)
    search_fields = ("id", 'user__username', 'account_number')

    def action(self, obj):
        if obj.is_active:
            return format_html('<a href="{}">Deactivate</a>', self.get_toggle_status_url(obj.id))
        else:
            return format_html('<a href="{}">Activate</a>', self.get_toggle_status_url(obj.id))

    action.short_description = 'Action'

    def get_toggle_status_url(self, pk):
        return f'/admin/{self.model._meta.app_label}/{self.model._meta.model_name}/{pk}/toggle-status/'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:pk>/toggle-status/',
                self.admin_site.admin_view(self.toggle_status),
                name='paymentmethod_toggle_status'
            ),
        ]
        return custom_urls + urls

    def toggle_status(self, request, pk, *args, **kwargs):
        payment_method = self.get_object(request, pk)
        if payment_method:
            payment_method.is_active = not payment_method.is_active
            payment_method.save()
        return redirect('admin:{}_{}_changelist'.format(self.model._meta.app_label, self.model._meta.model_name))


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', "short_name", "phone_prefix", "currency_name", "currency_sign", "to_dollar",
        "is_supported",
    )
    list_filter = ("is_supported",)
    search_fields = ("id", 'name', 'short_name', 'currency_name')

    def to_dollar(self, value):
        return format_html('<span>${}</span>', value.equivalent_to_dollar)


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'sim_number', 'mobile_carrier', 'plan_payment', 'plan_name', 'plan_cost', 'plan_length',
        'is_unlimited_minutes',
        'is_verified', 'is_active',
    )
    list_filter = ('is_unlimited_minutes', 'is_verified', 'is_active',)
    search_fields = ("id", 'user', 'sim_number')
