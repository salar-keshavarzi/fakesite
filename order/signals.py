from django.db.models.signals import post_save, pre_save, post_init
from django.dispatch import receiver
from lib.sms import send_tracking_code, send_buy_message_handler
from order.models import Buy
from django.conf import settings


@receiver(post_save, sender=Buy)
def change_tracking_code_callback(sender, instance, created, **kwargs):
    if created and settings.SEND_BUY_MESSAGE:
        send_buy_message_handler(instance.user.username, str(instance.id))
    if settings.SEND_TRACKING_CODE and instance.tracking_code and not instance._temp_tracking_code:
        send_tracking_code(instance.user.username, instance.tracking_code)


@receiver(post_init, sender=Buy)
def store_tracking_code_status(sender, instance, **kwargs):
    instance._temp_tracking_code = instance.tracking_code
