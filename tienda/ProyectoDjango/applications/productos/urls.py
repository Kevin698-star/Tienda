from django.urls import include, path
from . import views

urlpatterns = [
    # Ejemplo de ruta de prueba
    path('', views.home_view, name='home'),
    path('carrito/', include('applications.carrito.urls')),

  

]
