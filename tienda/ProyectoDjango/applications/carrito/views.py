from django.shortcuts import get_object_or_404, redirect, render
from applications.productos.models import Producto
from .models import Carrito, ItemCarrito


def obtener_carrito(request):
    """
    Recupera el carrito actual usando la sesión del usuario.
    Si no existe, se crea uno nuevo y se asocia a la sesión.
    """
    carrito_id = request.session.get("carrito_id")
    if carrito_id:
        carrito = Carrito.objects.filter(id=carrito_id).first()
    else:
        carrito = Carrito.objects.create()
        request.session["carrito_id"] = carrito.id
    return carrito


def agregar_al_carrito(request):
    """
    Agrega un producto (local o de la API externa) al carrito.
    Si ya está en el carrito, incrementa su cantidad.
    """
    carrito = obtener_carrito(request)

    if request.method == "POST":
        tipo = request.POST.get("tipo")

        # --- Producto local ---
        if tipo == "local":
            producto_id = request.POST.get("producto_id")
            producto = get_object_or_404(Producto, id=producto_id)

        # --- Producto externo (API) ---
        elif tipo == "api":
            nombre = request.POST.get("nombre")
            precio = request.POST.get("precio")
            imagen = request.POST.get("imagen")

            # Crea o recupera el producto según el nombre
            producto, created = Producto.objects.get_or_create(
                nombre=nombre,
                defaults={
                    "precio": precio,
                    "descripcion": "Producto externo (API)",
                    "imagen_url": imagen,
                },
            )

            # Si ya existía pero no tiene imagen, se actualiza
            if not created and not producto.imagen_url and imagen:
                producto.imagen_url = imagen
                producto.save()

        # --- Agregar o actualizar el item en el carrito ---
        item, creado = ItemCarrito.objects.get_or_create(carrito=carrito, producto=producto)
        if not creado:
            item.cantidad += 1
            item.save()

        return redirect("ver_carrito")

    return redirect("tienda")


def ver_carrito(request):
    """
    Muestra el contenido del carrito actual.
    """
    carrito = obtener_carrito(request)
    return render(request, "carrito/ver_carrito.html", {"carrito": carrito})


def eliminar_del_carrito(request, item_id):
    """
    Elimina un producto del carrito.
    """
    item = get_object_or_404(ItemCarrito, id=item_id)
    item.delete()
    return redirect("ver_carrito")
