"""
Preparación simplificada de datos para Power BI.

Este script verifica la estructura de la base de datos y crea
datasets optimizados para Power BI.
"""

import pandas as pd
import sqlite3
import logging
from pathlib import Path
import json
from datetime import datetime

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def check_database_structure(db_path: str = "data/processed/sales_analysis.db"):
    """Verificar la estructura de la base de datos."""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Obtener información de las tablas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print("📊 Tablas disponibles en la base de datos:")
        for table in tables:
            print(f"   - {table[0]}")
        
        # Verificar estructura de la tabla sales_data
        cursor.execute("PRAGMA table_info(sales_data);")
        columns = cursor.fetchall()
        
        print("\n📋 Columnas en la tabla sales_data:")
        for col in columns:
            print(f"   - {col[1]} ({col[2]})")
        
        # Verificar algunos datos de ejemplo
        cursor.execute("SELECT * FROM sales_data LIMIT 3;")
        sample_data = cursor.fetchall()
        
        print(f"\n📝 Datos de ejemplo (primeras 3 filas):")
        for i, row in enumerate(sample_data):
            print(f"   Fila {i+1}: {row[:5]}...")  # Mostrar solo las primeras 5 columnas
        
        conn.close()
        return [col[1] for col in columns]  # Retornar nombres de columnas
        
    except Exception as e:
        logger.error(f"Error al verificar la estructura: {e}")
        raise


