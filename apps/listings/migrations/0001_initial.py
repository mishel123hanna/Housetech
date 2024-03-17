# Generated by Django 5.0.2 on 2024-03-17 14:35

import autoslug.fields
import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Property",
            fields=[
                (
                    "pkid",
                    models.BigAutoField(
                        editable=False, primary_key=True, serialize=False
                    ),
                ),
                (
                    "id",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "title",
                    models.CharField(max_length=250, verbose_name="Property Title"),
                ),
                (
                    "slug",
                    autoslug.fields.AutoSlugField(
                        always_update=True,
                        editable=False,
                        populate_from="title",
                        unique=True,
                    ),
                ),
                (
                    "ref_code",
                    models.CharField(
                        blank=True,
                        max_length=255,
                        unique=True,
                        verbose_name="Property Reference Code",
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        default="Default description...update me please....",
                        verbose_name="Description",
                    ),
                ),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2,
                        default=0.0,
                        max_digits=8,
                        verbose_name="Price",
                    ),
                ),
                (
                    "plot_area",
                    models.DecimalField(
                        decimal_places=2,
                        default=0.0,
                        max_digits=8,
                        verbose_name="Plot Area(m^2)",
                    ),
                ),
                (
                    "property_status",
                    models.CharField(
                        choices=[("For Sale", "For Sale"), ("For Rent", "For Rent")],
                        default="For Sale",
                        max_length=50,
                        verbose_name="Advert Type",
                    ),
                ),
                (
                    "property_type",
                    models.CharField(
                        choices=[
                            ("House", "House"),
                            ("Apartment", "Apartment"),
                            ("Office", "Office"),
                            ("Warehouse", "Warehouse"),
                            ("Commercial", "Commercial"),
                            ("Other", "Other"),
                        ],
                        default="Other",
                        max_length=50,
                        verbose_name="Property Type",
                    ),
                ),
                (
                    "cover_photo",
                    models.ImageField(
                        blank=True,
                        default="/house_sample.jpg",
                        null=True,
                        upload_to="",
                        verbose_name="Main Photo",
                    ),
                ),
                ("city", models.CharField(max_length=50)),
                ("region", models.CharField(max_length=50)),
                ("street", models.CharField(max_length=50)),
                ("views", models.IntegerField(default=0, verbose_name="Total Views")),
                (
                    "total_floors",
                    models.IntegerField(default=0, verbose_name="Number of floors"),
                ),
                ("bedrooms", models.IntegerField(default=1, verbose_name="Bedrooms")),
                ("bathrooms", models.IntegerField(default=1, verbose_name="Bathrooms")),
                ("kitchens", models.IntegerField(default=1, verbose_name="Kitchens")),
                (
                    "living_rooms",
                    models.IntegerField(default=1, verbose_name="Living rooms"),
                ),
                (
                    "published_status",
                    models.BooleanField(default=False, verbose_name="Published Status"),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="owner",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Agent,Seller or Buyer",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Pictures",
            fields=[
                (
                    "pkid",
                    models.BigAutoField(
                        editable=False, primary_key=True, serialize=False
                    ),
                ),
                (
                    "id",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "picture",
                    models.ImageField(
                        blank=True,
                        default="/interior_sample.jpg",
                        null=True,
                        upload_to="",
                    ),
                ),
                (
                    "property_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="listings.property",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="PropertyViews",
            fields=[
                (
                    "pkid",
                    models.BigAutoField(
                        editable=False, primary_key=True, serialize=False
                    ),
                ),
                (
                    "id",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("ip", models.CharField(max_length=250, verbose_name="IP Address")),
                (
                    "property",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="property_views",
                        to="listings.property",
                    ),
                ),
            ],
            options={
                "verbose_name": "Total Views on Property",
                "verbose_name_plural": "Total Property Views",
            },
        ),
    ]