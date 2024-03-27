from django.db import models
import uuid
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.utils.translation import gettext_lazy as _
# from rest_framework_simplejwt.tokens import RefreshToken
# from phonenumber_field.modelfields import PhoneNumberField
from apps.utils.models import TimeStampedUUIDModel


class CustomUserManager(BaseUserManager):
    def email_validator(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError(_("Please Enter a Valid Email"))

    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        if not email:
            raise ValueError(_("Users must have an email address"))
        if not first_name:
            raise ValueError(_("First name is required"))
        if not last_name:
            raise ValueError(_("Last name is required"))

        email = self.normalize_email(email)
        self.email_validator(email)
        user = self.model(
            email=email, first_name=first_name, last_name=last_name, **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, first_name, last_name, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("is_staff must be True for admin user"))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("is_superuser must be True for admin user"))
        if extra_fields.get("is_active") is not True:
            raise ValueError(_("is_active must be True for admin user"))
        if password is None:
            raise TypeError("Superusers must have a password.")
        if email is None:
            raise TypeError("Superusers must have an email.")

        user = self.create_user(email, first_name, last_name, password, **extra_fields)
        user.save(using=self._db)
        return user


AUTH_PROVIDERS = {"email": "Email", "google": "Google"}


class CustomUser(AbstractBaseUser, PermissionsMixin):
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField(max_length=255, unique=True, verbose_name=_("Email"))
    first_name = models.CharField(verbose_name=_("First Name"), max_length=50)
    last_name = models.CharField(verbose_name=_("Last Name"), max_length=50)
    auth_provider = models.CharField(max_length=50, default=AUTH_PROVIDERS.get("email"), verbose_name=_("Auth Provider"))
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(default=timezone.now)
    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]
    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.email

    # def tokens(self):
    #     refresh = RefreshToken.for_user(self)
    #     return {"refresh": str(refresh), "access": str(refresh.access_token)}


class OneTimePassword(models.Model):
    user = models.OneToOneField(
        CustomUser, verbose_name=_("user"), on_delete=models.CASCADE
    )
    code = models.CharField(max_length=6, unique=True)

    def __str__(self):
        return f"{self.user.first_name}-passcode"


class PasswordResetCode(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name}-reset-code"


class Gender(models.TextChoices):
    MALE = "Male",_("MALE")
    FEMALE = "Female",_("Female")

class Profile(TimeStampedUUIDModel):
    user = models.OneToOneField(CustomUser, related_name = "profile", on_delete = models.CASCADE)
    phone_number = models.CharField(
        verbose_name=_("Phone Number"), max_length=30, default="0999999999"
    )
    about_me = models.TextField(
        verbose_name=_("About me"), default="say something about yourself"
    )
    profile_photo = models.ImageField(
        verbose_name=_("Profile Photo"), default="/user.png"
    )
    gender = models.CharField(
        verbose_name=_("Gender"),
        choices=Gender.choices,
        default=Gender.MALE,
        max_length=20,
    )
    city = models.CharField(
        verbose_name=_("City"),
        max_length=180,
        default="Homs",
        blank=False,
        null=False,
    )
    is_buyer = models.BooleanField(
        verbose_name=_("Buyer"),
        default=False,
        help_text=_("Are you looking to Buy a Property?"),
    )
    is_seller = models.BooleanField(
        verbose_name=_("Seller"),
        default=False,
        help_text=_("Are you looking to Sell a Property?"),
    )
    is_agent = models.BooleanField(
        verbose_name=_("Agent"), default=False, help_text=_("Are you an agent?")
    )
    rating = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    num_reviews = models.IntegerField(
        verbose_name=_("Number of Reviews"), default=0, null=True, blank=True
    )

    def __str__(self):
        return f"{self.user.get_full_name}'s profile"