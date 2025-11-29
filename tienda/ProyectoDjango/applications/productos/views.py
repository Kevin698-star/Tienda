from django.shortcuts import render, get_object_or_404, redirect
from applications.carrito.models import Carrito, ItemCarrito
from .models import Producto
import requests


def home_view(request):
    """
    Vista principal del sitio. Muestra la página de inicio.
    """
    return render(request, "home.html")


def tienda_view(request):
    """
    Muestra el catálogo de productos disponibles:
    - Productos locales almacenados en la base de datos.
    - Productos extern--os obtenidos desde la API pública DummyJSON.

    Permite realizar búsquedas por nombre o título dentro de ambos tipos de productos.
    """
    query = request.GET.get("q", "")

    # Productos registrados localmente en la base de datos
    productos_locales = Producto.objects.all()
    if query:
        productos_locales = productos_locales.filter(nombre__icontains=query)

    # Consulta de productos desde la API externa
    url = "https://dummyjson.com/products?limit=50"
    response = requests.get(url)
    productos_api = []

    if response.status_code == 200:
        data = response.json()
        productos_api = data.get("products", [])
        if query:
            productos_api = [
                p for p in productos_api if query.lower() in p["title"].lower()
            ]

    context = {
        "productos_locales": productos_locales,
        "productos_api": productos_api,
        "query": query,
    }

    return render(request, "productos/tienda.html", context)
