# Generated by Django 5.0.6 on 2024-05-14 13:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("gdparchis", "0003_game_state"),
    ]

    operations = [
        migrations.AddField(
            model_name="game",
            name="datetime",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2024, 5, 14, 13, 58, 18, 621178, tzinfo=datetime.timezone.utc
                )
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="game",
            name="max_players",
            field=models.IntegerField(default=4),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="game",
            name="uuid",
            field=models.UUIDField(default=1),
            preserve_default=False,
        ),
    ]