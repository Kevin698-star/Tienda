"""
URLs para la aplicación de APIs.
"""
from django.urls import path
from . import views

app_name = 'apis'

urlpatterns = [
    # Dashboard
    path('', views.dashboard_apis, name='dashboard'),
    
    # CRUD Productos API
    path('productos/', views.lista_productos_api, name='lista_productos'),
    path('productos/<int:producto_id>/', views.detalle_producto_api, name='detalle_producto'),
    path('productos/sincronizar/', views.sincronizar_productos, name='sincronizar_productos'),
    path('productos/<int:producto_id>/eliminar/', views.eliminar_producto_api, name='eliminar_producto'),
    path('productos/actualizar-precios/', views.actualizar_precios_cop, name='actualizar_precios'),
    
    # Búsqueda
    path('buscar/', views.buscar_en_api, name='buscar'),
    
    # Historial MongoDB
    path('historial/', views.historial_consultas, name='historial'),
    
    # API REST (JSON)
    path('api/tasas/', views.api_tasas_cambio, name='api_tasas'),
    path('api/productos/', views.api_productos_json, name='api_productos'),
    
    # Proxy de imágenes
    path('proxy-imagen/', views.proxy_imagen, name='proxy_imagen'),
]
