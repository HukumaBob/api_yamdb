# Generated by Django 3.2 on 2023-04-05 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genre',
            name='slug',
            field=models.SlugField(help_text='Жанр произведения', unique=True, verbose_name='Slug'),
        ),
    ]
