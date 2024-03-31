from django.core import validators
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class CustomUsernameValidator(validators.RegexValidator):
    regex = r"^\d{11}"
    message = _('Enter a valid phone number. This value may contain only numbers')
    flags = 0


def validate_password(password):
    if len(password) < 6:
        raise ValidationError(
            _("%(password)s must be more that 5 digit"),
            params={"password": password}, code="invalid"
        )
