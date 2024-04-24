from django.contrib import admin
from django.contrib.admin import register
from lib.base_model import CustomModelAdmin
from order.models import Order, Gateway, Transaction, Buy, BuyLine
from django_jalali.admin.filters import JDateFieldListFilter


class BuyLineInline(admin.TabularInline):
    model = BuyLine
    extra = 0
    readonly_fields = ('is_active',)


@register(Order)
class OrderAdmin(CustomModelAdmin):
    list_display = ('id', 'user', 'basket')
    search_fields = ('id',)


@register(Gateway)
class GatewayAdmin(CustomModelAdmin):
    list_display = ('id', 'name')


@register(Transaction)
class TransactionAdmin(CustomModelAdmin):
    list_display = ('id', 'user', 'amount', 'status', 'created_time')
    list_filter = (
        'status',
        ('created_time', JDateFieldListFilter),
    )
    search_fields = ('id',)
    readonly_fields = ('id', 'created_time', 'modified_time', 'ip')


@register(Buy)
class BuyAdmin(CustomModelAdmin):
    list_display = ('id', 'user', 'total_amount', 'created_time')
    list_filter = (
        'refund',
        ('created_time', JDateFieldListFilter),
    )
    search_fields = ('id', 'user')
    inlines = (BuyLineInline,)


@register(BuyLine)
class BuyLineAdmin(CustomModelAdmin):
    list_display = ('id', 'buy', 'product', 'quantity', 'size', 'color')
    search_fields = ('id', 'buy__id')


