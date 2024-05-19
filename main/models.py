from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
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
    phone_prefix = models.CharField(
        max_length=5,
        verbose_name=_("Country Phone Prefix"),
        blank=True,
        null=True,
        help_text=_("The phone number prefix for the country.")
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
        blank=False,
        null=False
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
        blank=False,
        validators=[
            RegexValidator(
                regex='^\d{10,50}$',
                message=_("Account number must be between 10 and 50 digits."),
                code='invalid_account_number'
            )
        ]
    )
    bank_name = models.CharField(
        max_length=100,
        verbose_name=_("Bank Name"),
        null=False,
        blank=False
    )
    swift_number = models.CharField(
        max_length=11,
        verbose_name=_("SWIFT Number"),
        null=True,
        blank=True,
        validators=[
            RegexValidator(
                regex='^[A-Z0-9]{8,11}$',
                message=_("SWIFT number must be between 8 and 11 characters."),
                code='invalid_swift_number'
            )
        ]
    )
    iban_number = models.CharField(
        max_length=34,
        verbose_name=_("IBAN Number"),
        null=True,
        blank=True,
        validators=[
            RegexValidator(
                regex='^[A-Z0-9]{15,34}$',
                message=_("IBAN number must be between 15 and 34 characters."),
                code='invalid_iban_number'
            )
        ]
    )
    country = models.ForeignKey(
        'Country',
        verbose_name=_("Country"),
        related_name="payment_methods",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _("Payment Method")
        verbose_name_plural = _("Payment Methods")
        indexes = [
            models.Index(fields=['user', 'account_number']),
        ]
        ordering = ['user', 'bank_name']
        unique_together = (('user', 'account_number'),)

    def __str__(self):
        return f"{self.user}'s Payment Method at {self.bank_name}"

    @property
    def get_account_number_display(self):
        return self.mask_number(self.account_number)

    @property
    def get_swift_number_display(self):
        return self.mask_number(self.swift_number)

    @property
    def get_iban_number_display(self):
        return self.mask_number(self.iban_number)

    def mask_number(self, number):
        if not number:
            return ""
        length = len(number)
        if length <= 4:
            return number
        start = number[:4]
        end = number[-4:]
        masked = '*' * (length - 8)
        return f"{start}{masked}{end}"


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
    sim_number = PhoneNumberField(verbose_name=_("SIM Number"), blank=False, null=False)
    mobile_carrier = models.CharField(
        max_length=100,
        verbose_name=_("Mobile Carrier"),
        null=False,
        blank=False
    )
    plan_payment = models.CharField(
        max_length=50,
        verbose_name=_("Plan Payment"),
        choices=PlanPaymentChoices.choices, default=PlanPaymentChoices.POST_PAID,
    )
    plan_name = models.CharField(
        max_length=100,
        verbose_name=_("Plan Name"),
        null=False,
        blank=False
    )
    plan_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Plan Cost"),
        help_text=_("Plan cost Based on USD Dollar ($)"),
        null=False,
        blank=False,
        default=0
    )
    plan_length = models.PositiveSmallIntegerField(
        verbose_name=_("Plan Length (Months)"),
        null=True,
        blank=True,
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(12)]
    )
    is_unlimited_minutes = models.BooleanField(
        verbose_name=_("Unlimited Minutes"),
        default=False
    )
    total_minutes = models.PositiveIntegerField(
        verbose_name=_("Total Minutes"),
        null=True,
        blank=True,
        default=0,
    )
    earned = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Earned"),
        help_text=_("Total earned"),
        default=0,
        validators=[MinValueValidator(0)],
        blank=True,
    )
    is_verified = models.BooleanField(verbose_name="Verified", default=False)
    is_active = models.BooleanField(verbose_name=_("Is Active"), default=False)

    class Meta:
        verbose_name = _("Device")
        verbose_name_plural = _("Devices")
        ordering = ["-created_at"]
        unique_together = (("user", "sim_number", "is_active"),)

    def __str__(self):
        return f"{self.user}'s Device"


class Notification(BaseModel):
    class PriorityChoices(models.TextChoices):
        LOW = "Low", _("Low")
        MEDIUM = "Medium", _("Medium")
        HIGH = "High", _("High")

    user = models.ForeignKey(
        get_user_model(),
        related_name="notifications",
        on_delete=models.CASCADE
    )
    device = models.ForeignKey(
        Device,
        on_delete=models.CASCADE,
        related_name="notifications",
        verbose_name=_("Device"),
        blank=True,
        null=True,
        help_text=_("If the notification related to this device")
    )
    payment_method = models.ForeignKey(
        PaymentMethod,
        on_delete=models.CASCADE,
        related_name="notifications",
        verbose_name=_("Bank Account"),
        blank=True,
        null=True,
        help_text=_("If the notification related to this bank account")
    )
    title = models.CharField(max_length=255, verbose_name=_("Title"), blank=False, null=False)
    message = models.TextField(verbose_name=_("Message"), blank=False, null=False)
    has_seen = models.BooleanField(
        verbose_name=_("Has Seen"),
        default=False,
        help_text=_("Has User Seen Notification?")
    )
    is_active = models.BooleanField(verbose_name=_("Visibility"), default=True)
    priority = models.CharField(
        max_length=20,
        choices=PriorityChoices.choices,
        default=PriorityChoices.MEDIUM,
        verbose_name=_("Priority")
    )

    class Meta:
        verbose_name = _("Notification")
        verbose_name_plural = _("Notifications")
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'has_seen']),
            models.Index(fields=['is_active', 'priority']),
        ]

    def __str__(self):
        return f"{self.id} - {self.title}"

    def mark_as_seen(self):
        self.has_seen = True
        self.save(update_fields=['has_seen'])

    def mark_as_unseen(self):
        self.has_seen = False
        self.save(update_fields=['has_seen'])

    def soft_delete(self):
        self.is_active = False
        self.save(update_fields=['is_active'])
