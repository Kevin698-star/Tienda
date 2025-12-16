from django.db import models
from django.conf import settings
from applications.productos.models import Producto


class Carrito(models.Model):
    """
    Representa el carrito de compras asociado a un usuario o a una sesión anónima.
    """
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='carritos',
        null=True,
        blank=True
    )
    creado_en = models.DateTimeField(auto_now_add=True)

    def total(self):
        """
        Calcula el total del carrito sumando los subtotales de cada producto.
        """
        return sum(item.subtotal() for item in self.items.all())

    def __str__(self):
        return f"Carrito #{self.id}"


class ItemCarrito(models.Model):
    """
    Representa un producto dentro del carrito, junto con su cantidad.
    """
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def subtotal(self):
        """
        Devuelve el valor total de este producto en el carrito.
        """
        return self.producto.precio * self.cantidad

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"
