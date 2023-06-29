from django.contrib import admin
from django.urls import path,re_path,include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.conf.urls import handler404
from django.http import JsonResponse
from apps.users.views import VistaMainJson

urlpatterns = [
    path('', VistaMainJson.as_view(), name='ruta_principal'),
    path('admin/', admin.site.urls),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    re_path('', include('apps.users.urls')),
    re_path('', include('apps.product.urls')),
    re_path('variations/',include('apps.product.routers')),
    re_path('', include('apps.tienda.urls')),
    re_path('', include('apps.order.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

