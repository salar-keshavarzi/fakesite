import json

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from account.models import Address, UserModel
from basket.models import Basket
from lib.base_model import BaseModel
import uuid
from product.models import Product, Size, Color
from manager.models import ShippingPrice
import requests


class Order(BaseModel):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='order')
    basket = models.ForeignKey(Basket, null=True, blank=True, on_delete=models.SET_NULL, related_name='orders')
    address = models.ForeignKey(Address, null=True, blank=True, on_delete=models.CASCADE, related_name='orders')

    def get_shipping_price(self):
        if self.basket.get_total_price() >= 500000:
            return 0
        shipping_price = ShippingPrice.objects.first()
        if shipping_price:
            return shipping_price.price
        return 30000

    def get_final_price(self):
        return self.basket.get_total_price() + self.get_shipping_price()

    def __str__(self):
        return f"{self.user}-order"

    class Meta:
        verbose_name = _('order')
        verbose_name_plural = _('orders')


class Gateway(BaseModel):
    name = models.CharField(max_length=48, verbose_name=_('name'))
    merchant_id = models.CharField(max_length=48, verbose_name=_('merchant id'))
    request_url = models.URLField(max_length=200, verbose_name=_('request url'))
    start_pay_url = models.URLField(max_length=200, verbose_name=_('start pay url'))
    verify_url = models.URLField(max_length=200, verbose_name=_('verify url'))

    def zpal_send_request(self, amount, phone_number, order_id):
        data = {
            "merchant_id": self.merchant_id,
            "amount": amount * 10,
            "callback_url": settings.DOMAIN + reverse('confirm_buy'),
            "description": "خرید از روژی شاپ",
            "metadata": {
                "mobile": phone_number,
                "order_id": order_id,
            }
        }
        raw_data = json.dumps(data)
        headers = {'content-type': 'application/json', 'content-length': str(len(raw_data))}
        try:
            response = requests.post(url=self.request_url, data=data, headers=headers, timeout=10)
            if response.status_code == 200:
                response = response.json()
                if response['data']['code'] == 100:
                    return {'status': True, 'url': self.start_pay_url + str(response['data']['authority']),
                            'authority': response['data']['authority']}
                else:
                    return {'status': False, 'code': str(response['data']['code'])}
            return {'status': False, 'code': 'error'}
        except requests.exceptions.Timeout:
            return {'status': False, 'code': 'timeout'}
        except requests.exceptions.ConnectionError:
            return {'status': False, 'code': 'connection error'}

    def zpal_verify_request(self, amount, authority):
        data = {
            "merchant_id": self.merchant_id,
            "amount": amount * 10,
            "authority": authority,
        }
        raw_data = json.dumps(data)
        headers = {'content-type': 'application/json', 'content-length': str(len(raw_data))}
        response = requests.post(self.verify_url, data=data, headers=headers)
        if response.status_code == 200:
            response = response.json()
            if response['data']['code'] == 100:
                return {'status': True, 'ref_id': response['data']['refID'], 'card_pan': response['data']['card_pan']}
            else:
                return {'status': False, 'code': str(response['data']['status'])}
        return {'status': False, 'code': 'error'}

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('gateway')
        verbose_name_plural = _('gateways')


class Transaction(BaseModel):
    NO_INFO = 1
    IS_PAID = 2
    FAILED = 3
    STATUS = [
        (NO_INFO, 'همراه با خطا'),
        (IS_PAID, 'موفق'),
        (FAILED, 'ناموفق'),
    ]
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = models.ForeignKey(UserModel, on_delete=models.PROTECT, related_name='transactions')
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='transactions')
    amount = models.PositiveIntegerField(verbose_name=_('amount'))
    gateway = models.ForeignKey(Gateway, null=True, blank=True, on_delete=models.PROTECT, related_name='transactions')
    authority = models.CharField(max_length=48, null=True, blank=True, verbose_name=_('authority code'))
    ref_id = models.CharField(max_length=48, null=True, blank=True, verbose_name=_('transaction number'))
    log = models.TextField(null=True, blank=True, verbose_name=_('log'))
    card_pan = models.CharField(max_length=24, blank=True, null=True)
    phone_number = models.CharField(max_length=11, blank=True, null=True, verbose_name=_('phone number'))
    status = models.PositiveSmallIntegerField(choices=STATUS, default=FAILED, verbose_name=_('status'))
    ip = models.CharField(max_length=48, editable=False, null=True, blank=True, verbose_name=_('ip'))

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
    tracking_code = models.CharField(max_length=64, null=True, blank=True, verbose_name=_('tracking code'))
    refund = models.BooleanField(default=False, verbose_name=_('refund'))

    @classmethod
    def get_by_user(cls, user):
        return ((cls.objects.filter(user=user).select_related('transaction')
                .prefetch_related('buy_lines', 'buy_lines__product', 'buy_lines__color', 'buy_lines__size'))
                .order_by('-created_time'))

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
