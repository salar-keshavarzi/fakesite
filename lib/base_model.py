from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django_jalali.db.models import jDateTimeField
from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from PIL import Image


class CustomManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(is_active=True)




class BaseModel(models.Model):
    default_manager = models.Manager()
    objects = CustomManager()
    is_active = models.BooleanField(default=True, verbose_name=_("active"))
    created_time = jDateTimeField(auto_now_add=True, verbose_name=_("created time"))
    modified_time = jDateTimeField(auto_now=True, verbose_name=_("modified time"))

    class Meta:
        abstract = True


class CustomModelAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'created_time', 'modified_time')
    ordering = ('-created_time',)


class CustomImageField(models.ImageField):
    def __init__(self, *args, **kwargs):
        self.process_function = kwargs.pop('process_function', None)
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        value = super().pre_save(model_instance, add)
        if value and self.process_function:
            img = Image.open(value)
            processed_img = self.process_function(img)
            processed_img.save(value.path)
        return value
