"""
Servicio para consumir API de ExchangeRate (conversión de monedas).
API 2: Convierte precios de USD a COP (pesos colombianos).
"""
import requests
from datetime import datetime
from ..db.mongodb import mongo_db

API_URL = "https://api.exchangerate-api.com/v4/latest/USD"

class ExchangeRateService:
    """Servicio para conversión de monedas"""
    
    @staticmethod
    def obtener_tasa_cambio():
        """
        Obtiene la tasa de cambio de USD a COP.
        Almacena el historial en MongoDB.
        """
        try:
            response = requests.get(API_URL, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            tasa_cop = data.get('rates', {}).get('COP', 0)
            
            # Guardar en MongoDB
            ExchangeRateService._guardar_historial({
                "tipo": "obtener_tasa_cambio",
                "fecha": datetime.now(),
                "tasa_usd_cop": tasa_cop,
                "exitoso": True,
                "todas_tasas": data.get('rates', {})
            })
            
            return {
                "tasa_cop": tasa_cop,
                "base": data.get('base'),
                "fecha": data.get('date'),
                "todas_tasas": data.get('rates', {})
            }
        except requests.RequestException as e:
            ExchangeRateService._guardar_historial({
                "tipo": "obtener_tasa_cambio",
                "fecha": datetime.now(),
                "exitoso": False,
                "error": str(e)
            })
            return None
    
    @staticmethod
    def convertir_usd_a_cop(monto_usd):
        """Convierte un monto de USD a COP"""
        try:
            tasas = ExchangeRateService.obtener_tasa_cambio()
            if tasas and tasas.get('tasa_cop'):
                tasa_cop = tasas['tasa_cop']
                monto_cop = float(monto_usd) * tasa_cop
                
                ExchangeRateService._guardar_historial({
                    "tipo": "conversion",
                    "fecha": datetime.now(),
                    "monto_usd": monto_usd,
                    "monto_cop": monto_cop,
                    "tasa_usada": tasa_cop,
                    "exitoso": True
                })
                
                return {
                    "monto_usd": monto_usd,
                    "monto_cop": round(monto_cop, 2),
                    "tasa": tasa_cop
                }
            return None
        except Exception as e:
            ExchangeRateService._guardar_historial({
                "tipo": "conversion",
                "fecha": datetime.now(),
                "monto_usd": monto_usd,
                "exitoso": False,
                "error": str(e)
            })
            return None
    
    @staticmethod
    def convertir_precio_producto(producto):
        """Convierte el precio de un producto de USD a COP"""
        if 'price' in producto:
            conversion = ExchangeRateService.convertir_usd_a_cop(producto['price'])
            if conversion:
                producto['precio_cop'] = conversion['monto_cop']
                producto['tasa_cambio'] = conversion['tasa']
        return producto
    
    @staticmethod
    def _guardar_historial(datos):
        """Guarda el historial de conversiones en MongoDB"""
        try:
            collection = mongo_db.get_collection('historial_exchangerate')
            collection.insert_one(datos)
        except Exception as e:
            print(f"Error al guardar en MongoDB: {e}")
    
    @staticmethod
    def obtener_historial(limit=50):
        """Obtiene el historial de conversiones desde MongoDB"""
        try:
            collection = mongo_db.get_collection('historial_exchangerate')
            historial = list(collection.find().sort("fecha", -1).limit(limit))
            return historial
        except Exception as e:
            print(f"Error al obtener historial: {e}")
            return []
