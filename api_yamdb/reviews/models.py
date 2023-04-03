from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    RegexValidator)
from .validators import validate_year


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
    '''Категории произведений (книги, фильмы, музыка и т.п)'''
    name = models.CharField(
        max_length=256,
        verbose_name='Название категории',
        help_text='Категория произведений'
    )
    slug = models.SlugField(
        unique=True, max_length=50,
        verbose_name='Slug',
        help_text='Категория произведений'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    '''Жанры произведений'''
    name = models.CharField(
        max_length=256,
        verbose_name='Название жанра',
        help_text='Жанр произведения')
    slug = models.SlugField(
        max_length=50,
        help_text='Жанр произведения',
        verbose_name='Slug'
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    '''Произведения'''
    name = models.CharField(
        max_length=256,
        verbose_name='Название',
        help_text='Название произведения')
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанры',
        help_text='Жанры произведения'
    )
    category = models.ForeignKey(
        Category,
        blank=False,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория',
        help_text='Категория произведения',
    )
    description = models.TextField(
        max_length=510,
        blank=True,
        verbose_name='Описание',
        help_text='Описание произведения'
    )
    year = models.IntegerField(
        verbose_name='Год выхода',
        help_text='Год выхода произведения',
        validators=[validate_year]
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


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
