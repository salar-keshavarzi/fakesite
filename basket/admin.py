from django.contrib import admin
from django.contrib.admin import register
from basket.models import Basket, BasketLine

from lib.base_model import CustomModelAdmin


class BasketLineInline(admin.TabularInline):
    model = BasketLine
    extra = 1


@register(Basket)
class BasketAdmin(CustomModelAdmin):
    list_display = ('id', 'user')
    search_fields = ('user__id', 'user__username')
    inlines = ()


@register(BasketLine)
class BasketLineAdmin(CustomModelAdmin):
    list_display = ('id', 'basket', 'product', 'quantity')
    search_fields = ('user__id', 'user__username')
