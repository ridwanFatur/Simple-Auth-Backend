# Generated by Django 4.2.7 on 2025-04-03 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user_settings", "0002_twofactorsettingmodel"),
    ]

    operations = [
        migrations.AddField(
            model_name="twofactorsettingmodel",
            name="is_active",
            field=models.BooleanField(default=False),
        ),
    ]
