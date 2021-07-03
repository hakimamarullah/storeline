from django.core.exceptions import ValidationError


def validatePhone(value):
    try:
        int(value)
    except:
        raise ValidationError("Phone number is invalid")
