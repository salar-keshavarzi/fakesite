import uuid
from django.db import models
from django.db.models import F, ExpressionWrapper, IntegerField, Sum, BooleanField, Case, When
from lib.base_model import BaseModel
from django.utils.translation import gettext_lazy as _
from lib.utils import attach_logo
from lib.base_model import CustomImageField


class Seller(BaseModel):
    name = models.CharField(max_length=48, verbose_name=_('name'))
    phone_number = models.CharField(max_length=24, null=True, blank=True, verbose_name=_('phone number'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('seller')
        verbose_name_plural = _('sellers')


class Category(BaseModel):
    title = models.CharField(max_length=48, unique=True, verbose_name=_('category title'))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')


class Brand(BaseModel):
    title = models.CharField(max_length=48, unique=True, verbose_name=_('brand title'))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('brand')
        verbose_name_plural = _('brands')


class ProductManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        # return qs.prefetch_related('inventories').annotate(is_available=Sum('inventories__quantity', output_field=BooleanField())).order_by('-is_available')
        return qs.prefetch_related('inventories').annotate(
            total_quantity=Sum('inventories__quantity', output_field=IntegerField())).annotate(
            is_available=Case(When(total_quantity__gt=0, then=True), default=False,
                              output_field=BooleanField())).order_by('-is_available')


class Product(BaseModel):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL, related_name='products')
    title = models.CharField(max_length=64, blank=True, null=True, verbose_name=_('product title'))
    first_price = models.PositiveIntegerField(default=0, verbose_name=_('first price'))
    discount = models.PositiveIntegerField(default=0, verbose_name=_('discount'))
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name='brands')
    visit_count = models.PositiveIntegerField(default=0, verbose_name=_('visit count'))
    buy_count = models.PositiveIntegerField(default=0, verbose_name=_('buy count'))
    seller = models.ForeignKey(Seller, null=True, blank=True, on_delete=models.SET_NULL,
                               related_name='products', verbose_name=_('seller'))
    objects = ProductManager()

    @classmethod
    def search(cls, product_title):
        return cls.objects.filter(title__contains=product_title)[:10]

    @classmethod
    def get_recent_adds(cls):
        return cls.objects.annotate(discount_percent=ExpressionWrapper(100 * F('discount') / F('first_price'),
                                                                       output_field=IntegerField())).order_by(
            '-is_available', '-created_time')[:20]

    @classmethod
    def get_offers(cls):
        return cls.objects.annotate(discount_percent=ExpressionWrapper(100 * F('discount') / F('first_price'),
                                                                       output_field=IntegerField())).order_by(
            '-is_available', '-discount_percent')[:12]

    def get_final_price(self):
        if self.inventories.filter(quantity__gt=0).exists():
            if self.discount:
                return self.first_price - self.discount
            return self.first_price
        return 0

    def is_discounted(self):
        if self.discount:
            return True
        return False

    def get_image(self):
        main_image = ProductImage.objects.filter(product=self).order_by('-is_main').first()
        if main_image:
            return main_image.image
        return None

    def get_image_url(self):
        image = self.get_image()
        if image:
            return image.url
        return None

    def __str__(self):
        return self.title

    def get_total_quantity(self):
        result = Inventory.objects.filter(product=self).aggregate(total_quantity=Sum('quantity'))
        return result.get('total_quantity', 0)

    def get_attributes(self):
        return Attribute.objects.filter(product=self)

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')


class Attribute(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='attributes')
    title = models.CharField(max_length=48, verbose_name=_('attribute title'))
    value = models.CharField(max_length=48, verbose_name=_('value'))

    def __str__(self):
        return f"{str(self.product)}-{self.title}:{self.value}"

    class Meta:
        verbose_name = _('attribute')
        verbose_name_plural = _('attributes')


class ProductImage(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    # image = CustomImageField(upload_to='products/', null=True, process_function=attach_logo, verbose_name=_('image'))
    image = models.ImageField(upload_to='products/', null=True, verbose_name=_('image'))
    size = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, editable=False,
                               verbose_name=_('size (MB)'))
    is_main = models.BooleanField(default=False, verbose_name=_('is main image'))

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
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
    name = models.CharField(max_length=16, verbose_name=_('color name'), unique=True)
    code = models.CharField(max_length=9, default='#fff', verbose_name=_('color code (hex)'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('color')
        verbose_name_plural = _('colors')


class Size(BaseModel):
    name = models.CharField(max_length=16, verbose_name=_('size'), unique=True)

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
