from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from order.models import Order


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
