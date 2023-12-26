from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
import re


def number_validator(password):
    regex = re.compile("[0-9]")
    if regex.search(password) is None:
        raise ValidationError(
            _("Password must include number"),
            code="include_number",
        )


def letter_validator(password):
    regex = re.compile("[a-zA-Z]")
    if regex.search(password) is None:
        raise ValidationError(
            _("Password must include letter"),
            code="include_letter",
        )


def special_char_validator(password):
    regex = re.compile("[@_!#$%^&*()<>?/\|}{~:]")
    if regex.search(password) is None:
        raise ValidationError(
            _("Password must include special char"),
            code="include_special_char",
        )
