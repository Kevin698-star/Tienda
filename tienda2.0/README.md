# 🚀 Sistema de Integración de APIs - Proyecto Django

## 📋 Descripción

Proyecto Django que integra dos APIs públicas siguiendo el patrón **MVC (Modelo-Vista-Controlador)** con bases de datos relacionales (PostgreSQL) y no relacionales (MongoDB).

### 🎯 APIs Utilizadas

#### 1. **DummyJSON API** - Gestión de Productos
- **URL**: https://dummyjson.com/products
- **Propósito**: Obtener catálogo de productos de prueba con información detallada
- **Funcionalidades**:
  - Sincronización de productos
  - Búsqueda en tiempo real
  - Almacenamiento en PostgreSQL
  - Historial de consultas en MongoDB

**¿Por qué esta API?**
DummyJSON proporciona datos estructurados de productos perfectos para demostrar operaciones CRUD completas y simular un catálogo real de e-commerce.

#### 2. **ExchangeRate API** - Conversión de Monedas
- **URL**: https://api.exchangerate-api.com/v4/latest/USD
- **Propósito**: Convertir precios de USD a COP (pesos colombianos) en tiempo real
- **Funcionalidades**:
  - Obtención de tasas de cambio actualizadas
  - Conversión automática de precios
  - Historial de conversiones en MongoDB

**¿Por qué esta API?**
Complementa la funcionalidad de productos permitiendo mostrar precios en moneda local, esencial para e-commerce internacional.

---

## 🏗️ Arquitectura MVC

### **Modelo (Model)**
- **PostgreSQL**: 
  - `ProductoAPI`: Almacena productos sincronizados
  - `ConsultaAPI`: Registro de consultas realizadas
- **MongoDB**: 
  - Colección `historial_dummyjson`: Historial detallado de consultas a DummyJSON
  - Colección `historial_exchangerate`: Historial de conversiones de moneda

### **Vista (View)**
Templates HTML ubicados en `/templates/apis/`:
- `dashboard.html`: Panel principal con estadísticas
- `productos_lista.html`: Listado de productos con filtros y paginación
- `producto_detalle.html`: Detalle completo de producto
- `busqueda.html`: Búsqueda directa en API
- `historial.html`: Visualización del historial MongoDB

### **Controlador (Controller)**
Archivo `views.py` que orquesta:
- Servicios de APIs (`dummyjson_service.py`, `exchangerate_service.py`)
- Modelos de datos (PostgreSQL y MongoDB)
- Renderizado de templates
- Manejo de errores y respuestas HTTP

---

## 📁 Estructura del Proyecto

```
ProyectoDjango/
├── applications/
│   ├── apis/                    # Nueva app de integración de APIs
│   │   ├── db/
│   │   │   └── mongodb.py       # Conexión MongoDB
│   │   ├── services/
│   │   │   ├── dummyjson_service.py    # Servicio API 1
│   │   │   └── exchangerate_service.py  # Servicio API 2
│   │   ├── models.py            # Modelos PostgreSQL
│   │   ├── views.py             # Controladores
│   │   ├── urls.py              # Rutas
│   │   └── admin.py             # Admin Django
│   ├── productos/               # App de productos existente
│   ├── carrito/                 # App de carrito existente
│   └── usuarios/                # App de usuarios existente
├── templates/
│   └── apis/                    # Templates de la app APIs
├── static/                      # Archivos estáticos
├── ProyectoDjango/
│   ├── settings/
│   │   ├── base.py
│   │   └── local.py
│   └── urls.py
├── docker-compose.yml           # PostgreSQL
├── manage.py
└── README.md
```

---

## 🔧 Configuración de Bases de Datos

### PostgreSQL (Relacional)
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'tienda_db',
        'USER': 'postgres',
        'PASSWORD': 'cami322',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
```

### MongoDB (No Relacional)
```python
# Conexión en applications/apis/db/mongodb.py
MongoClient('mongodb://localhost:27017/')
Database: 'tienda_apis_db'
```

---

## 🚀 Instalación y Configuración

### 1. Clonar el repositorio
```bash
git clone <URL_REPOSITORIO>
cd tienda/ProyectoDjango
```

### 2. Crear entorno virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate  # Windows
```

### 3. Instalar dependencias
```bash
pip install django==5.2.7
pip install djangorestframework
pip install django-cors-headers
pip install psycopg2-binary
pip install requests
pip install Pillow
pip install pymongo
pip install dnspython
```

### 4. Iniciar PostgreSQL con Docker
```bash
docker compose up -d
```

### 5. Iniciar MongoDB con Docker
```bash
docker run -d --name tienda_mongodb -p 27017:27017 mongo:latest
```

### 6. Aplicar migraciones
```bash
python manage.py migrate
```

### 7. Crear superusuario (opcional)
```bash
python manage.py createsuperuser
```

### 8. Iniciar servidor
```bash
python manage.py runserver
```

---

## 🧪 Cómo Probar la Funcionalidad

### 1. **Acceder al Dashboard**
```
URL: http://127.0.0.1:8000/apis/
```
Verás el panel principal con estadísticas y acciones rápidas.

