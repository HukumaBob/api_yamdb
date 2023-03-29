from django.contrib.auth.models import AbstractUser
from django.db import models
# from django.contrib.auth import get_user_model


class User(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('moderator', 'Moderator'),
        ('admin', 'Admin'),
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='user',
    )
    bio = models.TextField(
        'Description',
        blank=True,
    )


# User = get_user_model()


class Category(models.Model):
    pass


class Genre(models.Model):
    pass


class Title(models.Model):
    pass


class Review(models.Model):
    pass


class Comment(models.Model):
    pass
