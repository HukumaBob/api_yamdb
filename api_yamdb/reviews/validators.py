import datetime
from django.core.exceptions import ValidationError


def validate_username(value):
    if value == 'me':
        raise ValidationError(
            ('Users name can`t be <me>.'),
            params={'value': value},
        )


def validate_year(year):
    this_year = datetime.date.today().year
    if year > this_year:
        raise ValidationError(
            'It`s not possible now'
        )
