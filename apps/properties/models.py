import random
import string
from django.db import models
# from django.contrib.gis.db import models as gis_models
# from django.contrib.gis.geos import Point
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from autoslug import AutoSlugField
from apps.utils.models import TimeStampedUUIDModel

User = get_user_model()

class PropertyPublishedManager(models.Manager):
    def get_queryset(self):
        return (
            super(PropertyPublishedManager, self)
            .get_queryset()
            .filter(published_status=True)
        )
    
class Location(models.Model):
    # latitude = gis_models.FloatField(verbose_name=_("Latitude"))
    # longitude = gis_models.FloatField(verbose_name=_("Longitude"))
    city = models.CharField(verbose_name=_("City"), max_length=180, default="Homs")
    region = models.CharField(verbose_name=_("Region"), max_length=50, null=True, blank=True)
    street = models.CharField(verbose_name=_("Street Address"), max_length=150, null=True, blank=True)


    def __str__(self):
        return f"{self.city}-{self.region}"

class Property(TimeStampedUUIDModel):
    class PropertyStatus(models.TextChoices):
        FOR_SALE = "For Sale", _("For Sale")
        FOR_RENT = "For Rent", _("For Rent")

    class PropertyType(models.TextChoices):
        HOUSE = "House", _("House")
        APARTMENT = "Apartment", _("Apartment")
        VILLA = "Villa", _("Villa")
        OFFICE = "Office", _("Office")
        CHALET = "Chalet", _("Chalet")
        COMMERCIAL = "Commercial", _("Commercial")
        FARM = "Farm", _("Farm")
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
    
    price = models.IntegerField(
            verbose_name=_("Price"),default=0)
    plot_area = models.DecimalField(
        verbose_name=_("Plot Area(m^2)"), max_digits=8, decimal_places=2, default=0.0
    )

    property_status = models.CharField(
        verbose_name=_("Property Status"),
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
        verbose_name=_("Main Photo"), default="/house.jpeg", null=True, blank=True
    )
    # city = models.CharField(verbose_name=_("City"), max_length=180, default="Homs")
    # region = models.CharField(verbose_name=_("Region"), max_length=50, null=True, blank=True)
    # street = models.CharField(verbose_name=_("Street Address"), max_length=150, null=True, blank=True)
    property_number = models.IntegerField(
        verbose_name=_("Property Number"),
        validators=[MinValueValidator(1)],
        default=1,
    )
    views = models.IntegerField(verbose_name=_("Total Views"), default=0)
    total_floors = models.IntegerField(verbose_name=_("Number of floors"), default=0)
    bedrooms = models.IntegerField(verbose_name=_("Bedrooms"), default=1)
    bathrooms = models.IntegerField(verbose_name=_("Bathrooms"), default=1)
    kitchens = models.IntegerField(verbose_name=_("Kitchens"), default=1)
    living_rooms = models.IntegerField(verbose_name=_("Living rooms"), default=1)
    location = models.ForeignKey(
        Location,
        on_delete=models.DO_NOTHING,
        verbose_name=_("Property Location"),
        related_name="property_location",
    )
    published_status = models.BooleanField(
        verbose_name=_("Published Status"), default=False
    )
    objects = models.Manager()
    published = PropertyPublishedManager()


    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.title = str.title(self.title)
        self.description = str.capitalize(self.description)
        self.ref_code = "".join(
            random.choices(string.ascii_uppercase + string.digits, k=10)
        )
        super(Property, self).save(*args, **kwargs)


class PropertyPictures(TimeStampedUUIDModel):
    property_id = models.ForeignKey(Property, on_delete=models.CASCADE)
    image = models.ImageField(default="/house.jpg",
        null=True,
        blank=True,)


class PropertyViews(TimeStampedUUIDModel):
    ip = models.CharField(verbose_name=_("IP Address"), max_length=250)
    property = models.ForeignKey(
        Property, related_name="property_views", on_delete=models.CASCADE
    )

    def __str__(self):
        return (
            f"Total views on - {self.property.title} is - {self.property.views} view(s)"
        )

    class Meta:
        verbose_name = "Total Views on Property"
        verbose_name_plural = "Total Property Views"
