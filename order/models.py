from django.db import models
from django.utils.translation import gettext_lazy as _
from account.models import Address, UserModel
from basket.models import Basket
from lib.base_model import BaseModel
import uuid
from product.models import Product, Size, Color


class Order(BaseModel):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='order')
    basket = models.ForeignKey(Basket, null=True, blank=True, on_delete=models.SET_NULL, related_name='orders')
    address = models.ForeignKey(Address, null=True, blank=True, on_delete=models.CASCADE, related_name='orders')

    def __str__(self):
        return f"{self.user}-order"

    class Meta:
        verbose_name = _('order')
        verbose_name_plural = _('orders')


class Gateway(BaseModel):
    name = models.CharField(max_length=48, verbose_name=_('name'))
    merchant_id = models.CharField(max_length=48, verbose_name=_('merchant id'))
    request_url = models.URLField(max_length=200, verbose_name=_('request url'))
    verify_url = models.URLField(max_length=200, verbose_name=_('verify url'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('gateway')
        verbose_name_plural = _('gateways')


class Transaction(BaseModel):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = models.ForeignKey(UserModel, on_delete=models.PROTECT, related_name='transactions')
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='transactions')
    amount = models.PositiveIntegerField(verbose_name=_('amount'))
    gateway = models.ForeignKey(Gateway, on_delete=models.PROTECT, related_name='transactions')
    authority = models.CharField(max_length=48, null=True, blank=True, verbose_name=_('authority code'))
    ref_id = models.CharField(max_length=48, null=True, blank=True, verbose_name=_('transaction number'))
    log = models.TextField(null=True, blank=True, verbose_name=_('log'))
    card_pan = models.CharField(max_length=24, blank=True, null=True)
    phone_number = models.CharField(max_length=11, blank=True, null=True, verbose_name=_('phone number'))
    is_paid = models.BooleanField(default=False, editable=False, verbose_name=_('is paid'))
    ip = models.CharField(max_length=16, editable=False, null=True, blank=True, verbose_name=_('ip'))

    def __str__(self):
        return f"{self.id}-transaction"

    class Meta:
        verbose_name = _('transaction')
        verbose_name_plural = _('transactions')


class Buy(BaseModel):
    user = models.ForeignKey(UserModel, on_delete=models.PROTECT, related_name='buys')
    transaction = models.ForeignKey(Transaction, on_delete=models.PROTECT, related_name='buys')
    gateway = models.ForeignKey(Gateway, on_delete=models.SET_NULL, null=True, blank=True, related_name='buys')
    full_name = models.CharField(max_length=64, verbose_name=_('fullname'))
    phone_number = models.CharField(max_length=11, verbose_name=_('phone number'))
    address = models.TextField(verbose_name=_('address'))
    zipcode = models.CharField(max_length=16, verbose_name=_('zipcode'))
    package_price = models.PositiveIntegerField(verbose_name=_('package price'))
    shipping_price = models.PositiveIntegerField(verbose_name=_('shipping price'))
    discount_amount = models.PositiveIntegerField(verbose_name=_('discount amount'))
    total_amount = models.PositiveIntegerField(verbose_name=_('total amount'))
    tracking_code = models.CharField(max_length=64, verbose_name=_('tracking code'))

    def __str__(self):
        return f"{self.id}-buy"

    class Meta:
        verbose_name = _('buy')
        verbose_name_plural = _('buys')


class BuyLine(BaseModel):
    buy = models.ForeignKey(Buy, on_delete=models.CASCADE, related_name='buy_lines')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='buy_lines')
    quantity = models.PositiveSmallIntegerField(default=1, verbose_name=_('quantity'))
    size = models.ForeignKey(Size, null=True, on_delete=models.SET_NULL, related_name='buy_lines')
    color = models.ForeignKey(Color, null=True, on_delete=models.SET_NULL, related_name='buy_lines')
    product_price = models.PositiveIntegerField(verbose_name=_('product price'))

    def get_total_price(self):
        return self.product_price * self.quantity

    def __str__(self):
        return f"{self.id}-buyLine"

    class Meta:
        verbose_name = _('buy line')
        verbose_name_plural = _('buy lines')


class Refund(BaseModel):
    buy = models.ForeignKey(Buy, on_delete=models.PROTECT, related_name='refunds')

    def __str__(self):
        return f"{self.id}-refund"

    class Meta:
        verbose_name = _('refund')
        verbose_name_plural = _('refunds')
