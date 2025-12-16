from django.shortcuts import render
from .models import Producto
from .services.api_dummyjson import obtener_productos_api

def home_view(request):
    """
    Página principal
    """
    return render(request, "home.html")

def tienda_view(request):
    """
    Controlador que orquesta:
    - Productos locales (BD)
    - Productos externos (API)
    """
    query = request.GET.get("q", "").strip()

    # Productos locales
    if query:
        productos_locales = Producto.objects.filter(nombre__icontains=query)
    else:
        productos_locales = Producto.objects.all()

    # Productos desde API externa
    productos_api = obtener_productos_api()

    context = {
        "productos_locales": productos_locales,
        "productos_api": productos_api,
        "query": query,
    }

    return render(request, "productos/tienda.html", context)
