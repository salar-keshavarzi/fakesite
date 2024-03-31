from django.contrib import admin
from django.contrib.admin import register
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from account.models import UserModel, BlockUser, Address
from lib.base_model import CustomModelAdmin


@register(UserModel)
class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'registered_time')}),
    )
    readonly_fields = ('registered_time', 'last_login')

    # def get_fieldsets(self, request, obj=None):
    #     # require for creation form
    #     if not obj:
    #         return self.add_fieldsets
    #     if request.user.is_superuser:
    #         self.readonly_fields = ('registered_time', 'last_login')
    #     else:
    #         self.readonly_fields = ('registered_time', 'is_staff', 'is_superuser', 'user_permissions', 'last_login')
    #     return self.fieldsets

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return ('registered_time', 'last_login')
        else:
            return ('registered_time', 'is_staff', 'is_superuser', 'user_permissions', 'last_login')

    def get_queryset(self, request):
        qs = super(CustomUserAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(is_superuser=False)


@register(Address)
class AddressAdmin(CustomModelAdmin):
    list_display = ('id', 'user', 'region', 'city', 'zipcode')
    list_filter = ('is_active',)
    search_fields = ('id', 'user__id', 'user__username')


@register(BlockUser)
class BlockUserAdmin(CustomModelAdmin):
    list_display = ('id', 'phone_number', 'user', 'created_time')
    list_filter = ('is_active',)
    search_fields = ('id', 'phone_number', 'user__id')
