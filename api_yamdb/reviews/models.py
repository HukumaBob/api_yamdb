from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    RegexValidator)


class User(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('moderator', 'Moderator'),
        ('admin', 'Admin'),
    )
    VALIDATOR = RegexValidator(r'^[\w.@+-]+\Z')
    username = models.CharField(
        validators=[VALIDATOR],
        max_length=150,
        unique=True
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Email'
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
    confirmation_code = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Confirmation code',
        default='00000000'
    )

    @property
    def is_moderator(self):
        if self.role == self.ROLE_CHOICES['moderator']:
            return True
        else:
            return False

    @property
    def is_user(self):
        if self.role == self.ROLE_CHOICES['user']:
            return True
        else:
            return False

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_username_email'
            )
        ]


class Category(models.Model):
    pass


class Genre(models.Model):
    pass


class Title(models.Model):
    pass


class TitleGenre(models.Model):
    pass


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Title'
    )
    text = models.TextField(
        verbose_name='Text'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Author'
    )
    score = models.IntegerField(
        validators=[MinValueValidator(1),
                    MaxValueValidator(10)],
        verbose_name='Score'
    )
    pub_date = models.DateTimeField(
        auto_now=True,
        db_index=True,
        verbose_name='Add date'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title_id', 'author'],
                name='review_only_once'
            )
        ]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Review'
    )
    text = models.TextField(
        verbose_name='Text'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Author'
    )
    pub_date = models.DateTimeField(
        auto_now=True,
        db_index=True,
        verbose_name='Add date'
    )
