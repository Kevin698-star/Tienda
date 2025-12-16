#!/usr/bin/env python
"""
Script de prueba para verificar la integración de APIs.
Ejecuta pruebas básicas de las funcionalidades implementadas.
"""
import os
import sys
import django

# Configurar Django
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'ProyectoDjango'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ProyectoDjango.settings.local')
django.setup()

from applications.apis.services.dummyjson_service import DummyJSONService
from applications.apis.services.exchangerate_service import ExchangeRateService
from applications.apis.models import ProductoAPI, ConsultaAPI

def prueba_1_obtener_productos():
    """Prueba 1: Obtener productos de DummyJSON API"""
    print("\n" + "="*60)
    print("PRUEBA 1: Obtener productos de DummyJSON API")
    print("="*60)
    
    productos = DummyJSONService.obtener_productos(limit=5)
    
    if productos:
        print(f"✓ Éxito: Se obtuvieron {len(productos)} productos")
        print(f"  Ejemplo: {productos[0]['title']} - ${productos[0]['price']}")
    else:
        print("✗ Error: No se pudieron obtener productos")
    
    return len(productos) > 0

def prueba_2_conversion_moneda():
    """Prueba 2: Conversión de USD a COP"""
    print("\n" + "="*60)
    print("PRUEBA 2: Conversión de moneda USD a COP")
    print("="*60)
    
    tasas = ExchangeRateService.obtener_tasa_cambio()
    
    if tasas:
        print(f"✓ Éxito: Tasa obtenida")
        print(f"  1 USD = {tasas['tasa_cop']:.2f} COP")
        
        # Probar conversión
        conversion = ExchangeRateService.convertir_usd_a_cop(100)
        if conversion:
            print(f"  Conversión: $100 USD = ${conversion['monto_cop']:.2f} COP")
    else:
        print("✗ Error: No se pudo obtener la tasa de cambio")
    
    return tasas is not None

def prueba_3_sincronizar_base_datos():
    """Prueba 3: Sincronizar productos en base de datos"""
    print("\n" + "="*60)
    print("PRUEBA 3: Sincronizar productos en PostgreSQL")
    print("="*60)
    
    # Obtener productos de API
    productos = DummyJSONService.obtener_productos(limit=3)
    tasas = ExchangeRateService.obtener_tasa_cambio()
    
    if not productos or not tasas:
        print("✗ Error: No se pudieron obtener datos de las APIs")
        return False
    
    tasa_cop = tasas['tasa_cop']
    sincronizados = 0
    
    for prod_data in productos:
        precio_cop = float(prod_data['price']) * tasa_cop
        
        producto, created = ProductoAPI.objects.update_or_create(
            api_id=prod_data['id'],
            defaults={
                'titulo': prod_data['title'],
                'descripcion': prod_data['description'],
                'precio_usd': prod_data['price'],
                'precio_cop': precio_cop,
                'categoria': prod_data['category'],
                'marca': prod_data.get('brand', ''),
                'stock': prod_data['stock'],
                'rating': prod_data.get('rating', 0),
                'imagen_url': prod_data.get('thumbnail', ''),
                'activo': True,
            }
        )
        
        if created:
            sincronizados += 1
    
    total_productos = ProductoAPI.objects.count()
    print(f"✓ Éxito: {sincronizados} productos nuevos sincronizados")
    print(f"  Total en BD: {total_productos} productos")
    
    return True

def prueba_4_busqueda():
    """Prueba 4: Búsqueda en API"""
    print("\n" + "="*60)
    print("PRUEBA 4: Búsqueda de productos en API")
    print("="*60)
    
    resultados = DummyJSONService.buscar_productos("phone")
    
    if resultados:
        print(f"✓ Éxito: Se encontraron {len(resultados)} resultados para 'phone'")
        if resultados:
            print(f"  Ejemplo: {resultados[0]['title']}")
    else:
        print("✗ Error: No se encontraron resultados")
    
    return len(resultados) > 0

def prueba_5_historial_mongodb():
    """Prueba 5: Verificar historial en MongoDB"""
    print("\n" + "="*60)
    print("PRUEBA 5: Historial en MongoDB")
    print("="*60)
    
    historial_dummy = DummyJSONService.obtener_historial(limit=3)
    historial_exchange = ExchangeRateService.obtener_historial(limit=3)
    
    print(f"✓ Historial DummyJSON: {len(historial_dummy)} registros")
    print(f"✓ Historial ExchangeRate: {len(historial_exchange)} registros")
    
    return True

def prueba_6_consultas_postgresql():
    """Prueba 6: Verificar consultas en PostgreSQL"""
    print("\n" + "="*60)
    print("PRUEBA 6: Consultas registradas en PostgreSQL")
    print("="*60)
    
    total_consultas = ConsultaAPI.objects.count()
    consultas_exitosas = ConsultaAPI.objects.filter(exitosa=True).count()
    
    print(f"✓ Total de consultas: {total_consultas}")
    print(f"✓ Consultas exitosas: {consultas_exitosas}")
    
    return True

def main():
    """Ejecuta todas las pruebas"""
    print("\n" + "#"*60)
    print("# PRUEBAS DE INTEGRACIÓN DE APIs")
    print("#"*60)
    
    pruebas = [
        prueba_1_obtener_productos,
        prueba_2_conversion_moneda,
        prueba_3_sincronizar_base_datos,
        prueba_4_busqueda,
        prueba_5_historial_mongodb,
        prueba_6_consultas_postgresql,
    ]
    
    resultados = []
    
    for prueba in pruebas:
        try:
            resultado = prueba()
            resultados.append(resultado)
        except Exception as e:
            print(f"\n✗ Error en {prueba.__name__}: {str(e)}")
            resultados.append(False)
    
    # Resumen
    print("\n" + "="*60)
    print("RESUMEN DE PRUEBAS")
    print("="*60)
    exitosas = sum(resultados)
    total = len(resultados)
    print(f"Pruebas exitosas: {exitosas}/{total}")
    print(f"Tasa de éxito: {(exitosas/total)*100:.1f}%")
    
    if exitosas == total:
        print("\n✓ ¡Todas las pruebas pasaron exitosamente!")
    else:
        print(f"\n⚠ {total - exitosas} prueba(s) fallaron")
    
    print("\n" + "="*60)
    print("URLs del sistema:")
    print("  Dashboard: http://127.0.0.1:8000/apis/")
    print("  Productos: http://127.0.0.1:8000/apis/productos/")
    print("  Búsqueda:  http://127.0.0.1:8000/apis/buscar/")
    print("  Historial: http://127.0.0.1:8000/apis/historial/")
    print("="*60)

if __name__ == '__main__':
    main()
