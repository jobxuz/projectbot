import re
from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError


def validate_card_expire_date(value: str) -> None:
    """
    Validates that the given value is in MM/YY format.

    Args:
        value (str): The date string to validate.

    Raises:
        ValidationError: If the value does not match the MM/YY format.
    """
    pattern = re.compile(r'^(0[1-9]|1[0-2])\/\d{2}$')
    if not pattern.match(value):
        raise ValidationError(_('Invalid format. Please use MM/YY format.'))
