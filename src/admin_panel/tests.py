import io

from PIL import Image
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from products.models import Products


# Create your tests here.
User = get_user_model()
def generate_test_image():
    file = io.BytesIO()
    image = Image.new("RGB", (100, 100), color="red")
    image.save(file, "JPEG")
    file.seek(0)
    return SimpleUploadedFile("test.jpg", file.read(), content_type="image/jpeg")


class AdminApiTests(APITestCase):
    def setUp(self):
        self.superadmin = User.objects.create_user(
            email="superadmin@test.com",
            username="superadmin",
            password="pass1234",
            role="superadmin"
        )
        self.admin = User.objects.create_user(
            email="admin@test.com",
            username="admin",
            password="pass1234",
            role="admin"
        )
        self.user = User.objects.create_user(
            email="user@test.com",
            username="user",
            password="pass1234",
            role="verified"
        )

        self.client = APIClient()

        self.product = Products.objects.create(
            name="Тестовый продукт",
            description="Описание",
            price=100,
            image="test.jpg"
    )

    def authenticate_as(self, user):
        self.client.force_authenticate(user=user)

    # --- CREATE PRODUCT ---
    def test_create_product_superadmin(self):
        self.authenticate_as(self.superadmin)
        url = reverse("admin_create_product")
        image = generate_test_image()
        data = {"name": "Новый продукт", "description": "Описание", "price": 500, "image": image}
        response = self.client.post(url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Products.objects.filter(name="Новый продукт").exists())

    def test_create_product_no_permission(self):
        self.authenticate_as(self.user)
        url = reverse("admin_create_product")
        image = generate_test_image()
        data = {"name": "Fail продукт", "description": "Описание", "price": 200, "image": image}
        response = self.client.post(url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # --- GET PRODUCT ---
    def test_get_product(self):
        self.authenticate_as(self.admin)
        url = reverse("admin_panel", args=[self.product.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.product.name)

    # --- UPDATE PRODUCT ---
    def test_update_product_put(self):
        self.authenticate_as(self.admin)
        url = reverse("admin_panel", args=[self.product.id])
        image = generate_test_image()
        data = {"name": "Обновленный продукт", "description": "Новое описание", "price": 150, "image": image}
        response = self.client.put(url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, "Обновленный продукт")

    def test_partial_update_patch(self):
        self.authenticate_as(self.admin)
        url = reverse("admin_panel", args=[self.product.id])
        data = {"price": 777}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.price, 777)

    # --- DELETE PRODUCT ---
    def test_delete_product(self):
        self.authenticate_as(self.admin)
        url = reverse("admin_panel", args=[self.product.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Products.objects.filter(id=self.product.id).exists())

    # --- UPDATE USER ROLE ---
    def test_update_user_role_superadmin(self):
        self.authenticate_as(self.superadmin)
        url = reverse("admin_update_user_role", args=[self.user.id])
        response = self.client.patch(url, {"role": "admin"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.role, "admin")

    def test_update_user_role_invalid(self):
        self.authenticate_as(self.superadmin)
        url = reverse("admin_update_user_role", args=[self.user.id])
        response = self.client.patch(url, {"role": "invalid_role"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_user_role_no_permission(self):
        self.authenticate_as(self.admin)
        url = reverse("admin_update_user_role", args=[self.user.id])
        response = self.client.patch(url, {"role": "admin"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
