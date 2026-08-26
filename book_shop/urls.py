"""
URL configuration for book_shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.conf import settings
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from shop.views import custom_404_view
from shop.api import BookViewSet, CategoryViewSet
from order.api import OrderViewSet, CartViewSet
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

router = routers.DefaultRouter()
router.register(r'books', BookViewSet, basename='api-books')
router.register(r'categories', CategoryViewSet, basename='api-categories')
router.register(r'orders', OrderViewSet, basename='api-orders')
router.register(r'carts', CartViewSet, basename='api-carts')

handler404 = custom_404_view

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('shop.urls')),
    path('users/', include('user_management.urls')),

    path('accounts/', include('allauth.urls')),
    path('order/', include('order.urls')),

    path('i18n/', include('django.conf.urls.i18n')),

    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),

    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
