import requests

API_URL = "https://dummyjson.com/products"

def obtener_productos_api():
    """
    Consume la API externa DummyJSON
    """
    try:
        response = requests.get(API_URL, timeout=5)
        response.raise_for_status()
        data = response.json()
        return data.get("products", [])
    except requests.RequestException:
        return []
