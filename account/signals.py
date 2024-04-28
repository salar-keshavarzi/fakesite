from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from account.models import LoginCode, UserModel
from lib.sms import send_otp
import time


@receiver(post_save, sender=LoginCode)
def create_login_code_callback(sender, instance, created, **kwargs):
    if created:
        phone_number = instance.phone_number
        try:
            user = UserModel.objects.get(username=phone_number)
            new_password = UserModel.objects.make_random_password(length=6, allowed_chars='0123456789')
            user.otp_try = 5
            user.set_password(new_password)
            user.save()
        except UserModel.DoesNotExist:
            new_password = UserModel.objects.make_random_password(length=6, allowed_chars='0123456789')
            user = UserModel.objects.create_user(username=phone_number, password=new_password)
        user.last_otp = int(time.time())
        user.save()
        print(f"{phone_number} : {new_password}")
        if settings.SEND_OTP_CODE:
            send_otp(phone_number, new_password)
