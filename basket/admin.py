from django.contrib import admin
from django.contrib.admin import register
from basket.models import Basket, BasketLine

from lib.base_model import CustomModelAdmin


class BasketLineInline(admin.TabularInline):
    model = BasketLine
    extra = 1
    readonly_fields = ('is_active',)


@register(Basket)
class BasketAdmin(CustomModelAdmin):
    list_display = ('id',)
    search_fields = ('id',)
    inlines = (BasketLineInline,)


@register(BasketLine)
class BasketLineAdmin(CustomModelAdmin):
    list_display = ('id', 'basket', 'product', 'quantity')
    search_fields = ('basket__id',)
