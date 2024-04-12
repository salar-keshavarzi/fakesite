from django.contrib import admin
from django.contrib.admin import register
from product.models import Category, Product, Attribute, ProductImage, Size, Color, Inventory, Brand
from lib.base_model import CustomModelAdmin


class ProductInventoryInline(admin.TabularInline):
    model = Inventory
    extra = 1
    readonly_fields = ('is_active',)


class ProductAttributeInline(admin.TabularInline):
    model = Attribute
    extra = 1
    readonly_fields = ('is_active',)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    readonly_fields = ('size', 'is_active')


@register(Brand)
class BrandAdmin(CustomModelAdmin):
    list_display = ('id', 'title')


@register(Category)
class CategoryAdmin(CustomModelAdmin):
    list_display = ('id', 'title', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('id', 'title',)


@register(Product)
class ProductAdmin(CustomModelAdmin):
    list_display = ('id', 'title', 'category', 'first_price', 'discount', 'get_total_quantity', 'is_active')
    list_filter = ('is_active', 'category__title')
    search_fields = ('id', 'title', 'category__title')
    inlines = (ProductInventoryInline, ProductAttributeInline, ProductImageInline)


@register(Attribute)
class AttributeAdmin(CustomModelAdmin):
    list_display = ('id', 'product', 'title', 'value', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('id', 'product__id', 'title')


@register(ProductImage)
class ProductImageAdmin(CustomModelAdmin):
    list_display = ('id', 'product', 'size', 'is_main', 'is_active')
    list_filter = ('is_active', 'is_main')
    search_fields = ('id', 'product__id')

    def get_readonly_fields(self, *args, **kwargs):
        return ['created_time', 'modified_time', 'size']


@register(Color)
class ColorAdmin(CustomModelAdmin):
    list_display = ('id', 'name', 'code', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('id', 'name', 'code')


@register(Size)
class SizeAdmin(CustomModelAdmin):
    list_display = ('id', 'name', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('id', 'name')


@register(Inventory)
class InventoryAdmin(CustomModelAdmin):
    list_display = ('id', 'product', 'size', 'color', 'quantity', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('id', 'product__id')
