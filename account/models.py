from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.conf import settings
from django.contrib.auth.models import BaseUserManager, User, PermissionsMixin
from django.core.validators import RegexValidator, validate_email
from django_jalali.db.models import jDateTimeField
from account.validators import CustomUsernameValidator, validate_password
from django.utils.translation import gettext_lazy as _

from lib.base_model import BaseModel

PHONE_REGEX = RegexValidator(regex=r"^\d{11}", message='phone number must be 11 digits only!')


class UserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError('phone_number is required!')
        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(username=username, password=password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUserManager(UserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(is_active=True)


class UserModel(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(unique=True, max_length=11, null=False, blank=False, validators=[PHONE_REGEX],
                                verbose_name=_('username'))
    password = models.CharField(max_length=128, validators=[validate_password], verbose_name=_('password'))
    email = models.EmailField(max_length=80, blank=True, null=True, validators=[validate_email],
                              verbose_name=_('email'))
    first_name = models.CharField(max_length=150, blank=True, null=True, verbose_name=_('firstname'))
    last_name = models.CharField(max_length=150, blank=True, null=True, verbose_name=_('lastname'))
    is_active = models.BooleanField(default=True, verbose_name=_('is active'))
    is_staff = models.BooleanField(default=False, verbose_name=_('is staff'))
    registered_time = jDateTimeField(auto_now_add=True, verbose_name=_('registered time'))
    last_login = jDateTimeField(blank=True, null=True, verbose_name=_('last login'))
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name=_('date joined'))

    default_manager = UserManager()
    objects = CustomUserManager()
    # objects = UserManager()
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    # username_validator = CustomUsernameValidator()

    def __str__(self):
        return self.username

    def get_full_name(self):
        full_name = f"{self.first_name if self.first_name else ''} {self.last_name if self.last_name else ''}"
        if len(full_name) > 2:
            return full_name
        return 'کاربر روژی شاپ'

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")


class Address(BaseModel):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='addresses')
    region = models.CharField(max_length=32, blank=True, null=True, verbose_name=_('region'))
    city = models.CharField(max_length=32, blank=True, null=True, verbose_name=_('city'))
    address_detail = models.TextField(null=True, blank=True, verbose_name=_('address detail'))
    fullname = models.CharField(max_length=48, blank=True, null=True, verbose_name=_('receiver fullname'))
    phone_number = models.CharField(max_length=11, blank=True, null=True, verbose_name=_('receiver phone number'))
    zipcode = models.CharField(max_length=24, blank=True, null=True, verbose_name=_('zipcode'))

    def get_address(self):
        return f"{self.region} - {self.city} - {self.address_detail}"

    def get_full_address(self):
        return f"{str(self.user)} : {self.region} - {self.city} - {self.address_detail} - {self.zipcode} [ {self.fullname} - {self.phone_number} ]"

    def __str__(self):
        return f"{self.id}-{str(self.user)}-address"

    class Meta:
        verbose_name = _('address')
        verbose_name_plural = _('addresses')


class BlockUser(BaseModel):
    phone_number = models.CharField(max_length=11, unique=True, verbose_name=_('phone number'))
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='blocks', null=True, blank=True,
                             editable=False)

    def save(self, *args, **kwargs):
        user = UserModel.objects.filter(username=self.phone_number).first()
        if user:
            self.user = user
            super().save(*args, **kwargs)

    def __str__(self):
        return self.phone_number

    class Meta:
        verbose_name = _('blocked user')
        verbose_name_plural = _('blocked users')
