from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.

class User(AbstractUser):
    email = models.EmailField(_("email address"), blank=True, unique=True)
    middle_name = models.CharField(max_length=255, verbose_name=_("Middle Name"), blank=True, null=True, unique=False)
    phone_number = PhoneNumberField(blank=True, null=True, verbose_name=_("Phone Number"))
    wallet = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        default=0,
        verbose_name=_("Wallet"),
        validators=[MinValueValidator(0)]
    )
    last_ip = models.GenericIPAddressField(verbose_name=_("Last IP Address"), null=True, blank=True)

    def __str__(self):
        return self.username

    @property
    def get_full_name(self):
        if not self.first_name and not self.last_name:
            return self.username
        return f"{self.first_name} {self.last_name}"

    @property
    def get_initials_name(self):
        if not self.first_name or not self.last_name:
            return self.username[0:2]
        return f"{self.first_name[0]}{self.last_name[0]}"

    @property
    def get_wallet_display(self):
        return f"${self.wallet}"
