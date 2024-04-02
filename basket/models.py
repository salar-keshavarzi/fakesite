from django.db import models
# from django.db.models.aggregates import
from lib.base_model import BaseModel
from account.models import UserModel
from django.utils.translation import gettext_lazy as _

from product.models import Product, Inventory


class Basket(BaseModel):

    def get_total_price(self):
        total_price = 0
        basket_lines = BasketLine.objects.filter(basket=self)
        for line in basket_lines:
            total_price += (line.product.get_final_price() * line.quantity)

    def get_basket_lines(self):
        return BasketLine.objects.filter(basket=self)

    def __str__(self):
        return f"{self.id}-basket"

    class Meta:
        verbose_name = _('basket')
        verbose_name_plural = _('baskets')


class BasketLine(BaseModel):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name='basket_lines')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='basket_lines')
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name='basket_lines')
    quantity = models.PositiveSmallIntegerField(default=1, verbose_name=_('quantity'))

    def __str__(self):
        return f"{self.id}-basket_line"

    class Meta:
        verbose_name = _('basket line')
        verbose_name_plural = _('basket lines')
