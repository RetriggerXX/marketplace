import threading
import uuid
from datetime import timedelta

from django.core.mail import send_mail
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK
from rest_framework.views import APIView
from users.serializers import RegistrateSerializer, VerifyEmailSerializer

from users.models import User


class RegistrateView(APIView):
    def post(self, request):
        serializer = RegistrateSerializer(data = request.data)
        if serializer. is_valid():
            user = serializer.save()
            return Response({"message": "Пользователь успешно зарегистрирован."}, status= status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendVerificationLinkToUsersEmail(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        if user.role != "unverified":
            return Response({"error": "Пользователь уже верифицирован"}, status=status.HTTP_400_BAD_REQUEST)

        if user.verification_token_created and timezone.now() < user.verification_token_created + timedelta(hours=1):
            return Response({"error": "Код уже отправлен"}, status=status.HTTP_400_BAD_REQUEST)

        user.verification_token = uuid.uuid4()
        user.verification_token_created = timezone.now()
        user.save()

        verification_link = f"http://localhost:8000/verify-email/?token={user.verification_token}"

        def send_email():
            send_mail(
                subject="Код верификации",
                message=f"Перейдите по ссылке: {verification_link}",
                from_email="prostoodayn@gmail.com",
                recipient_list=[user.email]
            )

        threading.Thread(target=send_email).start()

        return Response({"message": "Код верификации отправлен на вашу почту"}, status=HTTP_200_OK)


class VerifyEmailView(APIView):
    def post(self, request):
        serializer = VerifyEmailSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        user = serializer.context["user"]
        user.role = "verified"
        user.verification_token = None
        user.verification_token_created = None
        user.save()

        return Response({"message": "Email успешно верифицирован"}, status=HTTP_200_OK)


