from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from users.models import User

User = get_user_model()

class UserApiTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="user@test.com",
            username="user",
            password="pass1234",
            role="unverified"
        )

    # --- Registration ---
    def test_register_user(self):
        url = reverse("register")
        data = {
            "email": "newuser@test.com",
            "username": "newuser",
            "password": "newpass123"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email="newuser@test.com").exists())

    def test_register_user_missing_field(self):
        url = reverse("register")
        data = {"email": "fail@test.com"}  # missing username and password
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # --- Verification Link ---
    def test_send_verification_link(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("verify")
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertIsNotNone(self.user.verification_token)

    def test_send_verification_link_already_verified(self):
        self.user.role = "verified"
        self.user.save()
        self.client.force_authenticate(user=self.user)
        url = reverse("verify")
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # --- Verify Email ---
    def test_verify_email_success(self):
        self.client.force_authenticate(user=self.user)
        self.user.verification_token = "12345678-1234-5678-1234-567812345678"
        self.user.verification_token_created = timezone.now()
        self.user.save()
        url = reverse("verify") + f"?token={self.user.verification_token}"
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.role, "verified")
        self.assertIsNone(self.user.verification_token)

    def test_verify_email_invalid_token(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("verify") + "?token=00000000-0000-0000-0000-000000000000"
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # --- Profile ---
    def test_get_profile(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("profile")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.user.email)

    def test_update_profile(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("profile")
        data = {"username": "updateduser"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "updateduser")
