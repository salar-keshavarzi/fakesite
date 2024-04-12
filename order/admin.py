from django.contrib import admin
from django.contrib.admin import register
from lib.base_model import CustomModelAdmin
from order.models import Order, Gateway, Transaction, Buy, BuyLine, Refund
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
    list_display = ('id', 'user', 'amount', 'created_time')
    list_filter = (
        ('created_time', JDateFieldListFilter),
    )
    search_fields = ('id',)


@register(Buy)
class BuyAdmin(CustomModelAdmin):
    list_display = ('id', 'user', 'total_amount', 'created_time')
    list_filter = (
        ('created_time', JDateFieldListFilter),
    )
    search_fields = ('id', 'user')
    inlines = (BuyLineInline,)


@register(BuyLine)
class BuyLineAdmin(CustomModelAdmin):
    list_display = ('id', 'buy', 'product', 'quantity', 'size', 'color')
    search_fields = ('id', 'buy__id')


@register(Refund)
class RefundAdmin(CustomModelAdmin):
    list_display = ('id', 'buy', 'created_time')
    list_filter = (
        ('created_time', JDateFieldListFilter),
    )
    search_fields = ('id', 'buy__id')
