"""Utility helpers for the accounts app."""
from __future__ import annotations

import random
import threading
from typing import Iterable, Optional

from django.conf import settings
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _


DEFAULT_CODE_LENGTH = 6


def generate_numeric_code(length: int = DEFAULT_CODE_LENGTH) -> str:
    """Return a random numeric string code of the desired length."""
    if length <= 0:
        raise ValueError("length must be a positive integer")
    return "".join(str(random.randint(0, 9)) for _ in range(length))


def send_async_mail(
    subject: str,
    message: str,
    recipient_list: Iterable[str],
    *,
    from_email: Optional[str] = None,
    fail_silently: bool = True,
) -> None:
    """Send email on a background thread to avoid blocking request handling."""
    if from_email is None:
        from_email = settings.DEFAULT_FROM_EMAIL

    # We intentionally use a background thread here because the legacy behaviour
    # relied on fire-and-forget email sending.
    thread = threading.Thread(
        target=send_mail,
        args=(subject, message, from_email, list(recipient_list)),
        kwargs={"fail_silently": fail_silently},
        daemon=True,
    )
    thread.start()


def send_password_reset_email(user, code: str) -> None:
    """Send the password reset code email to the supplied user."""
    subject = _("Password Reset Code")
    current_site = "Housetech.com"
    message = _(
        "Hi %(first_name)s, here is your password reset code for %(site)s: %(code)s"
    ) % {
        "first_name": user.first_name,
        "site": current_site,
        "code": code,
    }

    send_async_mail(subject, message, [user.email])
