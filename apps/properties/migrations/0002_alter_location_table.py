# Generated by Django 5.0.2 on 2024-03-30 09:33

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("properties", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelTable(
            name="location",
            table="properties_location",
        ),
    ]
