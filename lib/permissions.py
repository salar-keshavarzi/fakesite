from rest_framework.permissions import BasePermission
from account.models import UserModel


class FavoriteOwnerPermission(BasePermission):
    def has_permission(self, request, view):
        user = UserModel.objects.filter(id=view.kwargs['user_id']).first()
        if user:
            return request.user == user
        return False
