# Generated by Django 5.0.2 on 2024-03-25 19:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("properties", "0003_alter_property_price"),
    ]

    operations = [
        migrations.AlterField(
            model_name="property",
            name="price",
            field=models.CharField(max_length=202, verbose_name="Price"),
        ),
    ]
