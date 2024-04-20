from rest_framework.exceptions import ValidationError
from basket.models import Basket, BasketLine
from rest_framework import serializers

from product.models import Inventory


class BasketLineSerializer(serializers.ModelSerializer):
    basket_id = serializers.CharField(source='basket.id')
    product_id = serializers.CharField(source='product.id')
    size = serializers.CharField(source='inventory.size')
    color = serializers.CharField(source='inventory.color')

    class Meta:
        model = BasketLine
        fields = ('id', 'basket_id', 'product_id', 'size', 'color', 'quantity')
        extra_kwargs = {
            'id': {'read_only': True},
        }

    def validate(self, attrs):
        try:
            inventory = Inventory.objects.get(product_id=attrs['product']['id'],
                                              size__name=attrs['inventory']['size'],
                                              color__name=attrs['inventory']['color'])
            if inventory.quantity >= attrs['quantity']:
                return attrs
            attrs['quantity'] = inventory.quantity
            return attrs
        except Inventory.DoesNotExist:
            raise ValidationError('wrong information')

    def create(self, validated_data):
        try:
            inventory = Inventory.objects.get(product_id=validated_data['product']['id'],
                                              size__name=validated_data['inventory']['size'],
                                              color__name=validated_data['inventory']['color'])
            basket = Basket.objects.get(id=validated_data['basket']['id'])
            basket_line = BasketLine.objects.get_or_create(basket=basket, inventory=inventory,
                                                           product=inventory.product)[0]
            basket_line.quantity = validated_data['quantity']
            basket_line.save()
            return basket_line
        except Inventory.DoesNotExist:
            raise ValidationError('Inventory does not exist')
        except Basket.DoesNotExist:
            raise ValidationError('Basket does not exist')
        except KeyError as e:
            raise ValidationError(f'Missing key in validated data: {e}')


class BasketLineDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = BasketLine
        fields = ('id',)


class BasketSerializer(serializers.ModelSerializer):
    basket_lines = BasketLineSerializer(many=True, required=False)
    total_quantity = serializers.IntegerField(source='get_total_quantity', required=False, read_only=True)
    package_price = serializers.IntegerField(source='get_package_price', required=False, read_only=True)
    total_discount = serializers.IntegerField(source='get_total_discount', required=False, read_only=True)
    total_price = serializers.IntegerField(source='get_total_price', required=False, read_only=True)

    class Meta:
        model = Basket
        fields = ('id', 'basket_lines', 'total_quantity', 'package_price', 'total_discount', 'total_price')
        extra_kwargs = {
            'id': {'read_only': True},
            'basket_lines': {'read_only': True},
            'total_quantity': {'read_only': True},
        }
