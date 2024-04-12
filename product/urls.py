from django.urls import path
from product.views import ProductListAPI, ProductListView, ProductPageView

urlpatterns = [
    path('list/', ProductListView.as_view(), name='product_list'),
    path('list/api/', ProductListAPI.as_view(), name="product_list_api"),
    path('<str:product_id>/', ProductPageView.as_view(), name="product"),
]
