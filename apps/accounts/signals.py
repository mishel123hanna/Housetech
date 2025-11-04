from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from .models import CustomUser, OneTimePassword, Profile
from .utils import generate_numeric_code, send_async_mail


@receiver(post_save, sender=CustomUser)
def send_code_on_user_creation(sender, instance, created, **kwargs):
    if created:
        subject = _("One Time passcode for Email Verification")
        otp_code = generate_numeric_code()
        current_site = "Housetech.com"
        email_body = _(
            "Welcome %(first_name)s thanks for signing up on %(site)s. "
            "Please verify your email using the verification code %(code)s."
        ) % {
            "first_name": instance.first_name,
            "site": current_site,
            "code": otp_code,
        }
        to_email = [instance.email]

        # Create OneTimePassword object
        OneTimePassword.objects.create(user=instance, code=otp_code)
        Profile.objects.create(user=instance)

        send_async_mail(subject, email_body, to_email)
