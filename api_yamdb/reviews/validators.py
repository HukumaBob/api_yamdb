import datetime

from django.core.exceptions import ValidationError


def validate_year(year):
    this_year = datetime.date.today().year
    if year > this_year:
        raise ValidationError(
            'Год выхода произведения не должен быть в будущем'
        )