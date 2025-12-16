"""
Vistas (Controladores) para la aplicación de APIs.
Implementa el patrón MVC:
- Modelo: ProductoAPI, ConsultaAPI, MongoDB
- Vista: Templates HTML
- Controlador: Este archivo (views.py)
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from bson import ObjectId

from .models import ProductoAPI, ConsultaAPI
from .services.dummyjson_service import DummyJSONService
from .services.exchangerate_service import ExchangeRateService


# ==================== VISTAS PRINCIPALES ====================

def dashboard_apis(request):
    """Vista principal del dashboard de APIs"""
    context = {
        'total_productos': ProductoAPI.objects.count(),
        'productos_activos': ProductoAPI.objects.filter(activo=True).count(),
        'total_consultas': ConsultaAPI.objects.count(),
        'ultimas_consultas': ConsultaAPI.objects.all()[:5],
    }
    return render(request, 'apis/dashboard.html', context)


# ==================== CRUD PRODUCTOS API ====================

def lista_productos_api(request):
    """Lista todos los productos sincronizados desde la API (READ)"""
    productos = ProductoAPI.objects.all()
    
    # Filtros
    categoria = request.GET.get('categoria')
    busqueda = request.GET.get('q')
    
    if categoria:
        productos = productos.filter(categoria__icontains=categoria)
    if busqueda:
        productos = productos.filter(titulo__icontains=busqueda)
    
    # Paginación
    paginator = Paginator(productos, 12)
    page = request.GET.get('page', 1)
    productos_paginados = paginator.get_page(page)
    
    # Obtener categorías únicas
    categorias = ProductoAPI.objects.values_list('categoria', flat=True).distinct()
    
    context = {
        'productos': productos_paginados,
        'categorias': categorias,
        'categoria_actual': categoria,
        'busqueda': busqueda,
    }
    return render(request, 'apis/productos_lista.html', context)


def detalle_producto_api(request, producto_id):
    """Muestra el detalle de un producto (READ)"""
    producto = get_object_or_404(ProductoAPI, id=producto_id)
    
    # Actualizar precio COP con tasa actual
    tasas = ExchangeRateService.obtener_tasa_cambio()
    if tasas:
        producto.actualizar_precio_cop(tasas['tasa_cop'])
    
    context = {
        'producto': producto,
        'tasa_cambio': tasas.get('tasa_cop') if tasas else None,
    }
    return render(request, 'apis/producto_detalle.html', context)


@require_http_methods(["POST"])
def sincronizar_productos(request):
    """Sincroniza productos desde DummyJSON API (CREATE/UPDATE)"""
    try:
        # Obtener productos de la API
        productos = DummyJSONService.obtener_productos(limit=30)
        
        # Obtener tasa de cambio
        tasas = ExchangeRateService.obtener_tasa_cambio()
        tasa_cop = tasas.get('tasa_cop', 4000) if tasas else 4000
        
        sincronizados = 0
        actualizados = 0
        
        for prod_data in productos:
            # Convertir precio a COP
            precio_cop = float(prod_data.get('price', 0)) * tasa_cop
            
            # Crear o actualizar producto
            producto, created = ProductoAPI.objects.update_or_create(
                api_id=prod_data.get('id'),
                defaults={
                    'titulo': prod_data.get('title', ''),
                    'descripcion': prod_data.get('description', ''),
                    'precio_usd': prod_data.get('price', 0),
                    'precio_cop': precio_cop,
                    'categoria': prod_data.get('category', ''),
                    'marca': prod_data.get('brand', ''),
                    'stock': prod_data.get('stock', 0),
                    'rating': prod_data.get('rating', 0),
                    'imagen_url': prod_data.get('thumbnail', ''),
                    'activo': True,
                }
            )
            
            if created:
                sincronizados += 1
            else:
                actualizados += 1
        
        # Registrar consulta
        ConsultaAPI.objects.create(
            tipo='PRODUCTO',
            api_nombre='DummyJSON',
            exitosa=True,
            detalles=f'Sincronizados: {sincronizados}, Actualizados: {actualizados}'
        )
        
        messages.success(request, f'✓ {sincronizados} productos nuevos sincronizados, {actualizados} actualizados.')
        
    except Exception as e:
        ConsultaAPI.objects.create(
            tipo='PRODUCTO',
            api_nombre='DummyJSON',
            exitosa=False,
            detalles=str(e)
        )
        messages.error(request, f'Error al sincronizar: {str(e)}')
    
    return redirect('apis:lista_productos')


@require_http_methods(["POST"])
def eliminar_producto_api(request, producto_id):
    """Elimina un producto (DELETE)"""
    producto = get_object_or_404(ProductoAPI, id=producto_id)
    titulo = producto.titulo
    producto.delete()
    messages.success(request, f'Producto "{titulo}" eliminado correctamente.')
    return redirect('apis:lista_productos')


@require_http_methods(["POST"])
def actualizar_precios_cop(request):
    """Actualiza todos los precios a COP con la tasa actual (UPDATE)"""
    try:
        tasas = ExchangeRateService.obtener_tasa_cambio()
        if not tasas:
            messages.error(request, 'No se pudo obtener la tasa de cambio.')
            return redirect('apis:lista_productos')
        
        tasa_cop = tasas['tasa_cop']
        productos = ProductoAPI.objects.all()
        
        for producto in productos:
            producto.actualizar_precio_cop(tasa_cop)
        
        ConsultaAPI.objects.create(
            tipo='CONVERSION',
            api_nombre='ExchangeRate',
            exitosa=True,
            detalles=f'Actualizados {productos.count()} productos con tasa {tasa_cop}'
        )
        
        messages.success(request, f'✓ Precios actualizados. Tasa: 1 USD = {tasa_cop:.2f} COP')
        
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
    
    return redirect('apis:lista_productos')


# ==================== BÚSQUEDA EN API ====================

def buscar_en_api(request):
    """Busca productos directamente en la API de DummyJSON"""
    query = request.GET.get('q', '')
    productos_api = []
    
    if query:
        productos_api = DummyJSONService.buscar_productos(query)
        
        # Convertir precios a COP
        tasas = ExchangeRateService.obtener_tasa_cambio()
        if tasas:
            tasa_cop = tasas['tasa_cop']
            for prod in productos_api:
                prod['precio_cop'] = float(prod.get('price', 0)) * tasa_cop
        
        ConsultaAPI.objects.create(
            tipo='BUSQUEDA',
            api_nombre='DummyJSON',
            exitosa=True,
            detalles=f'Búsqueda: {query}, Resultados: {len(productos_api)}'
        )
    
    context = {
        'query': query,
        'productos': productos_api,
    }
    return render(request, 'apis/busqueda.html', context)


# ==================== HISTORIAL MONGODB ====================

def historial_consultas(request):
    """Muestra el historial de consultas desde MongoDB"""
    historial_dummy = DummyJSONService.obtener_historial(limit=20)
    historial_exchange = ExchangeRateService.obtener_historial(limit=20)
    
    # Convertir ObjectId a string para el template
    for item in historial_dummy:
        if '_id' in item and isinstance(item['_id'], ObjectId):
            item['_id'] = str(item['_id'])
    
    for item in historial_exchange:
        if '_id' in item and isinstance(item['_id'], ObjectId):
            item['_id'] = str(item['_id'])
    
    context = {
        'historial_dummy': historial_dummy,
        'historial_exchange': historial_exchange,
    }
    return render(request, 'apis/historial.html', context)


# ==================== API REST (JSON) ====================

def api_tasas_cambio(request):
    """Endpoint JSON para obtener tasas de cambio"""
    tasas = ExchangeRateService.obtener_tasa_cambio()
    if tasas:
        return JsonResponse(tasas, safe=False)
    return JsonResponse({'error': 'No se pudo obtener tasas'}, status=500)


def api_productos_json(request):
    """Endpoint JSON para listar productos"""
    productos = ProductoAPI.objects.filter(activo=True)[:20]
    data = []
    
    for prod in productos:
        data.append({
            'id': prod.id,
            'api_id': prod.api_id,
            'titulo': prod.titulo,
            'precio_usd': float(prod.precio_usd),
            'precio_cop': float(prod.precio_cop) if prod.precio_cop else None,
            'categoria': prod.categoria,
            'stock': prod.stock,
            'imagen': prod.imagen_url,
        })
    
    return JsonResponse(data, safe=False)


def proxy_imagen(request):
    """Proxy para cargar imágenes externas y evitar problemas de CORS"""
    import requests
    from django.http import HttpResponse
    
    url = request.GET.get('url')
    if not url:
        return HttpResponse('URL no proporcionada', status=400)
    
    try:
        response = requests.get(url, timeout=10)
        return HttpResponse(response.content, content_type=response.headers.get('content-type', 'image/jpeg'))
    except Exception as e:
        # Devolver imagen placeholder si falla
        return redirect('https://placehold.co/300x200/667eea/white?text=Error')
