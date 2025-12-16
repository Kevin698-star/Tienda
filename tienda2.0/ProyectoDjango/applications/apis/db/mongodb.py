"""
Configuración de MongoDB para almacenar datos no relacionales.
Este módulo maneja la conexión a MongoDB.
"""
from pymongo import MongoClient
from django.conf import settings

class MongoDBConnection:
    """Singleton para conexión a MongoDB"""
    _instance = None
    _client = None
    _db = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoDBConnection, cls).__new__(cls)
        return cls._instance
    
    def connect(self):
        """Establece la conexión con MongoDB"""
        if self._client is None:
            # Conexión a MongoDB local
            self._client = MongoClient('mongodb://localhost:27017/')
            self._db = self._client['tienda_apis_db']
        return self._db
    
    def get_collection(self, collection_name):
        """Obtiene una colección específica"""
        db = self.connect()
        return db[collection_name]
    
    def close(self):
        """Cierra la conexión"""
        if self._client:
            self._client.close()
            self._client = None
            self._db = None

# Instancia global
mongo_db = MongoDBConnection()
