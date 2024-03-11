from django.urls import path
from .views import *

urlpatterns = [
    path("register/", RegisterUserAPIView.as_view(), name="register"),
    path("verify-email/", VerifyUserEmailAPIView.as_view(), name="verify"),
    path("login/", LoginUserAPIView.as_view(), name="login"),
    path(
        "password-reset/",
        PasswordResetRequestAPIView.as_view(),
        name="password-reset-request",
    ),
    path(
        "password-reset/confirm/",
        PasswordResetConfirmAPIView.as_view(),
        name="password-reset-confirm",
    ),
    path(
        "profile/",
        GetProfileAPIView.as_view(),
        name = "get_user_profile"
    ),
    path(
        "edit-profile",
        UpdateProfileAPIView.as_view(),
        name = "update_user_profile"
    )

]