def create_powerbi_datasets(db_path: str = "data/processed/sales_analysis.db"):
    """Crear datasets optimizados para Power BI."""
    try:
        conn = sqlite3.connect(db_path)
        
        datasets = {}
        
        # 1. Dataset principal de ventas (solo columnas existentes)
        print("\n🔄 Creando dataset principal de ventas...")
        query_sales = """
        SELECT 
            ORDERNUMBER,
            ORDERDATE,
            CUSTOMERNAME,
            PRODUCTCODE,
            PRODUCTLINE,
            COUNTRY,
            CITY,
            SALES,
            QUANTITYORDERED,
            PRICEEACH,
            STATUS,
            DEALSIZE
        FROM sales_data
        WHERE STATUS != 'Cancelled'
        ORDER BY ORDERDATE DESC
        """
        
        datasets['sales_fact'] = pd.read_sql_query(query_sales, conn)
        print(f"   ✅ Dataset de ventas creado: {datasets['sales_fact'].shape[0]} registros")
        
        # 2. Dimensión de clientes
        print("🔄 Creando dimensión de clientes...")
        query_customers = """
        SELECT DISTINCT
            CUSTOMERNAME,
            COUNTRY,
            CITY,
            COUNT(*) as total_orders,
            SUM(SALES) as total_sales,
            AVG(SALES) as avg_order_value,
            MIN(ORDERDATE) as first_order_date,
            MAX(ORDERDATE) as last_order_date
        FROM sales_data
        WHERE STATUS != 'Cancelled'
        GROUP BY CUSTOMERNAME, COUNTRY, CITY
        ORDER BY total_sales DESC
        """
        
        datasets['dim_customers'] = pd.read_sql_query(query_customers, conn)
        print(f"   ✅ Dimensión de clientes creada: {datasets['dim_customers'].shape[0]} clientes")
        
        # 3. Dimensión de productos
        print("🔄 Creando dimensión de productos...")
        query_products = """
        SELECT DISTINCT
            PRODUCTCODE,
            PRODUCTLINE,
            COUNT(*) as total_orders,
            SUM(SALES) as total_sales,
            SUM(QUANTITYORDERED) as total_quantity,
            AVG(PRICEEACH) as avg_price,
            AVG(SALES) as avg_order_value
        FROM sales_data
        WHERE STATUS != 'Cancelled'
        GROUP BY PRODUCTCODE, PRODUCTLINE
        ORDER BY total_sales DESC
        """
        
        datasets['dim_products'] = pd.read_sql_query(query_products, conn)
        print(f"   ✅ Dimensión de productos creada: {datasets['dim_products'].shape[0]} productos")
        
        # 4. Dimensión de países
        print("🔄 Creando dimensión de países...")
        query_countries = """
        SELECT DISTINCT
            COUNTRY,
            COUNT(DISTINCT CUSTOMERNAME) as unique_customers,
            COUNT(*) as total_orders,
            SUM(SALES) as total_sales,
            AVG(SALES) as avg_order_value,
            COUNT(DISTINCT PRODUCTCODE) as unique_products
        FROM sales_data
        WHERE STATUS != 'Cancelled'
        GROUP BY COUNTRY
        ORDER BY total_sales DESC
        """
        
        datasets['dim_countries'] = pd.read_sql_query(query_countries, conn)
        print(f"   ✅ Dimensión de países creada: {datasets['dim_countries'].shape[0]} países")
        
        # 5. Métricas de ventas por fecha
        print("🔄 Creando métricas de ventas...")
        query_metrics = """
        SELECT 
            DATE(ORDERDATE) as order_date,
            SUM(SALES) as daily_sales,
            COUNT(*) as daily_orders,
            COUNT(DISTINCT CUSTOMERNAME) as daily_customers,
            AVG(SALES) as avg_order_value
        FROM sales_data
        WHERE STATUS != 'Cancelled'
        GROUP BY DATE(ORDERDATE)
        ORDER BY order_date
        """
        
        datasets['sales_metrics'] = pd.read_sql_query(query_metrics, conn)
        print(f"   ✅ Métricas de ventas creadas: {datasets['sales_metrics'].shape[0]} días")
        
        # 6. Análisis temporal
        print("🔄 Creando análisis temporal...")
        query_temporal = """
        SELECT 
            strftime('%Y', ORDERDATE) as year,
            strftime('%m', ORDERDATE) as month,
            strftime('%w', ORDERDATE) as day_of_week,
            COUNT(*) as order_count,
            SUM(SALES) as total_sales,
            COUNT(DISTINCT CUSTOMERNAME) as unique_customers,
            AVG(SALES) as avg_order_value
        FROM sales_data
        WHERE STATUS != 'Cancelled'
        GROUP BY year, month, day_of_week
        ORDER BY year, month, day_of_week
        """
        
        datasets['temporal_analysis'] = pd.read_sql_query(query_temporal, conn)
        print(f"   ✅ Análisis temporal creado: {datasets['temporal_analysis'].shape[0]} registros")
        
        # 7. Análisis geográfico
        print("🔄 Creando análisis geográfico...")
        query_geographic = """
        SELECT 
            COUNTRY,
            CITY,
            COUNT(*) as order_count,
            SUM(SALES) as total_sales,
            COUNT(DISTINCT CUSTOMERNAME) as unique_customers,
            COUNT(DISTINCT PRODUCTCODE) as unique_products,
            AVG(SALES) as avg_order_value
        FROM sales_data
        WHERE STATUS != 'Cancelled'
        GROUP BY COUNTRY, CITY
        ORDER BY total_sales DESC
        """
        
        datasets['geographic_analysis'] = pd.read_sql_query(query_geographic, conn)
        print(f"   ✅ Análisis geográfico creado: {datasets['geographic_analysis'].shape[0]} ubicaciones")
        
        conn.close()
        return datasets
        
    except Exception as e:
        logger.error(f"Error al crear datasets: {e}")
        raise


def export_to_excel(datasets, output_path: str = "data/final/powerbi_data.xlsx"):
    """Exportar datasets a Excel."""
    print(f"\n📊 Exportando datasets a Excel: {output_path}")
    
    try:
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            for sheet_name, df in datasets.items():
                # Limitar el nombre de la hoja a 31 caracteres
                sheet_name = sheet_name[:31]
                df.to_excel(writer, sheet_name=sheet_name, index=False)
                print(f"   ✅ Hoja '{sheet_name}': {df.shape[0]} filas, {df.shape[1]} columnas")
        
        print(f"✅ Archivo Excel creado exitosamente: {output_path}")
        
    except Exception as e:
        logger.error(f"Error al exportar a Excel: {e}")
        raise


def export_to_csv(datasets, output_dir: str = "data/final/powerbi_csv/"):
    """Exportar datasets a archivos CSV separados."""
    print(f"\n📄 Exportando datasets a CSV en: {output_dir}")
    
    try:
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        for dataset_name, df in datasets.items():
            csv_path = Path(output_dir) / f"{dataset_name}.csv"
            df.to_csv(csv_path, index=False, encoding='utf-8')
            print(f"   ✅ CSV '{dataset_name}': {df.shape[0]} filas, {df.shape[1]} columnas")
        
        print(f"✅ Archivos CSV creados exitosamente en: {output_dir}")
        
    except Exception as e:
        logger.error(f"Error al exportar a CSV: {e}")
        raise


