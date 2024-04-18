from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveAPIView, DestroyAPIView

from basket.models import Basket, BasketLine
from product.models import Product
from basket.serializers import BasketSerializer, BasketLineSerializer


# class BasketCreateAPI(CreateAPIView):
class BasketCreateAPI(ListCreateAPIView):
    serializer_class = BasketSerializer
    queryset = Basket.objects.all()


class BasketRetrieveAPI(RetrieveAPIView):
    serializer_class = BasketSerializer
    queryset = Basket.objects.all()
    lookup_url_kwarg = 'basket_id'


class BasketLineAPI(ListCreateAPIView):
    serializer_class = BasketLineSerializer
    queryset = BasketLine.objects.all()


class BasketLineDestroyAPI(DestroyAPIView):
    queryset = BasketLine.objects.all()
    lookup_url_kwarg = 'basket_line_id'
