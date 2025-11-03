import logging
import random
import threading

from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import CustomUser, OneTimePassword, PasswordResetCode, Profile

logger = logging.getLogger(__name__)


@receiver(post_save, sender=CustomUser)
def send_code_on_user_creation(sender, instance, created, **kwargs):
    if created:
        subject = "One Time passcode for Email Verification"
        otp_code = generate_otp()
        current_site = "Housetech.com"
        email_body = f"Welcome {instance.first_name} thanks for signing up on {current_site} please verify your email with \n verification code {otp_code} "
        from_email = settings.DEFAULT_FROM_EMAIL

        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = [instance.email]

        # Create OneTimePassword object
        OneTimePassword.objects.create(user=instance, code=otp_code)
        Profile.objects.create(user=instance)

        threading.Thread(
            target=send_mail,
            args=(
                subject,
                email_body,
                from_email,
                to_email,
            ),
        ).start()


def generate_otp():
    return "".join(str(random.randint(1, 9)) for _ in range(6))


@receiver(post_save, sender=PasswordResetCode)
def send_code_on_reset_password_creation(sender, instance, created, **kwargs):
    if created:
        otp_code = generate_otp()
        subject = "Password Reset Code"
        current_site = "Housetech.com"
        email_body = f"Hi {instance.user.first_name}, here is your code for reset password on {current_site}: {otp_code}"

        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = [instance.user.email]

        # Update the existing PasswordResetCode instance with the generated code
        instance.code = otp_code
        instance.save()

        send_mail(
            subject,
            email_body,
            from_email,
            to_email,
            fail_silently=True,
        )
