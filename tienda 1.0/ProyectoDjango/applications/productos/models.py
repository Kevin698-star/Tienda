from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    imagen_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.nombre

    @property
    def imagen_mostrar(self):
        if self.imagen:
            return self.imagen.url
        elif self.imagen_url:
            return self.imagen_url
        return "/static/img/placeholder.png"
