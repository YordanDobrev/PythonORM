# Generated by Django 5.0.4 on 2024-07-31 07:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_alter_match_options_alter_match_players_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tournament',
            old_name='price_money',
            new_name='prize_money',
        ),
        migrations.AlterField(
            model_name='match',
            name='winner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='matches_won', to='main_app.tennisplayer'),
        ),
    ]
