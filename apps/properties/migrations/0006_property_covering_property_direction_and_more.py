# Generated by Django 5.0.2 on 2024-04-26 23:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "properties",
            "0005_property_floor_number_alter_property_property_type_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="property",
            name="covering",
            field=models.CharField(
                choices=[
                    ("عادي", "عادي"),
                    ("سوبر", "سوبر"),
                    ("جيد", "جيد"),
                    ("جيد جدا", "جيد جدا"),
                    ("ممتاز", "ممتاز"),
                ],
                default="جيد",
                max_length=20,
                verbose_name="الاكساء",
            ),
        ),
        migrations.AddField(
            model_name="property",
            name="direction",
            field=models.CharField(
                blank=True,
                choices=[
                    ("شرق", "شرق"),
                    ("غرب", "غرب"),
                    ("شمال", "شمال"),
                    ("جنوب", "جنوب"),
                ],
                null=True,
                verbose_name="الاتجاه",
            ),
        ),
        migrations.AddField(
            model_name="property",
            name="elevator",
            field=models.BooleanField(default=False, verbose_name="مصعد"),
        ),
        migrations.AddField(
            model_name="property",
            name="furnishings",
            field=models.CharField(default="good", verbose_name="الفرش"),
        ),
        migrations.AddField(
            model_name="property",
            name="pool",
            field=models.BooleanField(default=False, verbose_name="مسبح"),
        ),
        migrations.AddField(
            model_name="property",
            name="ptype",
            field=models.CharField(
                choices=[
                    ("طابو أخضر", "طابو أخضر"),
                    ("عقد بيع قطعي", "عقد بيع قطعي"),
                    ("حكم المحكمة", "حكم المحكمة"),
                    ("وكالة كاتب العدل", "وكالة كاتب العدل"),
                    ("طابو أسهم", "طابو أسهم"),
                    ("طابو زراعي", "طابو زراعي"),
                    ("طابو إسكان", "طابو إسكان"),
                    ("فروغ", "فروغ"),
                ],
                default="طابو أخضر",
                max_length=50,
                verbose_name="نوع الملكية",
            ),
        ),
        migrations.AddField(
            model_name="property",
            name="solar_panels",
            field=models.BooleanField(default=False, verbose_name="طاقة شمسية"),
        ),
        migrations.AddField(
            model_name="property",
            name="total_rooms",
            field=models.IntegerField(default=1, verbose_name="عدد الغرف"),
        ),
        migrations.AlterField(
            model_name="property",
            name="property_status",
            field=models.CharField(
                choices=[("For Sale", "بيع"), ("For Rent", "أجار")],
                default="For Sale",
                max_length=50,
                verbose_name="Property Status",
            ),
        ),
        migrations.AlterField(
            model_name="property",
            name="property_type",
            field=models.CharField(
                choices=[
                    ("House", "بيت"),
                    ("Apartment", "شقة"),
                    ("Villa", "فيلا"),
                    ("Office", "مكتب"),
                    ("Chalet", "شاليه"),
                    ("Commercial", "تجاري"),
                    ("Farm", "مزرعة"),
                    ("Building", "بناء"),
                    ("Land", "أرض"),
                    ("Other", "اخر"),
                ],
                default="Other",
                max_length=50,
                verbose_name="Property Type",
            ),
        ),
    ]
