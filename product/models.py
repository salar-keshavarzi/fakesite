from PIL import Image
from django.db import models
from django.db.models import F

from lib.base_model import BaseModel
from django.utils.translation import gettext_lazy as _


class Category(BaseModel):
    title = models.CharField(max_length=48, blank=True, null=True, verbose_name=_('category title'))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')


class Product(BaseModel):
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL, related_name='products')
    title = models.CharField(max_length=64, blank=True, null=True, verbose_name=_('product title'))
    first_price = models.PositiveIntegerField(default=0, verbose_name=_('first price'))
    discount = models.PositiveIntegerField(default=0, verbose_name=_('discount'))

    @classmethod
    def search(cls, product_title):
        cls.objects.filter(title__contains=product_title)

    @classmethod
    def get_recent_adds(cls):
        return cls.objects.order_by('-created_time')[:20]

    @classmethod
    def get_offers(cls):
        return cls.objects.annotate(discount_percent=F('discount') / F('first_price') * 100).order_by(
            '-discount_percent')[:12]

    def get_final_price(self):
        if self.inventories.filter(quantity__gt=0).exists():
            if self.discount:
                return self.first_price - self.discount
            return self.first_price
        return 0

    def is_discounted(self):
        if self.discount > 0:
            return True
        return None

    def get_image(self):
        main_image = self.images.filter(is_main=True).first()
        if main_image:
            return main_image
        else:
            return self.images.first()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')


class Attribute(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='products')
    title = models.CharField(max_length=48, verbose_name=_('attribute title'))
    value = models.CharField(max_length=48, verbose_name=_('value'))

    def __str__(self):
        return f"{str(self.product)}-{self.title}:{self.value}"

    class Meta:
        verbose_name = _('attribute')
        verbose_name_plural = _('attributes')


class ProductImage(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name=_('image'))
    size = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, verbose_name=_('size (MB)'))
    is_main = models.BooleanField(default=False, verbose_name=_('is main image'))

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # image = Image.open(self.image.path)
        image_size = self.image.size
        size_in_mb = image_size / 1048576
        self.size = round(size_in_mb, 2)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{str(self.product)} - image"

    class Meta:
        verbose_name = _('product image')
        verbose_name_plural = _('product images')


class Color(BaseModel):
    name = models.CharField(max_length=16, verbose_name=_('color name'))
    code = models.CharField(max_length=9, default='#fff', verbose_name=_('color code (hex)'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('color')
        verbose_name_plural = _('colors')


class Size(BaseModel):
    name = models.CharField(max_length=16, verbose_name=_('size'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('size')
        verbose_name_plural = _('sizes')


class Inventory(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='inventories')
    size = models.ForeignKey(Size, on_delete=models.PROTECT, related_name='inventories')
    color = models.ForeignKey(Color, on_delete=models.PROTECT, related_name='inventories')
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name=_('quantity'))

    def __str__(self):
        return f"{str(self.product)}-{self.size}-{self.color}-{self.quantity}"

    class Meta:
        verbose_name = _('inventory')
        verbose_name_plural = _('inventories')
