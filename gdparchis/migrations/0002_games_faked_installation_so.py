# Generated by Django 4.0.5 on 2022-07-04 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gdparchis', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='games',
            name='faked',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='installation',
            name='so',
            field=models.CharField(default=2, max_length=200),
            preserve_default=False,
        ),
    ]