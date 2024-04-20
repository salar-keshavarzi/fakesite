from rest_framework.permissions import BasePermission
from account.models import UserModel
from order.models import Order


class FavoriteOwnerPermission(BasePermission):
    def has_permission(self, request, view):
        user = UserModel.objects.filter(id=view.kwargs['user_id']).first()
        if user:
            return request.user == user
        return False


class OrderAddressOwnerPermission(BasePermission):
    def has_permission(self, request, view):
        order = Order.objects.filter(id=view.kwargs['order_id']).first()
        if order:
            return order.user == request.user
        return False
