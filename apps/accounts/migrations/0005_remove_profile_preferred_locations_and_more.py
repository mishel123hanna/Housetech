# Generated by Django 5.0.2 on 2024-06-20 21:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0004_profile_preferred_locations"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="profile",
            name="preferred_locations",
        ),
        migrations.AddField(
            model_name="profile",
            name="preferred_locations",
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
