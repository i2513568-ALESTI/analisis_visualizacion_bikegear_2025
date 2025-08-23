# Bike&Gear - Sistema de Gestión de Tienda

Sistema de gestión para tienda de bicicletas y accesorios construido con Streamlit y Supabase.

## Características

### Gestión de Inventario
- Registro completo de productos con categorías
- Control de stock en tiempo real
- Precios y costos con formato de moneda
- Vista de catálogo con estadísticas rápidas
- Validación de datos y mensajes de confirmación

### Sistema de Ventas
- Registro de ventas con cálculo automático de ganancias
- Control de stock automático
- Información detallada del producto durante la venta
- Validación de disponibilidad de stock
- Vista de productos disponibles para venta

### Dashboard de Reportes
- Métricas principales con diseño nativo
- Gráficos interactivos con Plotly
- Análisis de tendencias temporales
- Rendimiento por producto y categoría
- Tablas de datos con formato mejorado

## Tecnologías

- **Frontend**: Streamlit 1.48.1
- **Base de Datos**: Supabase (PostgreSQL)
- **Gráficos**: Plotly 6.3.0
- **Análisis de Datos**: Pandas 2.3.2

## Instalación

1. **Clonar el repositorio**
   ```bash
   git clone <url-del-repositorio>
   cd analisis_visualizacion_bikegear_2025
   ```

2. **Crear entorno virtual**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar Supabase**
   - Crear cuenta en Supabase
   - Crear nuevo proyecto
   - Configurar tablas necesarias
   - Actualizar config/supabase_client.py

5. **Ejecutar aplicación**
   ```bash
   streamlit run main.py
   ```

## Base de Datos

### Tabla: productos
```sql
CREATE TABLE productos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    categoria VARCHAR(100) NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    costo DECIMAL(10,2) NOT NULL,
    stock INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Tabla: ventas
```sql
CREATE TABLE ventas (
    id SERIAL PRIMARY KEY,
    producto_id INTEGER REFERENCES productos(id),
    cantidad INTEGER NOT NULL,
    ingreso DECIMAL(10,2) NOT NULL,
    ganancia DECIMAL(10,2) NOT NULL,
    ubicacion VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
```

## Estructura del Proyecto

```
analisis_visualizacion_bikegear_2025/
├── main.py
├── pages/
│   ├── productos.py
│   ├── ventas.py
│   └── reportes.py
├── config/
│   └── supabase_client.py
├── utils/
│   └── helpers.py
├── requirements.txt
└── README.md
```

## Funcionalidades

### Gestión de Productos
- Agregar productos con formulario intuitivo
- Categorías: Bicicletas, Accesorios, Repuestos, Ropa, Herramientas
- Control de stock automático
- Manejo de precios y costos
- Vista de catálogo interactiva

### Sistema de Ventas
- Selección de productos con información en tiempo real
- Cálculo automático de ingresos y ganancias
- Validación de disponibilidad de stock
- Actualización automática del inventario
- Vista previa de transacciones

### Reportes y Analytics
- Métricas principales: Ingresos, ganancias, ventas, unidades
- Gráficos interactivos de líneas de tiempo
- Análisis de rendimiento por producto
- Tendencias y promedios
- Historial completo de ventas

## Despliegue

### Streamlit Cloud
1. Conectar repositorio a Streamlit Cloud
2. Configurar variables de entorno de Supabase
3. Desplegar automáticamente

### Heroku
1. Crear Procfile
2. Configurar variables de entorno
3. Desplegar con Git

## Licencia

Este proyecto está bajo la Licencia MIT.