from decimal import Decimal
from django.shortcuts import get_object_or_404, redirect, render
from applications.productos.models import Producto
from .models import Carrito, ItemCarrito


def obtener_carrito(request):
    carrito_id = request.session.get("carrito_id")
    if carrito_id:
        carrito = Carrito.objects.filter(id=carrito_id).first()
    else:
        carrito = Carrito.objects.create()
        request.session["carrito_id"] = carrito.id
    return carrito


def agregar_al_carrito(request):
    carrito = obtener_carrito(request)

    if request.method == "POST":
        tipo = request.POST.get("tipo")

        if tipo == "local":
            producto_id = request.POST.get("producto_id")
            producto = get_object_or_404(Producto, id=producto_id)

        elif tipo == "api":
            nombre = request.POST.get("nombre")
            precio = Decimal(request.POST.get("precio", "0"))
            imagen = request.POST.get("imagen")

            if not nombre or nombre.strip() == "":
                nombre = "Producto externo"

            producto, created = Producto.objects.get_or_create(
                nombre=nombre,
                defaults={
                    "precio": precio,
                    "descripcion": "Producto externo (API)",
                    "imagen_url": imagen,
                },
            )

            if not created and not producto.imagen_url and imagen:
                producto.imagen_url = imagen
                producto.save()

        else:
            return redirect("tienda")

        item, creado = ItemCarrito.objects.get_or_create(
            carrito=carrito, producto=producto
        )
        if not creado:
            item.cantidad += 1
            item.save()

        return redirect("ver_carrito")

    return redirect("tienda")


def ver_carrito(request):
    carrito = obtener_carrito(request)
    return render(request, "carrito/ver_carrito.html", {"carrito": carrito})


def eliminar_del_carrito(request, item_id):
    item = get_object_or_404(ItemCarrito, id=item_id)
    item.delete()
    return redirect("ver_carrito")