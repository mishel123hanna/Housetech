# Generated by Django 5.0.2 on 2024-03-05 07:44

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0004_alter_customuser_date_joined"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="last_login",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
