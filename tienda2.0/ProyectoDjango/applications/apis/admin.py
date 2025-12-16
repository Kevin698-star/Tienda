"""
Administración de modelos para el panel de Django Admin.
"""
from django.contrib import admin
from .models import ProductoAPI, ConsultaAPI

@admin.register(ProductoAPI)
class ProductoAPIAdmin(admin.ModelAdmin):
    list_display = ['api_id', 'titulo', 'precio_usd', 'precio_cop', 'categoria', 'stock', 'activo', 'sincronizado_en']
    list_filter = ['activo', 'categoria', 'marca', 'sincronizado_en']
    search_fields = ['titulo', 'descripcion', 'categoria', 'marca']
    readonly_fields = ['api_id', 'sincronizado_en', 'actualizado_en']
    list_editable = ['activo']
    
    fieldsets = (
        ('Información de API', {
            'fields': ('api_id', 'titulo', 'descripcion')
        }),
        ('Precios', {
            'fields': ('precio_usd', 'precio_cop')
        }),
        ('Detalles', {
            'fields': ('categoria', 'marca', 'stock', 'rating', 'imagen_url')
        }),
        ('Estado', {
            'fields': ('activo', 'sincronizado_en', 'actualizado_en')
        }),
    )

@admin.register(ConsultaAPI)
class ConsultaAPIAdmin(admin.ModelAdmin):
    list_display = ['api_nombre', 'tipo', 'fecha_consulta', 'exitosa']
    list_filter = ['api_nombre', 'tipo', 'exitosa', 'fecha_consulta']
    search_fields = ['api_nombre', 'detalles']
    readonly_fields = ['fecha_consulta']
    date_hierarchy = 'fecha_consulta'
