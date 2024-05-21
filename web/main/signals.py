from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
import logging

from settings.models import Notification, PaymentMethod

from .models import Device

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Device)
def create_device_notification(sender, instance, created, **kwargs):
    if created:
        try:
            Notification.objects.create(
                user=instance.user,
                message=_(
                    "Your new phone with SIM number '%(sim_number)s' will be reviewed soon by our support team."
                    ) % {'sim_number': instance.sim_number},
                status=Notification.StatusChoices.INFO,
                priority=Notification.PriorityChoices.LOW,
            )
        except Exception as e:
            logger.error(f"Failed to create notification for new device: {e}")


@receiver(post_save, sender=PaymentMethod)
def create_payment_method_notification(sender, instance, created, **kwargs):
    if created:
        try:
            Notification.objects.create(
                user=instance.user,
                message=_("Your new bank account '%(account_name)s' will be reviewed soon by our support team.") % {
                    'account_name': instance.account_name},
                status=Notification.StatusChoices.INFO,
                priority=Notification.PriorityChoices.LOW,
            )
        except Exception as e:
            logger.error(f"Failed to create notification for new payment method: {e}")
