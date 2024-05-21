from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.utils.timesince import timesince
from django.contrib.auth import get_user_model

from parler.models import TranslatableModel, TranslatedFields

from main.models import BaseModel, UploadPath, Device, PaymentMethod


# Create your models here.

class Notification(BaseModel):
    class PriorityChoices(models.TextChoices):
        LOW = "Low", _("Low")
        MEDIUM = "Medium", _("Medium")
        HIGH = "High", _("High")

    class StatusChoices(models.TextChoices):
        SUCCESS = "success", _("Success")
        ERROR = "error", _("Error")
        WARNING = "warning", _("Warning")
        INFO = "info", _("Info")

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
    message = models.CharField(max_length=255, verbose_name=_("Message"), blank=False, null=False)
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
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.INFO,
        verbose_name=_("Status")
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
        return f"{self.id} - {self.message}"

    def mark_as_seen(self):
        self.has_seen = True
        self.save(update_fields=['has_seen'])

    def mark_as_unseen(self):
        self.has_seen = False
        self.save(update_fields=['has_seen'])

    def soft_delete(self):
        self.is_active = False
        self.save(update_fields=['is_active'])

    def get_time_since_created(self):
        now = timezone.now()
        time_difference = timesince(self.created_at, now)
        return f"{time_difference} " + _("ago")


class Slide(TranslatableModel, BaseModel):
    title = models.CharField(max_length=255, verbose_name=_("Title"), blank=False, null=False)
    short_description = models.TextField(
        verbose_name=_("Short Description"),
        blank=False,
        null=False,
        help_text=_("A short description of the slide")
    )
    translations = TranslatedFields(
        image=models.ImageField(
            upload_to=UploadPath(folder="content", sub_path="slide"),
            verbose_name=_("Image"),
            blank=False,
            null=False,
        )
    )

    class Meta:
        verbose_name = _("Slide")
        verbose_name_plural = _("Slides")
        ordering = ['-id']

    def __str__(self):
        return self.title


class Page(TranslatableModel, BaseModel):
    class TypeChoices(models.TextChoices):
        HOME = "home", _("Home Page")
        ABOUT = "about", _("About")
        CONTACT = "contact", _("Contact us")
        PRIVACY = "privacy", _("Privacy Policy")
        TERMS = "terms", _("Terms Page")
        SIGNIN = "signIn", _("Sign In")
        SIGNUP = "signUp", _("Sign Up")

    type = models.CharField(
        max_length=255,
        choices=TypeChoices.choices,
        blank=False,
        null=False,
        unique=True,
        default=TypeChoices.HOME,
    )
    translations = TranslatedFields(
        video=models.FileField(
            upload_to=UploadPath(folder="content", sub_path="videos"),
            blank=True,
            null=True,
            verbose_name=_("Video File"),
            help_text=_("Video file is uploaded to your website.")
        ),
        video_poster=models.ImageField(
            upload_to=UploadPath(folder="content", sub_path="posters"),
            blank=True,
            null=True,
            verbose_name=_("Video Poster"),
            help_text=_("Upload the video poster.")
        )
    )

    class Meta:
        verbose_name = _("Page")
        verbose_name_plural = _("Pages")

    def __str__(self):
        return self.type


class Seo(TranslatableModel):
    page = models.OneToOneField(
        Page, related_name="page_seo", blank=False, null=False,
        verbose_name=_("Belonging Page"), on_delete=models.CASCADE
    )
    translations = TranslatedFields(
        seo_title=models.CharField(
            max_length=255, blank=False, null=False, verbose_name=_("Seo Title"),
            help_text=_("For SEO purposes, ideally between 60-70 characters.")
        ),
        seo_description=models.TextField(
            max_length=160, blank=False, null=False, verbose_name=_("Seo Description"),
            help_text=_("For SEO purposes, ideally between 150-160 characters.")
        ),
        seo_keywords=models.TextField(
            blank=False, null=False, verbose_name=_("Seo Keywords"),
            help_text=_("Comma-separated list of keywords.")
        ),
    )
    seo_canonical = models.URLField(blank=False, null=False, verbose_name=_("Seo Canonical"))
    seo_is_robots_index = models.BooleanField(
        default=False, verbose_name=_("Seo Robot Index"),
        help_text=_("Set to allow search engines to index this page.")
    )
    seo_is_robots_follow = models.BooleanField(
        default=False, verbose_name=_("Seo Robot Follow"),
        help_text=_("Set to allow search engines to follow links on this page.")
    )
    json_ld_data = models.TextField(
        blank=True, null=True, verbose_name="JSON-LD Data",
        help_text="Enter JSON-LD data for structured information (if applicable)."
    )

    class Meta:
        verbose_name = _("SEO")
        verbose_name_plural = _("SEO")

    def __str__(self):
        return str(self.id)
