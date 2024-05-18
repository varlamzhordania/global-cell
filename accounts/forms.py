from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import PasswordChangeForm as BasePasswordChangeForm

from .models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'middle_name', 'phone_number']
        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': _('Enter your first name'),
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': _('Enter your last name'),
                }
            ),
            "middle_name": forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': _('Enter your middle name'),
                }
            ),
            "phone_number": forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': _('Enter your phone number'),
                }
            ),
        }
        help_texts = {
            'first_name': _('Your given name.'),
            'last_name': _('Your family name.'),
            'middle_name': _('Your middle name, if you have one.'),
            'phone_number': _('Your contact number, example +12125552368.'),
        }


class PasswordChangeForm(BasePasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget = forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('Enter your old password'),
            }
        )
        self.fields['new_password1'].widget = forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('Enter your new password'),
            }
        )
        self.fields['new_password2'].widget = forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('Confirm your new password'),
            }
        )

    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']