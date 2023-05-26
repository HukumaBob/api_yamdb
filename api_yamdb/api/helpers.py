import uuid

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from reviews.models import User


def confirmation_code_to_email(username):
    # Retrieve the User object with the given username from the database
    user = get_object_or_404(User, username=username)

    # Generate a unique confirmation code using uuid.uuid4()
    confirmation_code = str(uuid.uuid4())

    # Assign the confirmation code to the user's confirmation_code field
    user.confirmation_code = confirmation_code

    # Set the email subject and message
    subject = 'YAMDb registration'
    message = f'Your confirmation code: {user.confirmation_code}'

    # Send an email using the Django send_mail() function
    send_mail(
        subject,
        message,
        settings.EMAIL_ADMIN,  # Sender's email address
        [user.email],  # Recipient's email address
    )

    # Save the updated user object with the assigned confirmation code
    user.save()
