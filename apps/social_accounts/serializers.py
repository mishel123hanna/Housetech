from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from .utils import Google, register_social_user


class GoogleSignInSerializer(serializers.Serializer):
    access_token = serializers.CharField(min_length=6)

    def validate_access_tokne(self, access_token):
        google_user_data = Google.validate(access_token)
        try:
            user_id = google_user_data["sub"]

        except Exception:
            raise serializers.ValidationError("this Token is Invalid or has Expired")

        if google_user_data["aud"] != settings.GOOGLE_CLIENT_ID:
            raise AuthenticationFailed("could not verify user")

        email = google_user_data["email"]
        first_name = google_user_data["given_name"]
        last_name = google_user_data["family_name"]
        provider = "google"
        return register_social_user(provider, email, first_name, last_name)
