# Generated by Django 5.0.4 on 2024-07-15 16:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_alter_restaurantreview_rating'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='restaurantreview',
            unique_together={('reviewer_name', 'restaurant')},
        ),
    ]