def create_powerbi_guide(output_path: str = "data/final/powerbi_guide.md"):
    """Generar guía para Power BI."""
    print(f"\n📖 Generando guía para Power BI: {output_path}")
    
    guide_content = """# Guía para Power BI - Análisis de Ventas

## 📊 Datasets Disponibles

### 1. **sales_fact** - Tabla Principal de Hechos
- **Descripción**: Datos de ventas detallados
- **Registros**: ~2,800 ventas
- **Columnas clave**: ORDERNUMBER, ORDERDATE, CUSTOMERNAME, PRODUCTCODE, SALES

### 2. **dim_customers** - Dimensión de Clientes
- **Descripción**: Información agregada por cliente
- **Registros**: ~350 clientes únicos
- **Columnas clave**: CUSTOMERNAME, COUNTRY, total_sales, avg_order_value

### 3. **dim_products** - Dimensión de Productos
- **Descripción**: Información agregada por producto
- **Registros**: ~100 productos únicos
- **Columnas clave**: PRODUCTCODE, PRODUCTLINE, total_sales, total_quantity

### 4. **dim_countries** - Dimensión de Países
- **Descripción**: Información agregada por país
- **Registros**: ~20 países
- **Columnas clave**: COUNTRY, total_sales, unique_customers

### 5. **sales_metrics** - Métricas de Ventas
- **Descripción**: Métricas agregadas por día
- **Registros**: ~200 días
- **Columnas clave**: order_date, daily_sales, daily_orders, avg_order_value

### 6. **temporal_analysis** - Análisis Temporal
- **Descripción**: Análisis por año, mes y día de la semana
- **Registros**: ~500 registros temporales
- **Columnas clave**: year, month, day_of_week, total_sales

### 7. **geographic_analysis** - Análisis Geográfico
- **Descripción**: Análisis por país y ciudad
- **Registros**: ~100 ubicaciones
- **Columnas clave**: COUNTRY, CITY, total_sales, unique_customers

## 🎯 Visualizaciones Recomendadas

### Dashboard Principal
1. **KPI Cards**:
   - Total de Ventas: `SUM(sales_fact[SALES])`
   - Número de Órdenes: `COUNTROWS(sales_fact)`
   - Clientes Únicos: `DISTINCTCOUNT(sales_fact[CUSTOMERNAME])`
   - Valor Promedio por Orden: `AVERAGE(sales_fact[SALES])`

2. **Gráficos de Línea**:
   - Ventas por Día: `sales_metrics[order_date]` vs `sales_metrics[daily_sales]`
   - Órdenes por Día: `sales_metrics[order_date]` vs `sales_metrics[daily_orders]`

3. **Gráficos de Barras**:
   - Top 10 Clientes: `dim_customers[CUSTOMERNAME]` vs `dim_customers[total_sales]`
   - Top 10 Productos: `dim_products[PRODUCTCODE]` vs `dim_products[total_sales]`
   - Ventas por País: `dim_countries[COUNTRY]` vs `dim_countries[total_sales]`

4. **Mapa**:
   - Ventas por País: Usar `geographic_analysis` con campo COUNTRY

### Dashboard de Análisis Detallado
1. **Tabla de Clientes**:
   - Todas las columnas de `dim_customers`
   - Filtros por país y rango de ventas

2. **Análisis de Productos**:
   - Todas las columnas de `dim_products`
   - Gráfico de dispersión: cantidad vs valor

3. **Análisis Temporal**:
   - Gráfico de calor: `temporal_analysis[month]` vs `temporal_analysis[day_of_week]`
   - Gráfico de líneas por año

## 🔗 Relaciones en Power BI

### Modelo de Datos
```
sales_fact (1) → (1) dim_customers [CUSTOMERNAME]
sales_fact (1) → (1) dim_products [PRODUCTCODE]
sales_fact (1) → (1) dim_countries [COUNTRY]
sales_fact (1) → (1) sales_metrics [ORDERDATE]
```

### Configuración de Relaciones
1. **sales_fact.CUSTOMERNAME** → **dim_customers.CUSTOMERNAME**
2. **sales_fact.PRODUCTCODE** → **dim_products.PRODUCTCODE**
3. **sales_fact.COUNTRY** → **dim_countries.COUNTRY**
4. **sales_fact.ORDERDATE** → **sales_metrics.order_date**

## 📈 Medidas DAX Recomendadas

### Medidas Básicas
```dax
Total Sales = SUM(sales_fact[SALES])
Total Orders = COUNTROWS(sales_fact)
Unique Customers = DISTINCTCOUNT(sales_fact[CUSTOMERNAME])
Average Order Value = DIVIDE([Total Sales], [Total Orders])
```

### Medidas Avanzadas
```dax
Sales Growth % = 
VAR CurrentSales = [Total Sales]
VAR PreviousSales = CALCULATE([Total Sales], DATEADD(sales_metrics[order_date], -1, MONTH))
RETURN
DIVIDE(CurrentSales - PreviousSales, PreviousSales)

Customer Retention = 
VAR CurrentCustomers = [Unique Customers]
VAR PreviousCustomers = CALCULATE([Unique Customers], DATEADD(sales_metrics[order_date], -1, MONTH))
RETURN
DIVIDE(CurrentCustomers, PreviousCustomers)
```

## 🎨 Configuración de Tema

### Colores Recomendados
- **Primario**: #1f77b4 (Azul)
- **Secundario**: #ff7f0e (Naranja)
- **Éxito**: #2ca02c (Verde)
- **Advertencia**: #d62728 (Rojo)
- **Neutro**: #7f7f7f (Gris)

### Tipografía
- **Títulos**: Segoe UI Bold, 16pt
- **Subtítulos**: Segoe UI Semibold, 14pt
- **Texto**: Segoe UI Regular, 12pt

## 📋 Checklist de Implementación

- [ ] Importar datasets desde Excel/CSV
- [ ] Configurar relaciones entre tablas
- [ ] Crear medidas DAX básicas
- [ ] Diseñar dashboard principal
- [ ] Crear visualizaciones recomendadas
- [ ] Configurar filtros y segmentadores
- [ ] Aplicar tema y colores
- [ ] Probar interactividad
- [ ] Optimizar rendimiento
- [ ] Documentar dashboard

## 🚀 Próximos Pasos

1. **Análisis Predictivo**: Implementar modelos de ML
2. **Alertas**: Configurar notificaciones automáticas
3. **Automatización**: Actualización automática de datos
4. **Móvil**: Optimizar para dispositivos móviles
5. **Colaboración**: Compartir con stakeholders

---
*Generado automáticamente por el sistema de análisis de datos*
"""
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(guide_content)
        
        print(f"✅ Guía de Power BI generada: {output_path}")
        
    except Exception as e:
        logger.error(f"Error al generar guía: {e}")
        raise


