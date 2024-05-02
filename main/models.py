from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField


class BaseModel(models.Model):
    created_at = models.DateTimeField(verbose_name=_("Date Created"), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(verbose_name=_("Date Updated"), auto_now=True)
    is_active = models.BooleanField(verbose_name=_("Is Active"), default=True)

    class Meta:
        abstract = True


class Country(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name=_("Name of Country"),
        unique=True,
        help_text=_("The country name is case insensitive."),
        blank=False,
        null=False
    )
    short_name = models.CharField(
        max_length=3,
        verbose_name=_("Short Name of Country"),
        unique=True,
        help_text=_("A short unique abbreviation for the country."),
        blank=False,
        null=False
    )
    currency_name = models.CharField(
        max_length=50,
        verbose_name=_("Currency of Country"),
        blank=False,
        null=False
    )
    currency_sign = models.CharField(
        max_length=5,
        verbose_name=_("Currency Sign"),
        blank=True,
        null=True
    )
    equivalent_to_dollar = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        verbose_name=_("Equivalent to 1 Dollar"),
        help_text=_("The value of the country's currency compared to 1 US Dollar."),
        blank=True,
        null=True
    )
    is_supported = models.BooleanField(
        verbose_name=_("Is Supported"),
        default=True,
        help_text=_("Is this country supported?")
    )

    class Meta:
        verbose_name = _("Country")
        verbose_name_plural = _("Countries")
        ordering = ['name']

    def __str__(self):
        return self.name


class PaymentMethod(BaseModel):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='payment_methods',
        blank=False, null=False
    )
    account_name = models.CharField(
        max_length=100,
        verbose_name=_("Account Name"),
        null=False,
        blank=False
    )
    account_number = models.CharField(
        max_length=50,
        verbose_name=_("Account Number"),
        null=False,
        blank=False
    )
    bank_name = models.CharField(
        max_length=100,
        verbose_name=_("Bank Name"),
        null=False,
        blank=False
    )
    swift_number = models.CharField(
        max_length=50,
        verbose_name=_("SWIFT Number"),
        null=True,
        blank=True
    )
    iban_number = models.CharField(
        max_length=50,
        verbose_name=_("IBAN Number"),
        null=True,
        blank=True
    )
    country = models.ForeignKey(
        Country,
        verbose_name=_("Country"),
        related_name="payment_methods",
        on_delete=models.SET_NULL,
        blank=True,
        null=True, )

    class Meta:
        verbose_name = _("Payment Method")
        verbose_name_plural = _("Payment Methods")

    def __str__(self):
        return f"{self.user}'s Payment Method"


# class DigitalBanking(models.Model):
#     user = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name='digital_banking'
#     )
#     digital_payment_name = models.CharField(
#         max_length=100,
#         verbose_name=_("Digital Payment Name"),
#         null=True,
#         blank=True
#     )
#     digital_payment_id = models.CharField(
#         max_length=100,
#         verbose_name=_("Digital Payment ID"),
#         null=True,
#         blank=True
#     )
#
#     class Meta:
#         verbose_name = _("Digital Banking")
#         verbose_name_plural = _("Digital Banking")
#
#     def __str__(self):
#         return f"{self.user}'s Digital Banking"


class Device(BaseModel):
    class PlanPaymentChoices(models.TextChoices):
        POST_PAID = "post_paid", _("Post Paid")
        PRE_PAID = "pre_paid", _("Pre Paid")

    user = models.ForeignKey(
        get_user_model(),
        related_name="devices",
        on_delete=models.CASCADE
    )
    sim_number = PhoneNumberField(verbose_name=_("SIM Number"), blank=False, null=False, unique=True)
    mobile_carrier = models.CharField(
        max_length=100,
        verbose_name=_("Mobile Carrier"),
        null=True,
        blank=True
    )
    plan_payment = models.CharField(
        max_length=50,
        verbose_name=_("Plan Payment"),
        choices=PlanPaymentChoices.choices, default=PlanPaymentChoices.POST_PAID,
    )
    plan_name = models.CharField(
        max_length=100,
        verbose_name=_("Plan Name"),
        null=True,
        blank=True
    )
    plan_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Plan Cost"),
        null=True,
        blank=True
    )
    plan_length = models.PositiveSmallIntegerField(
        verbose_name=_("Plan Length (Months)"),
        null=True,
        blank=True
    )
    is_unlimited_minutes = models.BooleanField(
        verbose_name=_("Unlimited Minutes"),
        default=False
    )
    total_minutes = models.PositiveIntegerField(
        verbose_name=_("Total Minutes"),
        null=True,
        blank=True
    )
    is_verified = models.BooleanField(verbose_name="Verified", default=False)
    is_active = models.BooleanField(verbose_name=_("Is Active"), default=False)

    class Meta:
        verbose_name = _("Device")
        verbose_name_plural = _("Devices")

    def __str__(self):
        return f"{self.user}'s Device"