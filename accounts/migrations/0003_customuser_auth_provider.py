# Generated by Django 5.0.2 on 2024-03-01 08:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0002_passwordresetcode"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="auth_provider",
            field=models.CharField(default="Email", max_length=50),
        ),
    ]
