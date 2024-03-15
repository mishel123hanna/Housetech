from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from .models import *
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework.authtoken.models import Token




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
    token = serializers.CharField(max_length = 100, read_only=True)
    # access_token = serializers.CharField(max_length=255, read_only=True)
    # refresh_token = serializers.CharField(max_length=255, read_only=True)

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
        token = Token.objects.get_or_create(user=user)
        print(token)
        return {
            "email": user.email,
            "full_name": user.get_full_name,
            "token": token[0],
            # "refresh_token": str(user_tokens.get("refresh")),
        }


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()


# class LogoutSerializer(serializers.Serializer):
#     refresh_token = serializers.CharField()

#     def validate(self, attrs):
#         self.token = attrs.get('refresh_token')
#         return attrs

#     def save(self, **kwargs):
#         try:
#             RefreshToken(self.token)
#             token.blacklist()
#         except TokenError:
#             return self.fail("bad token")

class ProfileSerializer(serializers.Serializer):
    first_name = serializers.CharField(source = "user.first_name")
    last_name = serializers.CharField(source = "user.last_name")
    email = serializers.CharField(source = "user.email")
    gender = serializers.CharField()
    phone_number = serializers.CharField()
    about_me = serializers.CharField()
    profile_photo = serializers.ImageField()
    city = serializers.CharField()
    is_buyer = serializers.BooleanField()
    is_seller = serializers.BooleanField()
    is_agent = serializers.BooleanField()
    top_agent = serializers.BooleanField()
    rating = serializers.DecimalField(max_digits=4, decimal_places=2)
    num_reviews = serializers.IntegerField()
    full_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Profile
        fields = [
            "first_name",
            "last_name",
            "full_name",
            "email",
            "id",
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
            "reviews",
        ]
    
    def get_full_name(self, obj):
        first_name = obj.user.first_name.title()
        last_name = obj.user.last_name.title()
        return f"{first_name} {last_name}"
    

class UpdateProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = [
            "gender",
            "phone_number",
            "about_me",
            "profile_photo",
            "city",
            "is_buyer",
            "is_seller",
            "is_agent",
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.top_agent:
            representation["top_agent"] = True
        return representation
