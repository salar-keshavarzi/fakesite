from django.urls import path
from basket.views import BasketCreateAPI, BasketLineAPI, BasketRetrieveAPI, BasketLineDestroyAPI, UserBasket

urlpatterns = [
    path('', UserBasket.as_view(), name="basket"),
    path('create/', BasketCreateAPI.as_view(), name="create_basket"),
    path('get/<str:basket_id>/', BasketRetrieveAPI.as_view(), name="retrieve_basket"),
    path('line/', BasketLineAPI.as_view(), name="create_basket_line"),
    path('line/delete/<str:basket_line_id>/', BasketLineDestroyAPI.as_view(), name="delete_basket_line"),
]
