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
    
class Location(TimeStampedUUIDModel):
    # latitude = gis_models.FloatField(verbose_name=_("Latitude"))
    # longitude = gis_models.FloatField(verbose_name=_("Longitude"))
    city = models.CharField(verbose_name=_("City"), max_length=180, default="Homs")
    region = models.CharField(verbose_name=_("Region"), max_length=50, null=True, blank=True)
    street = models.CharField(verbose_name=_("Street Address"), max_length=150, null=True, blank=True)


    def __str__(self):
        return f"{self.city}-{self.region}"

class Property(TimeStampedUUIDModel):
    class PropertyStatus(models.TextChoices):
        FOR_SALE = "For Sale", _("بيع")
        FOR_RENT = "For Rent", _("أجار")

    class PropertyType(models.TextChoices):
        HOUSE = "House", _("بيت")
        APARTMENT = "Apartment", _("شقة")
        VILLA = "Villa", _("فيلا")
        OFFICE = "Office", _("مكتب")
        CHALET = "Chalet", _("شاليه")
        COMMERCIAL = "Market", _("تجاري")
        FARM = "Farm", _("مزرعة")
        BUILDING = "Building", _("بناء")
        LAND = "Land", _("أرض")
        OTHER = "Other", _("اخر")
        
    class OwnershipType(models.TextChoices):
        A = "طابو أخضر", _("طابو أخضر")
        B = "عقد بيع قطعي", _("عقد بيع قطعي")
        C = "حكم محكمة", _("حكم محكمة")
        D = "وكالة كاتب بالعدل", _("وكالة كاتب بالعدل")
        E = "طابو أسهم", _("طابو أسهم")
        F = "طابو زراعي", _("طابو زراعي")
        G = "طابو إسكان", _("طابو إسكان")
        H = "فروغ", _("فروغ")

    class Covering(models.TextChoices):
        NORMAL = "عادي", _("عادي")
        SUPER = "سوبر",_("سوبر")
        GOOD = "جيد", _("جيد")
        VERYGOOD = "جيد جدا", _("جيد جدا")
        EXCELLENT = "ممتاز", _("ممتاز")

    class Direction(models.TextChoices):
        EAST = "شرق", _("شرق")
        WEST = "غرب", _("غرب")
        NORTH = "شمال", _("شمال")
        SOUTH = "جنوب", _("جنوب")
        NORTHEAST = "الشمال الشرقي", _("الشمال الشرقي")
        NORTHWEST = "الشمال الغربي", _("الشمال الغربي")
        SOUTHEAST = "الجنوب الشرقي", _("الجنوب الشرقي")
        SOUTHWEST = "الجنوب الغربي", _("الجنوب الغربي")


    class Furnishing(models.TextChoices):
        FURNISHED = "مفروش", _("مفروش")
        HALF_FURNISHED = "نص مفروش", _("نص مفروش")
        NOT_FURNISHED = "غير مفروش", _("غير مفروش")
    
    class RentType(models.TextChoices):
        MONTHLY = "شهري", _("شهري")
        DAILY = "يومي", _("يومي")

    class UserType(models.TextChoices):
        OWNER = "مالك", _("مالك")
        MERCHANT = "تاجر", _("تاجر")

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
    ownership_type = models.CharField(verbose_name=_("نوع الملكية"), max_length=50, choices=OwnershipType.choices, default=OwnershipType.A)
    user_type = models.CharField(verbose_name=_("نوع البائع"), max_length=50, choices=UserType.choices, default=UserType.OWNER)
    covering = models.CharField(verbose_name=_("الاكساء"), max_length=20, choices=Covering.choices, default=Covering.GOOD)
    # cover_photo = models.ImageField(
    #     verbose_name=_("Main Photo"), upload_to="property_main_images/", default="/house.jpg", null=True, blank=True
    # )
    # city = models.CharField(verbose_name=_("City"), max_length=180, default="Homs")
    # region = models.CharField(verbose_name=_("Region"), max_length=50, null=True, blank=True)
    # street = models.CharField(verbose_name=_("Street Address"), max_length=150, null=True, blank=True)
    property_number = models.IntegerField(
        verbose_name=_("Property Number"),
        validators=[MinValueValidator(1)],
        default=1,
    )
    views = models.IntegerField(verbose_name=_("Total Views"), default=0)
    total_floors = models.IntegerField(verbose_name=_("Numbers of floors"), default=0)
    floor_number = models.IntegerField(verbose_name=_("Number of floor"), default=0)
    bedrooms = models.IntegerField(verbose_name=_("Bedrooms"), default=1)
    bathrooms = models.IntegerField(verbose_name=_("Bathrooms"), default=1)
    kitchens = models.IntegerField(verbose_name=_("Kitchens"), default=1)
    living_rooms = models.IntegerField(verbose_name=_("Living rooms"), default=1)
    elevator = models.BooleanField(verbose_name=_("مصعد"), default=False)
    pool = models.BooleanField(verbose_name=_("مسبح"), default=False)
    solar_panels = models.BooleanField(verbose_name=_("طاقة شمسية"), default=False)
    furnishing = models.CharField(verbose_name=_("الفرش"), choices=Furnishing.choices, default=Furnishing.NOT_FURNISHED)
    direction = models.CharField(verbose_name=_("الاتجاه"), choices=Direction.choices, null=True, blank=True)
    total_rooms = models.IntegerField(verbose_name=_("عدد الغرف"), default=1)
    rent_type = models.CharField(verbose_name=_("نوع الأجار"), choices=RentType.choices, default=RentType.MONTHLY, null=True,blank=True)
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
        self.total_rooms = self.bedrooms+self.bathrooms+self.living_rooms+self.kitchens
        if self.property_status == Property.PropertyStatus.FOR_SALE:
            self.rent_type = None
        self.ref_code = "".join(
            random.choices(string.ascii_uppercase + string.digits, k=10)
        )
        super(Property, self).save(*args, **kwargs)


class PropertyImages(TimeStampedUUIDModel):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='property_images/', null=True, blank=True)

    class Meta:
        verbose_name = "Images For Property"
        verbose_name_plural = "Property Images"
    
    def __str__(self):
        return f"{self.property.title}-{self.property.property_type}"
    
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
