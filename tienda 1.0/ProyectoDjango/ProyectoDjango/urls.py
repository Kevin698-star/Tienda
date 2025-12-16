from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path

from rest_framework import routers
from applications.productos.api import ProductoViewSet
from applications.productos.views import home_view, tienda_view
router = routers.DefaultRouter()
router.register('productos', ProductoViewSet)

urlpatterns = [
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('tienda/', tienda_view, name='tienda'),
    re_path('carrito/', include('applications.carrito.urls')),
 
    path("", include("applications.productos.urls")),





    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
