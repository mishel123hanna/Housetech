# Generated by Django 5.0.2 on 2024-07-07 23:29

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0007_alter_profile_profile_photo"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="profile_photo",
            field=cloudinary.models.CloudinaryField(
                default="https://res.cloudinary.com/dl9tgk3vr/user.png",
                max_length=255,
                verbose_name="Profile Photo",
            ),
        ),
    ]
