from django.http import Http404
from django.shortcuts import render
from django.views import View
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveAPIView, DestroyAPIView

from basket.models import Basket, BasketLine
from product.models import Product
from basket.serializers import BasketSerializer, BasketLineSerializer


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


# class BasketCreateAPI(CreateAPIView):
class BasketCreateAPI(CreateAPIView):
    serializer_class = BasketSerializer
    queryset = Basket.objects.all()


class BasketRetrieveAPI(RetrieveAPIView):
    serializer_class = BasketSerializer
    queryset = Basket.objects.all()
    lookup_url_kwarg = 'basket_id'


class BasketLineAPI(CreateAPIView):
    serializer_class = BasketLineSerializer
    queryset = BasketLine.objects.all()


class BasketLineDestroyAPI(DestroyAPIView):
    queryset = BasketLine.objects.all()
    lookup_url_kwarg = 'basket_line_id'
