from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.db.transaction import atomic
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated

from account.forms import AddressForm
from account.models import Address
from basket.models import Basket, BasketLine
from lib.permissions import OrderAddressOwnerPermission
from lib.utils import get_client_ip
from order.models import Gateway, Order, Transaction, Buy, BuyLine
from lib.zarinpal import send_request, verify
from order.serializers import OrderAddressSerializer


class UserOrder(View):
    form_class = AddressForm

    @method_decorator(login_required)
    def get(self, request):
        form = self.form_class()
        basket_id = request.COOKIES.get('basket_id', None)
        if basket_id:
            try:
                basket = Basket.objects.get(id=basket_id)
                basket_lines = BasketLine.objects.filter(basket=basket).select_related('inventory', 'product',
                                                                                       'product__seller',
                                                                                       'inventory__color',
                                                                                       'inventory__size').all()
                order = Order.objects.get(basket_id=basket_id)
            except Basket.DoesNotExist:
                raise Http404
            except Order.DoesNotExist:
                order = Order.objects.create(basket=basket, user=request.user)
            addresses = Address.objects.filter(user=request.user).all()
            shipping_price = order.get_shipping_price()
            order_address = Address.objects.filter(user=request.user).first()
            if order_address and not order.address:
                order.address = order_address
                order.save()
            if basket.get_total_price() == 0:
                return redirect('basket')
            return render(request, template_name='order/order.html',
                          context={'order': order, 'basket': basket, 'basket_lines': basket_lines,
                                   'addresses': addresses, 'shipping_price': shipping_price, 'form': form})
        return render(request, template_name='order/order.html', context={'form': form})

    @method_decorator(login_required)
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
        return redirect('order')


class OrderAddressAPI(UpdateAPIView):
    permission_classes = [IsAuthenticated, OrderAddressOwnerPermission]
    serializer_class = OrderAddressSerializer
    lookup_url_kwarg = 'order_id'
    queryset = Order.objects.all()

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)


class ConfirmOrder(View):
    @method_decorator(login_required)
    def get(self, request):
        basket_id = request.COOKIES.get('basket_id', None)
        if basket_id:
            try:
                basket = Basket.objects.get(id=basket_id)
                basket_lines = BasketLine.objects.filter(basket=basket).select_related('inventory', 'product',
                                                                                       'product__seller',
                                                                                       'inventory__color',
                                                                                       'inventory__size').all()
                order = Order.objects.get(basket_id=basket_id)
            except Basket.DoesNotExist:
                raise Http404
            except Order.DoesNotExist:
                return redirect('order')
            shipping_price = order.get_shipping_price()
            address = order.address
            if basket.get_total_price() == 0:
                return redirect('basket')
            return render(request, template_name='order/confirm_order.html',
                          context={'order': order, 'basket': basket, 'basket_lines': basket_lines, 'address': address,
                                   'shipping_price': shipping_price})
        return redirect('order')


# class BuyView(View):
#     @method_decorator(login_required)
#     def get(self, request, order_id):
#         try:
#             order = Order.objects.get(id=order_id)
#             gateway = Gateway.objects.first()
#         except Order.DoesNotExist:
#             raise Http404
#         if not gateway:
#             raise Http404
#         order_amount = order.get_final_price()
#         data = gateway.zpal_send_request(amount=order_amount, phone_number=request.user.username, order_id=order_id)
#         if data['status']:
#             url = data['url']
#             authority = data['authority']
#             return redirect(url)
#         return redirect('confirm_order')
#
#
# class BuyVerifyView(View):
#     @method_decorator(login_required)
#     def get(self, request):
#         authority = request.GET.get('Authority', None)
#         status = request.GET.get('Status', 'NOK')
#         if authority and status != 'NOK':
#             pass
#         return render(request, template_name="order/confirm_buy.html", context={'status': None})

class BuyView(View):
    @method_decorator(login_required)
    def get(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            raise Http404
        order_amount = order.get_final_price()
        data = send_request(amount=order_amount)
        if data['status']:
            url = data['url']
            authority = data['authority']
            Transaction.objects.create(
                user=request.user,
                order=order,
                amount=order_amount,
                authority=authority,
                phone_number=request.user.username,
                ip=get_client_ip(request)
            )
            return redirect(url)
        return redirect('confirm_order')


class BuyVerifyView(View):
    @method_decorator(login_required)
    def get(self, request):
        authority = request.GET.get('Authority')
        status = request.GET.get('Status', 'NOK')
        if authority and status != 'NOK':
            transaction = (Transaction.objects.filter(user=request.user, authority=authority).first()
                           .select_related('order', 'order__address', 'order__basket'))
            if not transaction:
                raise Http404
            if transaction.amount == transaction.order.get_final_price():
                data = verify(transaction.amount, authority)
                if data['status']:
                    ref_id = data['ref_id']
                    with atomic():
                        transaction.status = 2
                        transaction.ref_id = ref_id
                        transaction.save()
                        buy = Buy.objects.create(
                            user=request.user,
                            transaction=transaction,
                            full_name=transaction.order.address.fullname,
                            phone_number=transaction.order.address.phone_number,
                            address=transaction.order.address.get_address(),
                            zipcode=transaction.order.address.zipcode,
                            package_price=transaction.order.basket.get_package_price(),
                            shipping_price=transaction.order.get_shipping_price(),
                            discount_amount=transaction.order.basket.get_total_discount(),
                            total_amount=transaction.amount,
                        )
                        for basket_line in transaction.order.basket.get_basket_lines():
                            BuyLine.objects.create(
                                buy=buy,
                                product=basket_line.product,
                                quantity=basket_line.quantity,
                                size=basket_line.inventory.size,
                                color=basket_line.inventory.color,
                                product_price=basket_line.product.get_final_price()
                            )
                    basket_id = request.COOKIES.get('basket_id')
                    if basket_id:
                        try:
                            Basket.objects.get(id=basket_id).clear()
                        except Basket.DoesNotExist:
                            pass
                    return render(request, template_name="order/confirm_buy.html",
                                  context={'status': transaction.status})
            else:
                if transaction.status == 3:
                    transaction.status = 1
                    transaction.save()
                return render(request, template_name="order/confirm_buy.html", context={'status': 1})
        return render(request, template_name="order/confirm_buy.html", context={'status': 3})
