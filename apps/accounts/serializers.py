from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.backends import ModelBackend
from django.utils import timezone
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed

from .models import CustomUser, PasswordResetCode, Profile


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=False, style={"input_type": "password"}
    )
    email = serializers.EmailField(read_only=True, required=False)

    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "email", "password"]

    def update(self, instance, validated_data):
        if "password" in validated_data:
            password = validated_data.pop("password")
            instance.set_password(password)

        # Update remaining validated data
        return super().update(instance, validated_data)


class UserRegisterationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=60, min_length=8, write_only=True)
    password2 = serializers.CharField(max_length=60, min_length=8, write_only=True)

    class Meta:
        model = CustomUser
        fields = ["email", "first_name", "last_name", "password", "password2"]

    def validate(self, attrs):
        password = attrs.get("password", "")
        password2 = attrs.get("password2", "")
        if password != password2:
            raise serializers.ValidationError("passwords do not match")
        return attrs

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            password=validated_data["password"],
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, min_length=6)
    password = serializers.CharField(max_length=60, write_only=True)
    full_name = serializers.CharField(max_length=255, read_only=True)
    token = serializers.CharField(max_length=100, read_only=True)

    class Meta:
        model = CustomUser
        fields = ["email", "password", "full_name", "token"]

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        request = self.context.get("request")

        user = authenticate(request, email=email, password=password)
        if not user:
            raise AuthenticationFailed("invalid credentials try again")
        if not user.is_active:
            raise AuthenticationFailed("Email is not Verified")
        token, _ = Token.objects.get_or_create(user=user)
        return {
            "email": user.email,
            "full_name": user.get_full_name,
            "token": token.key,
        }


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    email = serializers.CharField(source="user.email")
    full_name = serializers.SerializerMethodField(read_only=True)
    profile_photo = serializers.SerializerMethodField()
    preferred_locations = serializers.ListField(
        child=serializers.CharField(), required=False, source="preferred_locations_list"
    )

    class Meta:
        model = Profile
        fields = [
            "first_name",
            "last_name",
            "full_name",
            "email",
            "phone_number",
            "profile_photo",
            "about_me",
            "gender",
            "city",
            "is_buyer",
            "is_seller",
            "is_agent",
            "rating",
            "num_reviews",
            "preferred_locations",
        ]
        extra_kwargs = {
            "rating": {"allow_null": True},
            "num_reviews": {"required": False},
        }

    def get_full_name(self, obj):
        first_name = obj.user.first_name.title()
        last_name = obj.user.last_name.title()
        return f"{first_name} {last_name}"

    def get_profile_photo(self, obj):
        return f"{settings.CLOUDINARY_BASE_URL}/{obj.profile_photo}"


class UpdateProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    preferred_locations = serializers.ListField(
        child=serializers.CharField(), required=False, source="preferred_locations_list"
    )
    profile_photo_url = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            "user",
            "gender",
            "phone_number",
            "about_me",
            "profile_photo_url",
            "city",
            "is_buyer",
            "is_seller",
            "is_agent",
            "preferred_locations",
        ]

    def get_profile_photo_url(self, obj):
        return f"{settings.CLOUDINARY_BASE_URL}/{obj.profile_photo}"

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", None)
        preferred_locations_data = validated_data.pop("preferred_locations_list", None)

        if user_data:
            user_serializer = CustomUserSerializer(
                instance.user, data=user_data, partial=True
            )
            if user_serializer.is_valid():
                user_serializer.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if preferred_locations_data is not None:
            instance.preferred_locations = ",".join(preferred_locations_data)
            instance.save()
        return instance


class CustomEmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        User = get_user_model()

        if email is None or password is None:
            return None

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None

        if user.check_password(password) and user.is_active:
            return user
        elif user.check_password(password) and not user.is_active:
            # Handle inactive users here
            raise AuthenticationFailed(
                {"message": "Email is not Verified", "success": False}
            )

        else:
            return None


class VerifyOTPSerializer(serializers.Serializer):
    otp = serializers.CharField()
    email = serializers.EmailField()


class LogoutSerializer(serializers.Serializer):
    pass


class PasswordResetConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField()
    new_password = serializers.CharField(
        max_length=60, min_length=8, write_only=True, required=False
    )
    confirm_password = serializers.CharField(
        max_length=60, min_length=8, write_only=True, required=False
    )

    default_error_messages = {
        "password_mismatch": "passwords did not match",
        "password_required": "Both new_password and confirm_password are required.",
        "reset_code_expired": "Password reset code has expired.",
        "reset_code_invalid": "Invalid or expired password reset code.",
    }

    def validate(self, attrs):
        email = attrs.get("email")
        code = attrs.get("code")
        new_password = attrs.get("new_password")
        confirm_password = attrs.get("confirm_password")

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError(
                {"email": "User with this email does not exist."}
            )

        try:
            reset_entry = PasswordResetCode.objects.get(user=user, code=code)
        except PasswordResetCode.DoesNotExist:
            raise serializers.ValidationError({"code": self.error_messages["reset_code_invalid"]})

        timeout_seconds = getattr(settings, "PASSWORD_RESET_TIMEOUT", 0)
        if timeout_seconds:
            delta = timezone.now() - reset_entry.timestamp
            if delta.total_seconds() > timeout_seconds:
                raise serializers.ValidationError(
                    {"code": self.error_messages["reset_code_expired"]}
                )

        if new_password or confirm_password:
            if not new_password or not confirm_password:
                raise serializers.ValidationError(
                    {"new_password": self.error_messages["password_required"]}
                )
            if new_password != confirm_password:
                raise serializers.ValidationError(
                    {"confirm_password": self.error_messages["password_mismatch"]}
                )
            attrs["new_password"] = new_password
        else:
            attrs["new_password"] = None

        attrs["user"] = user
        attrs["reset_entry"] = reset_entry
        return attrs
