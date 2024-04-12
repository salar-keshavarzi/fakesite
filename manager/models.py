from django.db import models
from lib.base_model import BaseModel
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator
from product.models import Product, Category


class StoryCategory(BaseModel):
    title = models.CharField(max_length=48, verbose_name=_('title'))
    image = models.ImageField(upload_to='storyCategory/', verbose_name=_('image'))
    size = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, editable=False,
                               verbose_name=_('size (MB)'))

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        image_size = self.image.size
        size_in_mb = image_size / 1048576
        self.size = round(size_in_mb, 2)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title}-story_category"

    class Meta:
        verbose_name = _('story category')
        verbose_name_plural = _('story categories')


class Story(BaseModel):
    story_category = models.ForeignKey(StoryCategory, on_delete=models.CASCADE, related_name='stories')
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL, related_name='stories')
    image = models.ImageField(upload_to='stories/', verbose_name=_('image'))
    size = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, editable=False,
                               verbose_name=_('size (MB)'))

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        image_size = self.image.size
        size_in_mb = image_size / 1048576
        self.size = round(size_in_mb, 2)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product}-story"

    class Meta:
        verbose_name = _('story')
        verbose_name_plural = _('stories')


class ShippingPrice(BaseModel):
    price = models.PositiveIntegerField(null=False, verbose_name=_('price'))

    def __str__(self):
        return f"{self.price}-shipping"

    class Meta:
        verbose_name = _('shipping price')
        verbose_name_plural = _('shipping prices')


class Collection(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='collections')
    image = models.ImageField(upload_to='collections/', verbose_name=_('image'))
    size = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, editable=False,
                               verbose_name=_('size (MB)'))

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        image_size = self.image.size
        size_in_mb = image_size / 1048576
        self.size = round(size_in_mb, 2)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.category.title}-collection"

    class Meta:
        verbose_name = _('collection')
        verbose_name_plural = _('collections')


class Slider(BaseModel):
    image = models.ImageField(upload_to='collections/', verbose_name=_('image'))
    size = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, editable=False,
                               verbose_name=_('size (MB)'))

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        image_size = self.image.size
        size_in_mb = image_size / 1048576
        self.size = round(size_in_mb, 2)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.id}-slider"

    class Meta:
        verbose_name = _('slider')
        verbose_name_plural = _('sliders')
