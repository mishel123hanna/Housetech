import random
import string
from django.db import models
# from django.contrib.gis.db import models as gis_models
# from django.contrib.gis.geos import Point
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from autoslug import AutoSlugField

User = get_user_model()

# class Location(models.Model):
#     latitude = gis_models.FloatField(verbose_name=_("Latitude"))
#     longitude = gis_models.FloatField(verbose_name=_("Longitude"))
#     city = models.CharField(max_length=50)
#     region = models.CharField(max_length=50)
#     street = models.CharField(max_length=50)

    # def __str__(self):
    #     return f"{self.latitude}, {self.longitude}"

class Property(models.Model):
    class PropertyStatus(models.TextChoices):
        FOR_SALE = "For Sale", _("For Sale")
        FOR_RENT = "For Rent", _("For Rent")

    class PropertyType(models.TextChoices):
        HOUSE = "House", _("House")
        APARTMENT = "Apartment", _("Apartment")
        OFFICE = "Office", _("Office")
        WAREHOUSE = "Warehouse", _("Warehouse")
        COMMERCIAL = "Commercial", _("Commercial")
        OTHER = "Other", _("Other")
    
    user = models.ForeignKey(
            User,
            verbose_name=_("Agent,Seller or Buyer"),
            related_name="owner",
            on_delete=models.DO_NOTHING,
        )   
    title = models.CharField(verbose_name=_("Property Title"), max_length=250)
    slug = AutoSlugField(populate_from="title", unique=True, always_update=True)
    ref_code = models.CharField(
        verbose_name=_("Property Reference Code"),
        max_length=255,
        unique=True,
        blank=True,
    )
    description = models.TextField(
        verbose_name=_("Description"),
        default="Default description...update me please....",
    )
    
    price = models.DecimalField(
            verbose_name=_("Price"), max_digits=8, decimal_places=2, default=0.0)
    plot_area = models.DecimalField(
        verbose_name=_("Plot Area(m^2)"), max_digits=8, decimal_places=2, default=0.0
    )

    property_status = models.CharField(
        verbose_name=_("Advert Type"),
        max_length=50,
        choices=PropertyStatus.choices,
        default=PropertyStatus.FOR_SALE,
    )

    property_type = models.CharField(
        verbose_name=_("Property Type"),
        max_length=50,
        choices=PropertyType.choices,
        default=PropertyType.OTHER,
    )
    cover_photo = models.ImageField(
        verbose_name=_("Main Photo"), default="/house_sample.jpg", null=True, blank=True
    )
    views = models.IntegerField(verbose_name=_("Total Views"), default=0)
    total_floors = models.IntegerField(verbose_name=_("Number of floors"), default=0)
    bedrooms = models.IntegerField(verbose_name=_("Bedrooms"), default=1)
    bathrooms = models.IntegerField(verbose_name=_("Bathrooms"), default=1)
    kitchens = models.IntegerField(verbose_name=_("Kitchens"), default=1)
    living_rooms = models.IntegerField(verbose_name=_("Living rooms"), default=1)
    # location = models.OneToOneField(
    #     Location,
    #     on_delete=models.CASCADE,
    #     verbose_name=_("Property Location"),
    #     related_name="property_location",
    #     null=True,
    #     blank=True,
    # )
    objects = models.Manager()


    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.title = str.title(self.title)
        self.description = str.capitalize(self.description)
        self.ref_code = "".join(
            random.choices(string.ascii_uppercase + string.digits, k=10)
        )
        super(Property, self).save(*args, **kwargs)


class Pictures(models.Model):
    property_id = models.ForeignKey(Property, on_delete=models.CASCADE)
    picture = models.ImageField(default="/interior_sample.jpg",
        null=True,
        blank=True,)


