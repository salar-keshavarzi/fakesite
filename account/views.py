from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, reverse, redirect
from django.utils.decorators import method_decorator
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated

from account.models import UserModel, LoginCode, Address
from lib.permissions import OrderAddressOwnerPermission
from manager.models import ShippingPrice
from product.models import Product, ProductImage
from django.views import View
from account.serializers import LoginCodeSerializer, OrderAddressSerializer
from django.contrib.auth import authenticate, logout, login
import time
from lib.throttle import LoginThrottle1, LoginThrottle2
from basket.models import Basket, BasketLine
from order.models import Order
from account.froms import AddressForm


@login_required
def test(request):
    images = ProductImage.objects.all()
    return render(request, template_name='test.html', context={'images': images})


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
        return render(request, template_name='auth/login.html', context={'step': 1})

    def post(self, request):
        phone_number = request.POST.get('phone-number-hidden', None)
        otp_code = request.POST.get('otp-hidden', None)
        if phone_number and len(phone_number.strip()) == 11 and otp_code:
            username = phone_number.strip()
            otp = otp_code.strip()
            user = authenticate(username=username, password=otp)
            if user:
                login(request, user)
                if request.GET.get('next'):
                    return redirect(request.GET.get('next'))
                return redirect('home')
            else:
                user = UserModel.objects.filter(username=phone_number).first()
                if user:
                    temp_time = 120 - int(time.time() - user.last_otp)
                    remaining_time = temp_time if temp_time > 0 else 120
                    return render(request, template_name='auth/login.html',
                                  context={'step': 2, 'phone_number': phone_number, 'remaining_time': remaining_time})
        return render(request, template_name='auth/login.html', context={'step': 1})


class LoginAPI(CreateAPIView):
    queryset = LoginCode.objects.all()
    serializer_class = LoginCodeSerializer
    throttle_classes = [LoginThrottle1, LoginThrottle2]


class LogOutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')


class UserBasket(View):
    def get(self, request):
        basket_id = request.COOKIES.get('basket_id', None)
        if basket_id:
            try:
                basket = Basket.objects.get(id=basket_id)
                basket_lines = BasketLine.objects.filter(basket=basket).select_related('inventory', 'product',
                                                                                       'product__seller',
                                                                                       'inventory__color',
                                                                                       'inventory__size').all()
            except Basket.DoesNotExist:
                raise Http404
            return render(request, template_name='basket/basket.html',
                          context={'basket': basket, 'basket_lines': basket_lines})
        return render(request, template_name='basket/basket.html')


class UserOrder(View):

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
                                   'addresses': addresses, 'shipping_price': shipping_price})
        return render(request, template_name='order/order.html', )

    @method_decorator(login_required)
    def post(self, request):
        user = request.user
        region = request.POST.get('region', None)
        city = request.POST.get('city', None)
        address_detail = request.POST.get('address', None)
        fullname = request.POST.get('fullname', None)
        phone_number = request.POST.get('phone-number', None)
        zipcode = request.POST.get('zipcode', None)
        if region and city and address_detail and fullname and phone_number and zipcode:
            try:
                Address.objects.create(
                    user=user,
                    region=region,
                    city=city,
                    address_detail=address_detail,
                    fullname=fullname,
                    phone_number=phone_number,
                    zipcode=zipcode
                )
            except:
                return redirect('order')
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
