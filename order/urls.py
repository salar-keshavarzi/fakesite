from django.urls import path
from order.views import BuyView, BuyVerifyView, ConfirmOrder, UserOrder, OrderAddressAPI

urlpatterns = [
    path('', UserOrder.as_view(), name="order"),
    path('confirm/', ConfirmOrder.as_view(), name="confirm_order"),
    path('<int:order_id>/address/update/api/', OrderAddressAPI.as_view(), name="update_order_address"),
    path('<int:order_id>/buy/', BuyView.as_view(), name='buy'),
    path('buy/verify/', BuyVerifyView.as_view(), name='verify_buy'),
]
