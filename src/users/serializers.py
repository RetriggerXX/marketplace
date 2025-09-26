from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers
from users.models import User

class RegistrateSerializer(serializers.ModelSerializer):

    class Meta():
        model = get_user_model()
        fields = ('email', 'username', 'password')


    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
        )

        return user


class VerifyEmailSerializer(serializers.Serializer):
    token = serializers.UUIDField()

    def validate_token(self, value):
        try:
            user = User.objects.get(verification_token=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("Неверный токен")

        if user.verification_token_created + timedelta(hours=1) < timezone.now():
            raise serializers.ValidationError("Срок действия токена истёк")

        self.context["user"] = user
        return value