from rest_framework import serializers
from account.models import LoginCode, UserModel, BlockUser
import re
from django.utils.translation import gettext_lazy as _
from lib.otp import send_otp
import time

class LoginCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginCode
        fields = ('phone_number',)

    def validate_phone_number(self, attr):
        pattern = r'^09\d{9}$'
        if not re.match(pattern, attr):
            raise serializers.ValidationError(_('phone number is not valid'))
        if BlockUser.objects.filter(phone_number=attr).exists():
            raise serializers.ValidationError(_('The user is blocked'))
        return attr

    def create(self, validated_data):
        phone_number = validated_data['phone_number']
        try:
            user = UserModel.objects.get(username=phone_number)
            new_password = UserModel.objects.make_random_password(length=6, allowed_chars='0123456789')
            user.set_password(new_password)
            user.save()
        except UserModel.DoesNotExist:
            new_password = UserModel.objects.make_random_password(length=6, allowed_chars='0123456789')
            user = UserModel.objects.create_user(username=phone_number, password=new_password)
        user.last_otp = int(time.time())
        user.save()
        send_otp(phone_number, new_password)
        login_code = super().create(validated_data)
        return login_code
