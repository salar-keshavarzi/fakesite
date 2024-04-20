from django.urls import path
from account.views import test, UserBasket, UserOrder, OrderAddressAPI, ConfirmOrder

urlpatterns = [
    path('test/', test, name="test"),
    path('basket/', UserBasket.as_view(), name="basket"),
    path('order/', UserOrder.as_view(), name="order"),
    path('order/confirm/', ConfirmOrder.as_view(), name="confirm_order"),
    path('order/<int:order_id>/address/update/api/', OrderAddressAPI.as_view(), name="update_order_address"),
]
