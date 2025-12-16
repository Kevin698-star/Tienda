"""
Modelos para la aplicación de APIs.
Incluye modelos para almacenar productos sincronizados desde la API.
"""
from django.db import models
from django.utils import timezone

class ProductoAPI(models.Model):
    """
    Modelo para almacenar productos obtenidos de DummyJSON API.
    Este modelo representa la capa de MODELO en el patrón MVC.
    """
    api_id = models.IntegerField(unique=True, help_text="ID del producto en la API externa")
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    precio_usd = models.DecimalField(max_digits=10, decimal_places=2)
    precio_cop = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    categoria = models.CharField(max_length=100, blank=True)
    marca = models.CharField(max_length=100, blank=True)
    stock = models.IntegerField(default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    imagen_url = models.URLField(blank=True)
    
    # Metadatos
    sincronizado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'api_productos'
        verbose_name = 'Producto de API'
        verbose_name_plural = 'Productos de API'
        ordering = ['-sincronizado_en']
    
    def __str__(self):
        return f"{self.titulo} (${self.precio_usd})"
    
    def actualizar_precio_cop(self, tasa_cambio):
        """Actualiza el precio en COP según la tasa de cambio"""
        self.precio_cop = float(self.precio_usd) * tasa_cambio
        self.save()


class ConsultaAPI(models.Model):
    """
    Modelo para registrar consultas a las APIs en PostgreSQL.
    Complementa el historial almacenado en MongoDB.
    """
    TIPO_CHOICES = [
        ('PRODUCTO', 'Consulta de Productos'),
        ('CONVERSION', 'Conversión de Moneda'),
        ('BUSQUEDA', 'Búsqueda'),
    ]
    
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    api_nombre = models.CharField(max_length=100)
    fecha_consulta = models.DateTimeField(default=timezone.now)
    exitosa = models.BooleanField(default=True)
    detalles = models.TextField(blank=True)
    
    class Meta:
        db_table = 'api_consultas'
        verbose_name = 'Consulta de API'
        verbose_name_plural = 'Consultas de APIs'
        ordering = ['-fecha_consulta']
    
    def __str__(self):
        return f"{self.api_nombre} - {self.tipo} ({self.fecha_consulta})"
