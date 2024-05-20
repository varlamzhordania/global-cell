from django.contrib import admin
from django.utils.html import format_html
from django.shortcuts import redirect
from django.urls import path
from django.contrib.auth import get_user_model

from .models import Device, Country, PaymentMethod, Notification
from .forms import NotificationForm


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'has_seen', 'is_active', 'priority', 'created_at', 'updated_at',)
    list_filter = ('has_seen', 'is_active', 'priority', 'created_at', 'updated_at',)
    search_fields = ('id', 'title', 'user',)


class NotificationInline(admin.StackedInline):
    model = Notification
    form = NotificationForm
    min_num = 0
    extra = 1

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user" or db_field.name == "device" or db_field.name == "payment_method":
            obj_id = request.resolver_match.kwargs.get('object_id')
            if obj_id:
                payment_method = PaymentMethod.objects.filter(pk=obj_id).first()
                if payment_method:
                    if db_field.name == "user":
                        kwargs["queryset"] = get_user_model().objects.filter(id=payment_method.user.id)
                    if db_field.name == "device":
                        kwargs["queryset"] = Device.objects.filter(user=payment_method.user)
                else:
                    devices = Device.objects.filter(pk=obj_id).first()
                    if devices:
                        if db_field.name == "user":
                            kwargs["queryset"] = get_user_model().objects.filter(id=devices.user.id)
                        if db_field.name == "payment_method":
                            kwargs["queryset"] = PaymentMethod.objects.filter(user=devices.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'account_name', 'account_number', 'bank_name', 'is_active', 'action')
    list_filter = ("is_active",)
    search_fields = ("id", 'user__username', 'account_number')
    inlines = [NotificationInline]

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
    inlines = [NotificationInline]
