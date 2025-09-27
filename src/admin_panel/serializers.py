from products.models import Products
from rest_framework import serializers

from users.models import User


class CreateProductSerializer(serializers.ModelSerializer):


    class Meta():
        model = Products
        fields = ('name', 'description', 'price', 'image')


    def create(self, validated_data):
        product = Products.objects.create(
            name=validated_data['name'],
            description=validated_data['description'],
            price=validated_data['price'],
            image=validated_data['image']
        )

        return product


class UpdateUserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['role']

    VALID_ROLES = ['unverified', 'verified', 'admin', 'superadmin']

    def validate_role(self, value):
        if value not in self.VALID_ROLES:
            raise serializers.ValidationError(f"Недопустимая роль: {value}. Допустимые: {', '.join(self.VALID_ROLES)}")
        return value