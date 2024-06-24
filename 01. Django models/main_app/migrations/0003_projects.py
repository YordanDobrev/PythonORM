# Generated by Django 5.0.4 on 2024-06-24 15:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_delete_locations_department_location'),
    ]

    operations = [
        migrations.CreateModel(
            name='Projects',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField()),
                ('budget', models.DecimalField(decimal_places=2, max_digits=10)),
                ('duration_in_days', models.PositiveIntegerField(verbose_name='Duration in Days')),
                ('estimated_hours', models.FloatField(verbose_name='Estimated Hours')),
                ('start_date', models.DateField(default=datetime.date.today, verbose_name='Start Date')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('last_edited_on', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
