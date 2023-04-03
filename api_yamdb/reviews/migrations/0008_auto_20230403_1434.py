# Generated by Django 3.2 on 2023-04-03 11:34

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0007_auto_20230402_1952'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='author',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='reviews.user', verbose_name='Author'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='review',
            name='pub_date',
            field=models.DateTimeField(auto_now=True, db_index=True, verbose_name='Add date'),
        ),
        migrations.AddField(
            model_name='review',
            name='score',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)], verbose_name='Score'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='review',
            name='text',
            field=models.TextField(default=0, verbose_name='Text'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='review',
            name='title',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='reviews.title', verbose_name='Title'),
            preserve_default=False,
        ),
        migrations.AddConstraint(
            model_name='review',
            constraint=models.UniqueConstraint(fields=('title_id', 'author'), name='review_only_once'),
        ),
    ]
