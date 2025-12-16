-- ================================================
-- SCRIPT SQL PARA PROYECTO TIENDA
-- Base de Datos: tienda_db
-- Motor: PostgreSQL 15
-- ================================================

-- Crear base de datos (ejecutar como superusuario)
-- CREATE DATABASE tienda_db;
-- CREATE USER postgres WITH PASSWORD 'cami322';
-- GRANT ALL PRIVILEGES ON DATABASE tienda_db TO postgres;

-- Conectar a la base de datos
-- \c tienda_db

-- ================================================
-- TABLA: api_productos
-- Descripción: Almacena productos sincronizados desde DummyJSON API
-- ================================================
CREATE TABLE IF NOT EXISTS api_productos (
    id SERIAL PRIMARY KEY,
    api_id INTEGER UNIQUE NOT NULL,
    titulo VARCHAR(200) NOT NULL,
    descripcion TEXT,
    precio_usd NUMERIC(10, 2) NOT NULL,
    precio_cop NUMERIC(15, 2),
    categoria VARCHAR(100),
    marca VARCHAR(100),
    stock INTEGER DEFAULT 0,
    rating NUMERIC(3, 2),
    imagen_url TEXT,
    sincronizado_en TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    actualizado_en TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    activo BOOLEAN DEFAULT TRUE,
    
    CONSTRAINT api_productos_precio_usd_check CHECK (precio_usd >= 0),
    CONSTRAINT api_productos_stock_check CHECK (stock >= 0),
    CONSTRAINT api_productos_rating_check CHECK (rating >= 0 AND rating <= 5)
);

-- Índices para optimizar consultas
CREATE INDEX idx_api_productos_categoria ON api_productos(categoria);
CREATE INDEX idx_api_productos_activo ON api_productos(activo);
CREATE INDEX idx_api_productos_api_id ON api_productos(api_id);

-- Comentarios de la tabla
COMMENT ON TABLE api_productos IS 'Productos sincronizados desde DummyJSON API';
COMMENT ON COLUMN api_productos.api_id IS 'ID del producto en la API externa';
COMMENT ON COLUMN api_productos.precio_usd IS 'Precio en dólares estadounidenses';
COMMENT ON COLUMN api_productos.precio_cop IS 'Precio convertido a pesos colombianos';

-- ================================================
-- TABLA: api_consultas
-- Descripción: Registro de consultas realizadas a las APIs
-- ================================================
CREATE TABLE IF NOT EXISTS api_consultas (
    id SERIAL PRIMARY KEY,
    tipo VARCHAR(20) NOT NULL,
    api_nombre VARCHAR(100) NOT NULL,
    fecha_consulta TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    exitosa BOOLEAN DEFAULT TRUE,
    detalles TEXT,
    
    CONSTRAINT api_consultas_tipo_check CHECK (tipo IN ('PRODUCTO', 'CONVERSION', 'BUSQUEDA'))
);

-- Índices para optimizar consultas
CREATE INDEX idx_api_consultas_fecha ON api_consultas(fecha_consulta DESC);
CREATE INDEX idx_api_consultas_api_nombre ON api_consultas(api_nombre);
CREATE INDEX idx_api_consultas_tipo ON api_consultas(tipo);

-- Comentarios de la tabla
COMMENT ON TABLE api_consultas IS 'Registro de todas las consultas realizadas a APIs externas';
COMMENT ON COLUMN api_consultas.tipo IS 'Tipo de consulta: PRODUCTO, CONVERSION, BUSQUEDA';
COMMENT ON COLUMN api_consultas.exitosa IS 'Indica si la consulta fue exitosa';

-- ================================================
-- VISTA: productos_activos_con_precio_cop
-- Descripción: Vista de productos activos con precios en COP
-- ================================================
CREATE OR REPLACE VIEW productos_activos_con_precio_cop AS
SELECT 
    id,
    api_id,
    titulo,
    categoria,
    marca,
    precio_usd,
    precio_cop,
    stock,
    rating,
    sincronizado_en,
    actualizado_en
FROM api_productos
WHERE activo = TRUE AND precio_cop IS NOT NULL
ORDER BY actualizado_en DESC;

-- ================================================
-- FUNCIÓN: actualizar_timestamp
-- Descripción: Actualiza automáticamente el campo actualizado_en
-- ================================================
CREATE OR REPLACE FUNCTION actualizar_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.actualizado_en = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger para actualizar timestamp en api_productos
CREATE TRIGGER trigger_actualizar_timestamp_productos
BEFORE UPDATE ON api_productos
FOR EACH ROW
EXECUTE FUNCTION actualizar_timestamp();

-- ================================================
-- DATOS DE EJEMPLO (Opcional - solo para pruebas)
-- ================================================

-- Insertar consulta de ejemplo
INSERT INTO api_consultas (tipo, api_nombre, exitosa, detalles) 
VALUES ('PRODUCTO', 'DummyJSON', TRUE, 'Sincronización inicial de productos');

-- ================================================
-- CONSULTAS ÚTILES
-- ================================================

-- Ver productos activos por categoría
-- SELECT categoria, COUNT(*) as cantidad, AVG(precio_usd) as precio_promedio
-- FROM api_productos
-- WHERE activo = TRUE
-- GROUP BY categoria
-- ORDER BY cantidad DESC;

-- Ver historial de consultas exitosas
-- SELECT api_nombre, tipo, COUNT(*) as total
-- FROM api_consultas
-- WHERE exitosa = TRUE
-- GROUP BY api_nombre, tipo;

-- Ver productos sin precio en COP (necesitan actualización)
-- SELECT titulo, precio_usd
-- FROM api_productos
-- WHERE precio_cop IS NULL AND activo = TRUE;

-- ================================================
-- RESPALDO Y RESTAURACIÓN
-- ================================================

-- Crear respaldo:
-- pg_dump -U postgres -d tienda_db -F c -b -v -f tienda_db_backup.dump

-- Restaurar respaldo:
-- pg_restore -U postgres -d tienda_db -v tienda_db_backup.dump

-- ================================================
-- PERMISOS
-- ================================================

-- Otorgar permisos al usuario de la aplicación
GRANT SELECT, INSERT, UPDATE, DELETE ON api_productos TO postgres;
GRANT SELECT, INSERT, UPDATE, DELETE ON api_consultas TO postgres;
GRANT USAGE, SELECT ON SEQUENCE api_productos_id_seq TO postgres;
GRANT USAGE, SELECT ON SEQUENCE api_consultas_id_seq TO postgres;

-- ================================================
-- NOTAS IMPORTANTES
-- ================================================

-- 1. Este script crea las tablas necesarias para la app 'apis'
-- 2. Las migraciones de Django crearán automáticamente estas tablas
-- 3. Este archivo es útil para entender la estructura sin Django
-- 4. MongoDB se usa para historial detallado (no incluido aquí)
-- 5. Ajustar PASSWORD según configuración de seguridad
