from django.db import models

class Producto(models.Model):
    """
    Representa un producto disponible en la tienda.
    Puede provenir tanto de la base de datos local como de una fuente externa (API).
    """
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    imagen_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.nombre

    @property
    def imagen_mostrar(self):
        """
        Retorna la imagen del producto.
        Si tiene una imagen local, la usa.
        En caso contrario, intenta mostrar la imagen externa.
        Si no existe ninguna, muestra una imagen por defecto.
        """
        if self.imagen:
            return self.imagen.url
        elif self.imagen_url:
            return self.imagen_url
        return "/static/img/placeholder.png"
