"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView, TokenVerifyView,
)

from users.views import RegistrateView, SendVerificationLinkToUsersEmail, GetProfile
from products.views import GetProduct, ProductDetailView
from admin_panel.views import AdminPanelProduct, AdminCreateProduct, AdminUpdateUserRole



urlpatterns = [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),


    #USERS_URLS
    path('register/', RegistrateView.as_view(), name='register'),
    path('verify/', SendVerificationLinkToUsersEmail.as_view(), name='verify'),
    path('profile/', GetProfile.as_view(), name='profile'),


    #TOKEN_URLS
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_refresh'),


    #PRODUCTS_URLS
    path('products/', GetProduct.as_view(), name='products'),
    path('products/<int:id>/', ProductDetailView.as_view(), name='product-detail'),


    #ADMIN_PANEL_URLS
    path('admin_panel/', AdminCreateProduct.as_view(), name='admin_panel'),
    path('admin_panel/<int:id>/', AdminPanelProduct.as_view(), name='admin_panel'),
    path('admin_panel/users/<int:id>/role/', AdminUpdateUserRole.as_view(), name='admin-update-user-role'),

]