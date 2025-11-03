# pip install google-api-python-client

from django.conf import settings
from django.contrib.auth import authenticate
from google.auth.transport import requests
from google.oauth2 import id_token
from rest_framework.exceptions import AuthenticationFailed

from apps.accounts.models import CustomUser


class Google:
    @staticmethod
    def validate(access_token):
        try:
            id_info = id_token.verify_oauth2_token(access_token, requests.Request())
            if "accounts.google.com" in id_info("lss"):
                return id_info
        except Exception:
            return "Token is Invalid or has Expired"


def login_social_user(email, password):
    user = authenticate(email=email, password=settings.SOCIAL_AUTH_PASSWORD)
    user_tokens = user.tokens()
    return {
        "email": user.email,
        "full_name": user.get_full_name,
        "access_token": str(user_tokens.get("access")),
        "refresh_token": str(user_tokens.get("refresh")),
    }


def register_social_user(provider, email, first_name, last_name):
    user = CustomUser.objects.filter(email=email)
    if user.exists():
        if provider == user[0].auth_provider:
            result = login_social_user(email, settings.SOCIAL_AUTH_PASSWORD)
            return result
        else:
            raise AuthenticationFailed(
                f"Please continue your login with {user[0].auth_provider}"
            )

    new_user = {
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "password": settings.SOCIAL_AUTH_PASSWORD,
    }
    register_user = CustomUser.objects.create_user(**new_user)
    register_user.auth_provider = provider
    register_user.is_active = True
    register_user.save()
    result = login_social_user(
        email=register_user.email, password=settings.SOCIAL_AUTH_PASSWORD
    )
    return result
