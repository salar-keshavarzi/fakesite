from product.models import Product, Inventory, ProductImage
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    image = serializers.CharField(source='get_image_url')
    category = serializers.CharField(source='category.title')
    final_price = serializers.IntegerField(source='get_final_price')

    class Meta:
        model = Product
        fields = ('id', 'category', 'title', 'first_price', 'final_price', 'image')


class InventorySerializer(serializers.ModelSerializer):
    product_id = serializers.CharField(source='product.id')

    class Meta:
        model = Inventory
        fields = ('id', 'product_id', 'size', 'color', 'quantity')
