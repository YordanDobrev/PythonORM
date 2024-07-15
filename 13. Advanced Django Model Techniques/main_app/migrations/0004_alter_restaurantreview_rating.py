# Generated by Django 5.0.4 on 2024-07-15 16:49

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_restaurantreview'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurantreview',
            name='rating',
            field=models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(5)]),
        ),
    ]