from django.utils import timezone
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import CustomUser, OneTimePassword, PasswordResetCode, Profile
from .serializers import (
    LogoutSerializer,
    PasswordResetConfirmSerializer,
    PasswordResetSerializer,
    ProfileSerializer,
    UpdateProfileSerializer,
    UserLoginSerializer,
    UserRegisterationSerializer,
    VerifyOTPSerializer,
)
from .utils import generate_numeric_code, send_password_reset_email


class RegisterUserAPIView(GenericAPIView):
    serializer_class = UserRegisterationSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        user_data = request.data
        serializer = self.serializer_class(data=user_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user = serializer.data
            return Response(
                {
                    "data": user,
                    "message": f"hi {user['first_name']} thanks for signing up, a passcode has been sent to your email",
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyUserEmailAPIView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = VerifyOTPSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        otp_code = serializer.validated_data["otp"]
        email = serializer.validated_data["email"]

        otp_obj = (
            OneTimePassword.objects.select_related("user")
            .filter(user__email=email, code=otp_code)
            .first()
        )
        if not otp_obj:
            return Response(
                {"message": "Passcode is invalid or not associated with the user"},
                status=status.HTTP_403_FORBIDDEN,
            )

        user = otp_obj.user
        if not user.is_active:
            user.is_active = True
            user.save(update_fields=["is_active"])
        otp_obj.delete()
        return Response(
            {"message": "Account verified successfully"}, status=status.HTTP_200_OK
        )


class LoginUserAPIView(GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = LogoutSerializer

    def post(self, request):
        token = getattr(request, "auth", None)
        if token is None:
            # Fall back to clearing tokens associated with the user.
            Token.objects.filter(user=request.user).delete()
            return Response(
                {"success": "Successfully logged out."}, status=status.HTTP_200_OK
            )

        if hasattr(token, "delete"):
            token.delete()
        else:
            Token.objects.filter(key=str(token)).delete()

        return Response(
            {"success": "Successfully logged out."}, status=status.HTTP_200_OK
        )


class PasswordResetRequestAPIView(GenericAPIView):
    serializer_class = PasswordResetSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response(
                {"message": "Email does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        reset_code = generate_numeric_code()
        reset_entry, _ = PasswordResetCode.objects.get_or_create(user=user)
        reset_entry.code = reset_code
        reset_entry.timestamp = timezone.now()
        reset_entry.save(update_fields=["code", "timestamp"])

        send_password_reset_email(user, reset_code)

        return Response(
            {"message": "Password reset email sent successfully."},
            status=status.HTTP_200_OK,
        )


class PasswordResetConfirmAPIView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        reset_entry = serializer.validated_data["reset_entry"]
        new_password = serializer.validated_data["new_password"]

        if not new_password:
            return Response({"email": user.email, "valid": True}, status=status.HTTP_200_OK)

        user.set_password(new_password)
        user.save(update_fields=["password"])
        reset_entry.delete()

        return Response(
            {"message": "Successfully reset password"},
            status=status.HTTP_201_CREATED,
        )


class GetProfileAPIView(GenericAPIView):
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            profile = request.user.profile
        except Profile.DoesNotExist:
            return Response(
                {"message": "Profile not found."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(profile, context={"request": request})
        return Response({"profile": serializer.data}, status=status.HTTP_200_OK)


class UpdateProfileAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    serializer_class = UpdateProfileSerializer

    def patch(self, request):
        try:
            profile = request.user.profile
        except Profile.DoesNotExist:
            return Response(
                {"message": "user does not exist"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(
            profile, data=request.data, partial=True, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


# class TopAgentsListAPIView(generics.ListAPIView):
#     permission_classes = (IsAuthenticated,)
#     queryset = Profile.objects.filter(top_agent=True)
#     serializer_class = ProfileSerializer


class AgentListAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Profile.objects.filter(is_agent=True)
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return super().get_queryset().select_related("user")
