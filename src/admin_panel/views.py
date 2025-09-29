from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from admin_panel.serializers import CreateProductSerializer

from products.models import Products

from users.permissions import IsSuperAdmin, IsAdmin

from users.models import User

from admin_panel.serializers import UpdateUserRoleSerializer


# Create your views here.
class AdminCreateProduct(APIView):
    permission_classes = [IsSuperAdmin | IsAdmin]

    def post(self, request):
        serializer = CreateProductSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Продукт создан."}, status= status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class AdminPanelProduct(APIView):
    permission_classes = [IsSuperAdmin | IsAdmin]

    def put(self, request, id):
        product = get_object_or_404(Products, id=id)
        serializer = CreateProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Продукт обновлён"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def patch(self, request, id):
        product = get_object_or_404(Products, id=id)
        serializer = CreateProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Продукт обновлён"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, id):
        product = get_object_or_404(Products, id=id)
        product.delete()
        return Response({"message": "Продукт удален"}, status=status.HTTP_204_NO_CONTENT)

    def get(self, request, id):
        product = get_object_or_404(Products, id=id)
        serializer = CreateProductSerializer(product)
        return Response(serializer.data)

class AdminUpdateUserRole(APIView):
    permission_classes = [IsSuperAdmin]

    def patch(self, request, id):
        user = get_object_or_404(User, id=id)
        serializer = UpdateUserRoleSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": f"Роль пользователя обновлена на {serializer.data['role']}"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)









