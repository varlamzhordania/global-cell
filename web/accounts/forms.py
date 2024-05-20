from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm as BasePasswordChangeForm, SetPasswordForm, \
    PasswordResetForm
from django.contrib.auth.password_validation import password_validators_help_text_html

from .models import User


class StylesCustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label=_("New password"),
        help_text=password_validators_help_text_html(),
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "off",
                "class": "form-control",
                "placeholder": _("Enter new password for your account"),
            }
        ),
        strip=False,
    )
    new_password2 = forms.CharField(
        label=_("Password Confirmation"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "off",
                "class": "form-control",
                "placeholder": "Retype your password here",
            }
        ),
    )


class StylesCustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "example@example.com",
            }
        ),
    )


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        help_text=_("Required. Enter a valid email address."),
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': "example@example.com"})
    )
    password1 = forms.CharField(
        max_length=128,
        min_length=8,
        label=_("Password"),
        required=True,
        help_text=password_validators_help_text_html(),
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "********",
                "autocomplete": "off",
            }
        )
    )
    password2 = forms.CharField(
        max_length=128, min_length=8, label=_("Confirm Password"), required=True, widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Retype your password here",
                "autocomplete": "off",
            }
        )
    )

    class Meta:
        model = User
        fields = (
            "first_name", "last_name", "email", "password1", "password2"
        )
        widgets = {
            'first_name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': _("Enter your first name here")}
            ),
            'last_name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': _("Enter your last name here")}
            ),
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_("A user with that email already exists."))
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.email
        if commit:
            user.save()
        return user


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
