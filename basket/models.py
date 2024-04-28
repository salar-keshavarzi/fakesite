from django.db import models
from django.db.models import Sum
from django.db.models.functions import Coalesce

# from django.db.models.aggregates import
from lib.base_model import BaseModel
from account.models import UserModel
from django.utils.translation import gettext_lazy as _
import uuid
from product.models import Product, Inventory


class Basket(BaseModel):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)

    def validate_inventories(self):
        flag = True
        basket_lines = self.get_basket_lines()
        for basket_line in basket_lines:
            if basket_line.quantity > basket_line.inventory.quantity:
                flag = False
                if basket_line.inventory.quantity == 0:
                    basket_line.delete()
                else:
                    basket_line.quantity = basket_line.inventory.quantity
                    basket_line.save()
        return flag

    def get_package_price(self):
        total_price = 0
        basket_lines = BasketLine.objects.filter(basket=self)
        for line in basket_lines:
            total_price += (line.product.first_price * line.quantity)
        return total_price

    def get_total_discount(self):
        total_discount = 0
        basket_lines = BasketLine.objects.filter(basket=self)
        for line in basket_lines:
            total_discount += (line.product.discount * line.quantity)
        return total_discount

    def get_total_price(self):
        total_price = 0
        basket_lines = BasketLine.objects.filter(basket=self)
        for line in basket_lines:
            total_price += (line.product.get_final_price() * line.quantity)
        return total_price

    def get_basket_lines(self):
        return BasketLine.objects.select_related('inventory').filter(basket=self).all()

    def get_total_quantity(self):
        return BasketLine.objects.filter(basket=self).aggregate(total_quantity=Coalesce(Sum('quantity'), 0)).get(
            'total_quantity', 0)

    def clear_and_update_inventories(self):
        basket_lines = self.get_basket_lines()
        for basket_line in basket_lines:
            if basket_line.inventory.quantity - basket_line.quantity >= 0:
                basket_line.inventory.quantity -= basket_line.quantity
            else:
                basket_line.inventory.quantity = 0
            basket_line.inventory.save()
            basket_line.delete()
        basket_lines.delete()

    def __str__(self):
        return f"{self.id}-basket"

    class Meta:
        verbose_name = _('basket')
        verbose_name_plural = _('baskets')


class BasketLine(BaseModel):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name='basket_lines')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='basket_lines')
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name='basket_lines')
    quantity = models.PositiveSmallIntegerField(default=1, verbose_name=_('quantity'))

    def __str__(self):
        return f"{self.id}-basket_line"

    class Meta:
        verbose_name = _('basket line')
        verbose_name_plural = _('basket lines')