def main():
    """Función principal."""
    print("🚀 Preparando datos para Power BI...")
    
    try:
        # 1. Verificar estructura de la base de datos
        print("\n🔍 Verificando estructura de la base de datos...")
        columns = check_database_structure()
        
        # 2. Crear datasets
        print("\n🔄 Creando datasets optimizados...")
        datasets = create_powerbi_datasets()
        
        # 3. Exportar a Excel
        export_to_excel(datasets)
        
        # 4. Exportar a CSV
        export_to_csv(datasets)
        
        # 5. Generar guía
        create_powerbi_guide()
        
        print("\n✅ ¡Datos preparados exitosamente para Power BI!")
        print(f"\n📊 Archivos generados:")
        print(f"   - Excel: data/final/powerbi_data.xlsx")
        print(f"   - CSV: data/final/powerbi_csv/")
        print(f"   - Guía: data/final/powerbi_guide.md")
        
        print(f"\n🎯 Próximos pasos:")
        print(f"   1. Abrir Power BI Desktop")
        print(f"   2. Importar el archivo Excel: data/final/powerbi_data.xlsx")
        print(f"   3. Configurar las relaciones entre tablas")
        print(f"   4. Crear las visualizaciones siguiendo la guía")
        print(f"   5. Aplicar el tema y colores recomendados")
        
    except Exception as e:
        logger.error(f"Error en la preparación de datos: {e}")
        raise


if __name__ == "__main__":
    main()

