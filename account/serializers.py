from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from account.models import LoginCode, UserModel, BlockUser, Address
import re
from django.utils.translation import gettext_lazy as _
from lib.otp import send_otp
import time

from order.models import Order


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


class OrderAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'address')
        extra_kwargs = {
            'id': {'read_only': True, 'required': False}
        }

    def validate(self, attrs):
        address = attrs.get('address')
        if self.instance.user == address.user:
            return attrs
        raise ValidationError('address does not belong to this user')
