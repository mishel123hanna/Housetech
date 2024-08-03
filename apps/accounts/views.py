from django.utils import timezone
from django.shortcuts import get_object_or_404
from .models import *
from rest_framework import generics
from rest_framework.generics import GenericAPIView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import (
    UserRegisterationSerializer,
    UserLoginSerializer,
    PasswordResetSerializer,
    ProfileSerializer,
    UpdateProfileSerializer,
    VerifyOTPSerializer,
    LogoutSerializer,
    PasswordResetConfirmSerializer,
)
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings




class RegisterUserAPIView(GenericAPIView):
    serializer_class = UserRegisterationSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        user_data = request.data
        serializer = self.serializer_class(data=user_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user = serializer.data
            # send_code_to_user(user['email'])
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
        if not serializer.is_valid():
            return Response(
                {"message": "Invalid data provided"},
                status=status.HTTP_400_BAD_REQUEST
            )

        otp_code = serializer.validated_data.get("otp")
        email = serializer.validated_data.get("email")

        try:
            otp_obj = OneTimePassword.objects.get(user__email=email, code=otp_code)
            user = otp_obj.user
            if not user.is_active:
                user.is_active = True
                user.save()
            otp_obj.delete()
            return Response(
                {"message": "Account verified successfully"},
                status=status.HTTP_200_OK
            )
        except OneTimePassword.DoesNotExist:
            return Response(
                {"message": "Passcode is invalid or not associated with the user"},
                status=status.HTTP_403_FORBIDDEN
            )
        except Exception as e:
            return Response(
                {"message": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
class LoginUserAPIView(GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        print(request.user)
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class LogoutAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = LogoutSerializer
    def post(self, request):
        try:
            token = request.auth
            token.delete()
            return Response({'success': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetRequestAPIView(GenericAPIView):
    serializer_class = PasswordResetSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                email = serializer.validated_data["email"]
                user = CustomUser.objects.get(email=email)

                PasswordResetCode.objects.update_or_create(user=user, code=0)

                return Response(
                    {"message": "Password reset email sent successfully."},
                    status=status.HTTP_200_OK,
                )
            except:
                return Response(
                    {"message": "Email Does not Exist"},
                    status=status.HTTP_404_NOT_FOUND,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmAPIView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = PasswordResetConfirmSerializer
    def post(self, request):
        email = request.data.get("email", "")
        code = request.data.get("code", "")
        new_password = request.data.get("new_password", "")
        confirm_password = request.data.get("confirm_password")

        try:
            user = CustomUser.objects.get(email=email)
            reset_entry = PasswordResetCode.objects.get(user=user, code=code)

            # Verify if the reset code is still valid
            if (
                timezone.now() - reset_entry.timestamp
            ).seconds > settings.PASSWORD_RESET_TIMEOUT:
                raise AuthenticationFailed(
                    {"message": "Password reset code has expired."},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
            if code and not new_password:
                data = {"email": email, "valid": True}

                return Response(data, status=status.HTTP_200_OK)
            if code and new_password and confirm_password:
                if new_password == confirm_password:
                    user.set_password(new_password)
                    user.save()

                    reset_entry.delete()
                    return Response(
                        {"message": "successfully reset password"},
                        status=status.HTTP_201_CREATED,
                    )
                else:
                    raise AuthenticationFailed(
                        {"datial": "passwords did not match"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            else:
                return Response({"message":"email , code, new_password, confirm_password are required"})
        except CustomUser.DoesNotExist:
            return Response(
                {"message": "User with this email does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except PasswordResetCode.DoesNotExist:
            raise AuthenticationFailed(
                {"message": "Invalid or expired password reset code."},
            )
    




class GetProfileAPIView(GenericAPIView):
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        user = self.request.user
        user_profile = Profile.objects.get(user=user)
        serializer = ProfileSerializer(user_profile, context = {"request":request})
        return Response({"profile":serializer.data}, status=status.HTTP_200_OK)
    
class UpdateProfileAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    serializer_class = UpdateProfileSerializer

    def patch(self, request):
        email = request.user
        try:
            Profile.objects.get(user__email=email)
        except Profile.DoesNotExist:
            return Response({"message":"user does not exist"}, status = status.HTTP_404_NOT_FOUND)
        if email != email:
            return Response({"message":"Not your Profile"}, status=status.HTTP_403_FORBIDDEN)
        data = request.data
        serializer = UpdateProfileSerializer(
            instance=request.user.profile, data=data, partial=True
        )
        if serializer.is_valid():
            serializer.save()  
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

# class TopAgentsListAPIView(generics.ListAPIView):
#     permission_classes = (IsAuthenticated,)
#     queryset = Profile.objects.filter(top_agent=True)
#     serializer_class = ProfileSerializer

class AgentListAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Profile.objects.filter(is_agent=True)
    serializer_class = ProfileSerializer