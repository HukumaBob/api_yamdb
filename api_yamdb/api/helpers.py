import uuid

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from reviews.models import User


def confirmation_code_to_email(username):
    user = get_object_or_404(User, username=username)
    confirmation_code = str(uuid.uuid4())
    user.confirmation_code = confirmation_code
    subject = 'YAMDb registration'
    message = f'You confirmation code {user.confirmation_code}'
    send_mail(
        subject,
        message,
        settings.EMAIL_ADMIN,
        [user.email],
    )
    user.save()