### 2. **Sincronizar Productos (CREATE/UPDATE)**
- Clic en "Sincronizar Productos"
- Se obtienen 30 productos de DummyJSON
- Se convierten precios a COP automáticamente
- Se almacenan en PostgreSQL
- Se registra historial en MongoDB

### 3. **Listar Productos (READ)**
```
URL: http://127.0.0.1:8000/apis/productos/
```
- Filtrar por categoría
- Buscar por nombre
- Paginación automática

### 4. **Ver Detalle de Producto (READ)**
- Clic en "Ver" en cualquier producto
- Muestra información completa
- Precios en USD y COP

### 5. **Actualizar Precios COP (UPDATE)**
- Botón "Actualizar Precios COP"
- Obtiene tasa actual de ExchangeRate API
- Actualiza todos los productos

### 6. **Eliminar Producto (DELETE)**
- Botón "🗑️" en cualquier producto
- Confirmación antes de eliminar

### 7. **Buscar en API**
```
URL: http://127.0.0.1:8000/apis/buscar/
```
- Búsqueda directa en DummyJSON (sin guardar)
- Conversión de precios en tiempo real

### 8. **Ver Historial MongoDB**
```
URL: http://127.0.0.1:8000/apis/historial/
```
- Historial de todas las consultas a APIs
- Separado por tipo de API
- Muestra éxitos y errores

### 9. **Endpoints JSON (API REST)**
```
GET http://127.0.0.1:8000/apis/api/tasas/
GET http://127.0.0.1:8000/apis/api/productos/
```

---

## 🔄 Operaciones CRUD Completas

| Operación | Endpoint | Método | Descripción |
|-----------|----------|--------|-------------|
| **CREATE** | `/apis/productos/sincronizar/` | POST | Sincroniza productos desde API |
| **READ** | `/apis/productos/` | GET | Lista todos los productos |
| **READ** | `/apis/productos/<id>/` | GET | Detalle de un producto |
| **UPDATE** | `/apis/productos/actualizar-precios/` | POST | Actualiza precios COP |
| **DELETE** | `/apis/productos/<id>/eliminar/` | POST | Elimina un producto |

---

## 🎨 Patrón MVC Implementado

### **Separación de Responsabilidades**

1. **Modelos (`models.py`)**
   - Lógica de datos
   - Conexión a PostgreSQL
   - Definición de esquemas

2. **Servicios (`services/`)**
   - Consumo de APIs externas
   - Lógica de negocio
   - Conexión a MongoDB

3. **Vistas/Controladores (`views.py`)**
   - Orquestación entre modelos y servicios
   - Validación de datos
   - Manejo de errores HTTP

4. **Templates (`templates/apis/`)**
   - Presentación de datos
   - Interfaz de usuario
   - Sin lógica de negocio

---

## 🛠️ Manejo de Errores

El sistema implementa manejo robusto de errores:

- **Timeout de APIs**: 10 segundos máximo
- **Validación de respuestas**: `response.raise_for_status()`
- **Try-except**: En todas las operaciones críticas
- **Mensajes al usuario**: Sistema de mensajes de Django
- **Logging**: Registro en MongoDB de éxitos y fallos
- **Respuestas HTTP apropiadas**: 200, 404, 500

---

## 📊 Base de Datos

### PostgreSQL - Tablas
```sql
-- api_productos: Productos sincronizados
-- api_consultas: Registro de consultas
```

### MongoDB - Colecciones
```javascript
// historial_dummyjson
// historial_exchangerate
```

---

## 🔐 Variables de Entorno

Revisar `.env.example` para configuración:

```env
# PostgreSQL
DB_NAME=tienda_db
DB_USER=postgres
DB_PASSWORD=cami322
DB_HOST=127.0.0.1
DB_PORT=5432

# MongoDB
MONGO_HOST=localhost
MONGO_PORT=27017
MONGO_DB=tienda_apis_db
```

---

## 🎥 Video Demostrativo

[Enlace al video] - Máximo 5 minutos mostrando:
1. Consumo de las APIs
2. Operaciones CRUD
3. Estructura MVC
4. Bases de datos (PostgreSQL + MongoDB)

---

## 👨‍💻 Autor

**[Tu Nombre]**
- Correo: [tu_correo]
- GitHub: [tu_usuario]

---

## 📝 Notas

- Las APIs públicas utilizadas no requieren autenticación
- Los datos de DummyJSON son de prueba
- ExchangeRate puede tener límite de consultas diarias
- MongoDB debe estar ejecutándose en localhost:27017
- PostgreSQL debe estar ejecutándose en localhost:5432

---

## 🏆 Características Destacadas

✅ Patrón MVC bien definido
✅ Dos bases de datos (relacional + no relacional)
✅ CRUD completo funcional
✅ Manejo robusto de errores
✅ Diseño responsivo
✅ Paginación implementada
✅ Filtros y búsqueda
✅ APIs REST (JSON)
✅ Historial completo de operaciones
✅ Conversión de monedas en tiempo real
