from rest_framework import serializers
from products.models import Products


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ["name", "price", "image"]


class ProductDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ["name", "price", "image", "description"]