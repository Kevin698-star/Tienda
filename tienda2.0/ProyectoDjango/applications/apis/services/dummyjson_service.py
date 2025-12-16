"""
Servicio para consumir API de DummyJSON (productos).
API 1: Obtiene datos de productos de prueba.
"""
import requests
from datetime import datetime
from ..db.mongodb import mongo_db

API_URL = "https://dummyjson.com/products"

class DummyJSONService:
    """Servicio para interactuar con la API de DummyJSON"""
    
    @staticmethod
    def obtener_productos(limit=30):
        """
        Consume la API externa DummyJSON para obtener productos.
        Almacena el historial de consultas en MongoDB.
        """
        try:
            response = requests.get(f"{API_URL}?limit={limit}", timeout=10)
            response.raise_for_status()
            data = response.json()
            productos = data.get("products", [])
            
            # Guardar en MongoDB el historial de consulta
            DummyJSONService._guardar_historial({
                "tipo": "obtener_productos",
                "fecha": datetime.now(),
                "cantidad": len(productos),
                "exitoso": True,
                "datos": productos[:5]  # Guardar solo los primeros 5 como muestra
            })
            
            return productos
        except requests.RequestException as e:
            DummyJSONService._guardar_historial({
                "tipo": "obtener_productos",
                "fecha": datetime.now(),
                "cantidad": 0,
                "exitoso": False,
                "error": str(e)
            })
            return []
    
    @staticmethod
    def obtener_producto_por_id(producto_id):
        """Obtiene un producto específico por ID"""
        try:
            response = requests.get(f"{API_URL}/{producto_id}", timeout=10)
            response.raise_for_status()
            producto = response.json()
            
            DummyJSONService._guardar_historial({
                "tipo": "obtener_producto_por_id",
                "producto_id": producto_id,
                "fecha": datetime.now(),
                "exitoso": True,
                "datos": producto
            })
            
            return producto
        except requests.RequestException as e:
            DummyJSONService._guardar_historial({
                "tipo": "obtener_producto_por_id",
                "producto_id": producto_id,
                "fecha": datetime.now(),
                "exitoso": False,
                "error": str(e)
            })
            return None
    
    @staticmethod
    def buscar_productos(query):
        """Busca productos por nombre"""
        try:
            response = requests.get(f"{API_URL}/search?q={query}", timeout=10)
            response.raise_for_status()
            data = response.json()
            productos = data.get("products", [])
            
            DummyJSONService._guardar_historial({
                "tipo": "buscar_productos",
                "query": query,
                "fecha": datetime.now(),
                "cantidad": len(productos),
                "exitoso": True
            })
            
            return productos
        except requests.RequestException as e:
            DummyJSONService._guardar_historial({
                "tipo": "buscar_productos",
                "query": query,
                "fecha": datetime.now(),
                "exitoso": False,
                "error": str(e)
            })
            return []
    
    @staticmethod
    def _guardar_historial(datos):
        """Guarda el historial de consultas en MongoDB"""
        try:
            collection = mongo_db.get_collection('historial_dummyjson')
            collection.insert_one(datos)
        except Exception as e:
            print(f"Error al guardar en MongoDB: {e}")
    
    @staticmethod
    def obtener_historial(limit=50):
        """Obtiene el historial de consultas desde MongoDB"""
        try:
            collection = mongo_db.get_collection('historial_dummyjson')
            historial = list(collection.find().sort("fecha", -1).limit(limit))
            return historial
        except Exception as e:
            print(f"Error al obtener historial: {e}")
            return []
