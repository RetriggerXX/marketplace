from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from products.models import Products
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import io

User = get_user_model()

def generate_test_image():
    file = io.BytesIO()
    image = Image.new("RGB", (100, 100), color="blue")
    image.save(file, "JPEG")
    file.seek(0)
    return SimpleUploadedFile("test_product.jpg", file.read(), content_type="image/jpeg")

class ProductApiTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.product1 = Products.objects.create(
            name="Продукт 1",
            description="Описание 1",
            price=100,
            image=generate_test_image()
        )
        self.product2 = Products.objects.create(
            name="Продукт 2",
            description="Описание 2",
            price=200,
            image=generate_test_image()
        )

    def test_list_products(self):
        url = reverse("products")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertIn("name", response.data[0])
        self.assertIn("price", response.data[0])
        self.assertIn("image", response.data[0])

    def test_search_products(self):
        url = reverse("products") + "?search=Продукт 1"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Продукт 1")

    def test_ordering_products_by_price(self):
        url = reverse("products") + "?ordering=price"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["price"], "100.00")

        url_desc = reverse("products") + "?ordering=-price"
        response_desc = self.client.get(url_desc)
        self.assertEqual(response_desc.data[0]["price"], "200.00")

    def test_product_detail(self):
        url = reverse("product_detail", args=[self.product1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.product1.name)
        self.assertEqual(response.data["description"], self.product1.description)
        self.assertIn("price", response.data)
        self.assertIn("image", response.data)

    def test_product_detail_not_found(self):
        url = reverse("product_detail", args=[9999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

