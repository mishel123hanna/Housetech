# Generated by Django 5.0.2 on 2024-03-25 19:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("properties", "0005_alter_property_price"),
    ]

    operations = [
        migrations.AlterField(
            model_name="property",
            name="price",
            field=models.DecimalField(
                decimal_places=2, default=0.0, max_digits=20, verbose_name="Price"
            ),
        ),
    ]