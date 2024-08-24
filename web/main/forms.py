from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from settings.models import Notification

from .models import Device, PaymentMethod, Country


class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['user', 'device', 'payment_method', 'message', 'has_seen', 'is_active']


class PaymentMethodForm(forms.ModelForm):
    country = forms.ModelChoiceField(
        queryset=Country.objects.filter(is_supported=True), label=_("Country"), required=True, widget=forms.Select(
            attrs={"class": "form-select"}
        ), )

    class Meta:
        model = PaymentMethod
        fields = '__all__'
        exclude = ["user", "is_active"]
        widgets = {
            "account_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": _("Enter the name of the account")}
            ),
            "account_number": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": _("Enter the account number"),
                       "autocomplete": "off"}
            ),
            "bank_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": _("Enter the bank name")}
            ),
            "swift_number": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": _("Enter the SWIFT number"),
                       "autocomplete": "off"}
            ),
            "iban_number": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": _("Enter the IBAN number"),
                       "autocomplete": "off"}
            ),
        }


class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = '__all__'
        exclude = ["user", "is_active", "is_verified"]
        widgets = {
            "mobile_carrier": forms.TextInput(
                attrs={"class": "form-control", "placeholder": _("Enter the name of the company")}
            ),
            "plan_payment": forms.Select(attrs={"class": "form-select"}),
            "plan_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": _("Enter the name of the plan")}
            ),
            "plan_cost": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": _("Enter the cost of the plan ")}
            ),
            "plan_length": forms.NumberInput(attrs={"class": "form-control"}),
            "total_minutes": forms.NumberInput(attrs={"class": "form-control"}),
            "is_unlimited_minutes": forms.CheckboxInput(attrs={"class": "form-check-box"}),

        }
        error_messages = {
            "sim_number": {
                "required": _("Please enter a phone number."),
                "invalid": _("Please enter a valid International phone number of chosen country."),
            },
        }
