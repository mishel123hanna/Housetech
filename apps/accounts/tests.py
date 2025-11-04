from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from apps.accounts.models import OneTimePassword, PasswordResetCode, Profile


class AccountsAPITests(APITestCase):
    def setUp(self):
        super().setUp()
        utils_patcher = patch("apps.accounts.utils.send_async_mail")
        self.mock_send_async = utils_patcher.start()
        self.addCleanup(utils_patcher.stop)

        signals_patcher = patch(
            "apps.accounts.signals.send_async_mail", new=self.mock_send_async
        )
        signals_patcher.start()
        self.addCleanup(signals_patcher.stop)
        self.user_model = get_user_model()
        self.password = "TestPass123!"

    def create_user(self, email="jane@example.com", is_active=True):
        user = self.user_model.objects.create_user(
            email=email,
            first_name="Jane",
            last_name="Doe",
            password=self.password,
        )
        if is_active:
            user.is_active = True
            user.save(update_fields=["is_active"])
        self.mock_send_async.reset_mock()
        return user

    def authenticate(self, user):
        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        return token

    def test_registration_creates_profile_and_otp(self):
        response = self.client.post(
            reverse("register"),
            {
                "email": "newuser@example.com",
                "first_name": "New",
                "last_name": "User",
                "password": "SecurePass123!",
                "password2": "SecurePass123!",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = self.user_model.objects.get(email="newuser@example.com")
        self.assertFalse(user.is_active)
        self.assertTrue(Profile.objects.filter(user=user).exists())

        otp = OneTimePassword.objects.get(user=user)
        self.assertEqual(len(otp.code), 6)
        self.mock_send_async.assert_called_once()

    def test_email_verification_activates_user(self):
        self.client.post(
            reverse("register"),
            {
                "email": "verifyme@example.com",
                "first_name": "Verify",
                "last_name": "Me",
                "password": "SecurePass123!",
                "password2": "SecurePass123!",
            },
            format="json",
        )
        user = self.user_model.objects.get(email="verifyme@example.com")
        otp_code = OneTimePassword.objects.get(user=user).code

        response = self.client.post(
            reverse("verify"),
            {"email": user.email, "otp": otp_code},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertTrue(user.is_active)
        self.assertFalse(OneTimePassword.objects.filter(user=user).exists())

    def test_login_returns_token_for_active_user(self):
        user = self.create_user(email="login@example.com", is_active=True)

        response = self.client.post(
            reverse("login"),
            {"email": user.email, "password": self.password},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token_key = response.data["token"]
        self.assertTrue(Token.objects.filter(key=token_key, user=user).exists())

    def test_password_reset_request_creates_code_and_sends_email(self):
        user = self.create_user(email="reset@example.com", is_active=True)
        self.mock_send_async.reset_mock()

        response = self.client.post(
            reverse("password-reset-request"),
            {"email": user.email},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        reset_entry = PasswordResetCode.objects.get(user=user)
        self.assertEqual(len(reset_entry.code), 6)
        self.mock_send_async.assert_called_once()

    def test_password_reset_confirm_validates_and_updates_password(self):
        user = self.create_user(email="confirm@example.com", is_active=True)
        response = self.client.post(
            reverse("password-reset-request"),
            {"email": user.email},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        reset_code = PasswordResetCode.objects.get(user=user).code

        response = self.client.post(
            reverse("password-reset-confirm"),
            {"email": user.email, "code": reset_code},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"email": user.email, "valid": True})

        new_password = "NewSecurePass456!"
        response = self.client.post(
            reverse("password-reset-confirm"),
            {
                "email": user.email,
                "code": reset_code,
                "new_password": new_password,
                "confirm_password": new_password,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user.refresh_from_db()
        self.assertTrue(user.check_password(new_password))
        self.assertFalse(PasswordResetCode.objects.filter(user=user).exists())

    def test_profile_retrieval_and_update(self):
        user = self.create_user(email="profile@example.com", is_active=True)
        profile = user.profile
        profile.preferred_locations = "Homs"
        profile.save()

        token = self.authenticate(user)

        response = self.client.get(reverse("get_user_profile"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["profile"]["email"], user.email)

        payload = {
            "user": {"first_name": "Updated", "last_name": "Name"},
            "city": "Damascus",
            "phone_number": "0100000000",
            "preferred_locations": ["Damascus", "Homs"],
        }
        response = self.client.patch(
            reverse("update_user_profile"),
            payload,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user.refresh_from_db()
        profile.refresh_from_db()
        self.assertEqual(user.first_name, "Updated")
        self.assertEqual(profile.city, "Damascus")
        self.assertEqual(
            profile.preferred_locations_list,
            ["Damascus", "Homs"],
        )

        self.client.credentials()
        Token.objects.filter(key=token.key).delete()

    def test_logout_removes_token(self):
        user = self.create_user(email="logout@example.com", is_active=True)
        token = self.authenticate(user)

        response = self.client.post(reverse("logout"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Token.objects.filter(key=token.key).exists())

        self.client.credentials()

    def test_agent_list_returns_only_agents(self):
        agent = self.create_user(email="agent@example.com", is_active=True)
        agent.profile.is_agent = True
        agent.profile.save()

        non_agent = self.create_user(email="buyer@example.com", is_active=True)
        non_agent.profile.is_agent = False
        non_agent.profile.save()

        response = self.client.get(reverse("get_all_agents"))
        self.assertIn(
            response.status_code,
            {status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN},
        )

        token = self.authenticate(agent)
        response = self.client.get(reverse("get_all_agents"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["email"], agent.email)

        self.client.credentials()
        Token.objects.filter(key=token.key).delete()
