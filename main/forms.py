from django import forms
from main.models import Device, PaymentMethod
from django.utils.translation import gettext_lazy as _


class PaymentMethodForm(forms.ModelForm):
    class Meta:
        model = PaymentMethod
        fields = '__all__'
        exclude = ["user", "is_active"]
        widgets = {
            "account_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": _("Enter the name of the account")}
            ),
            "account_number": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": _("Enter the name of the account")}
            ),
            "bank_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": _("Enter the name of the account")}
            ),
            "swift_number": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": _("Enter the name of the account")}
            ),
            "iban_number": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": _("Enter the name of the account")}
            ),
            "country": forms.Select(
                attrs={"class": "form-select"}
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
