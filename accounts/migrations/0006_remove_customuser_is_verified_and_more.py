# Generated by Django 5.0.2 on 2024-03-05 07:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0005_alter_customuser_last_login"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="customuser",
            name="is_verified",
        ),
        migrations.AlterField(
            model_name="customuser",
            name="is_active",
            field=models.BooleanField(default=False),
        ),
    ]
