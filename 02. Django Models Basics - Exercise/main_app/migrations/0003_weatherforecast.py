# Generated by Django 5.0.4 on 2024-06-25 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_blog_alter_person_age'),
    ]

    operations = [
        migrations.CreateModel(
            name='WeatherForecast',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('temperature', models.FloatField()),
                ('humidity', models.FloatField()),
                ('precipitation', models.FloatField()),
            ],
        ),
    ]
