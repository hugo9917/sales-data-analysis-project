"""
Preparación de datos para Power BI.

Este módulo prepara los datos optimizados para Power BI,
incluyendo consultas SQL especializadas y transformaciones
de datos para visualizaciones efectivas.
"""

import pandas as pd
import sqlite3
import logging
from pathlib import Path
from typing import Dict, List, Tuple
import json
from datetime import datetime
import numpy as np

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PowerBIDataPreparator:
    """
    Clase para preparar datos optimizados para Power BI.
    """
    
    def __init__(self, db_path: str = "data/processed/sales_analysis.db"):
        """
        Inicializar el preparador de datos para Power BI.
        
        Args:
            db_path: Ruta a la base de datos SQLite
        """
        self.db_path = db_path
        self.connection = None
        
    def connect_db(self) -> sqlite3.Connection:
        """Conectar a la base de datos."""
        try:
            self.connection = sqlite3.connect(self.db_path)
            logger.info("Conectado a la base de datos SQLite")
            return self.connection
        except Exception as e:
            logger.error(f"Error al conectar a la base de datos: {e}")
            raise
    
    def create_powerbi_datasets(self) -> Dict[str, pd.DataFrame]:
        """
        Crear datasets optimizados para Power BI.
        
        Returns:
            Diccionario con los datasets principales
        """
        logger.info("Creando datasets optimizados para Power BI...")
        
        datasets = {}
        
        # 1. Dataset principal de ventas
        datasets['sales_fact'] = self._create_sales_fact_table()
        
        # 2. Dimensiones
        datasets['dim_customers'] = self._create_customer_dimension()
        datasets['dim_products'] = self._create_product_dimension()
        datasets['dim_countries'] = self._create_country_dimension()
        datasets['dim_dates'] = self._create_date_dimension()
        
        # 3. Métricas calculadas
        datasets['sales_metrics'] = self._create_sales_metrics()
        datasets['customer_metrics'] = self._create_customer_metrics()
        datasets['product_metrics'] = self._create_product_metrics()
        
        # 4. Análisis temporal
        datasets['temporal_analysis'] = self._create_temporal_analysis()
        
        # 5. Análisis geográfico
        datasets['geographic_analysis'] = self._create_geographic_analysis()
        
        logger.info(f"Se crearon {len(datasets)} datasets para Power BI")
        return datasets
    
    def _create_sales_fact_table(self) -> pd.DataFrame:
        """Crear tabla de hechos de ventas optimizada."""
        query = """
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
            DEALSIZE,
            YEAR,
            MONTH,
            QUARTER,
            DAY_OF_WEEK,
            IS_WEEKEND,
            SALES_PER_UNIT,
            TOTAL_ORDER_VALUE,
            CUSTOMER_SEGMENT,
            PRODUCT_CATEGORY
        FROM sales_data
        WHERE STATUS != 'Cancelled'
        ORDER BY ORDERDATE DESC
        """
        
        df = pd.read_sql_query(query, self.connection)
        logger.info(f"Tabla de hechos creada: {df.shape[0]} registros")
        return df
    
    def _create_customer_dimension(self) -> pd.DataFrame:
        """Crear dimensión de clientes."""
        query = """
        SELECT DISTINCT
            CUSTOMERNAME,
            COUNTRY,
            CITY,
            CUSTOMER_SEGMENT,
            COUNT(*) as total_orders,
            SUM(SALES) as total_sales,
            AVG(SALES) as avg_order_value,
            MIN(ORDERDATE) as first_order_date,
            MAX(ORDERDATE) as last_order_date
        FROM sales_data
        WHERE STATUS != 'Cancelled'
        GROUP BY CUSTOMERNAME, COUNTRY, CITY, CUSTOMER_SEGMENT
        ORDER BY total_sales DESC
        """
        
        df = pd.read_sql_query(query, self.connection)
        logger.info(f"Dimensión de clientes creada: {df.shape[0]} clientes únicos")
        return df
    
    def _create_product_dimension(self) -> pd.DataFrame:
        """Crear dimensión de productos."""
        query = """
        SELECT DISTINCT
            PRODUCTCODE,
            PRODUCTLINE,
            PRODUCT_CATEGORY,
            COUNT(*) as total_orders,
            SUM(SALES) as total_sales,
            SUM(QUANTITYORDERED) as total_quantity,
            AVG(PRICEEACH) as avg_price,
            AVG(SALES) as avg_order_value
        FROM sales_data
        WHERE STATUS != 'Cancelled'
        GROUP BY PRODUCTCODE, PRODUCTLINE, PRODUCT_CATEGORY
        ORDER BY total_sales DESC
        """
        
        df = pd.read_sql_query(query, self.connection)
        logger.info(f"Dimensión de productos creada: {df.shape[0]} productos únicos")
        return df
    
    def _create_country_dimension(self) -> pd.DataFrame:
        """Crear dimensión de países."""
        query = """
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
        
        df = pd.read_sql_query(query, self.connection)
        logger.info(f"Dimensión de países creada: {df.shape[0]} países")
        return df
    
    def _create_date_dimension(self) -> pd.DataFrame:
        """Crear dimensión de fechas."""
        query = """
        SELECT DISTINCT
            ORDERDATE,
            YEAR,
            MONTH,
            QUARTER,
            DAY_OF_WEEK,
            IS_WEEKEND,
            CASE 
                WHEN MONTH IN (12, 1, 2) THEN 'Winter'
                WHEN MONTH IN (3, 4, 5) THEN 'Spring'
                WHEN MONTH IN (6, 7, 8) THEN 'Summer'
                ELSE 'Fall'
            END as SEASON
        FROM sales_data
        WHERE STATUS != 'Cancelled'
        ORDER BY ORDERDATE
        """
        
        df = pd.read_sql_query(query, self.connection)
        logger.info(f"Dimensión de fechas creada: {df.shape[0]} fechas únicas")
        return df
    
    def _create_sales_metrics(self) -> pd.DataFrame:
        """Crear métricas de ventas agregadas."""
        query = """
        WITH daily_sales AS (
            SELECT 
                ORDERDATE,
                SUM(SALES) as daily_sales,
                COUNT(*) as daily_orders,
                COUNT(DISTINCT CUSTOMERNAME) as daily_customers
            FROM sales_data
            WHERE STATUS != 'Cancelled'
            GROUP BY ORDERDATE
        ),
        monthly_sales AS (
            SELECT 
                YEAR,
                MONTH,
                SUM(SALES) as monthly_sales,
                COUNT(*) as monthly_orders,
                COUNT(DISTINCT CUSTOMERNAME) as monthly_customers
            FROM sales_data
            WHERE STATUS != 'Cancelled'
            GROUP BY YEAR, MONTH
        )
        SELECT 
            'Daily' as aggregation_level,
            ORDERDATE as date,
            daily_sales,
            daily_orders,
            daily_customers,
            daily_sales / NULLIF(daily_orders, 0) as avg_order_value
        FROM daily_sales
        UNION ALL
        SELECT 
            'Monthly' as aggregation_level,
            DATE(YEAR || '-' || printf('%02d', MONTH) || '-01') as date,
            monthly_sales,
            monthly_orders,
            monthly_customers,
            monthly_sales / NULLIF(monthly_orders, 0) as avg_order_value
        FROM monthly_sales
        ORDER BY date
        """
        
        df = pd.read_sql_query(query, self.connection)
        logger.info(f"Métricas de ventas creadas: {df.shape[0]} registros")
        return df
    
    def _create_customer_metrics(self) -> pd.DataFrame:
        """Crear métricas de clientes."""
        query = """
        WITH customer_rankings AS (
            SELECT 
                CUSTOMERNAME,
                COUNTRY,
                COUNT(*) as order_count,
                SUM(SALES) as total_sales,
                AVG(SALES) as avg_order_value,
                ROW_NUMBER() OVER (ORDER BY SUM(SALES) DESC) as sales_rank,
                ROW_NUMBER() OVER (ORDER BY COUNT(*) DESC) as order_rank
            FROM sales_data
            WHERE STATUS != 'Cancelled'
            GROUP BY CUSTOMERNAME, COUNTRY
        )
        SELECT 
            *,
            CASE 
                WHEN sales_rank <= 10 THEN 'Top 10'
                WHEN sales_rank <= 50 THEN 'Top 50'
                WHEN sales_rank <= 100 THEN 'Top 100'
                ELSE 'Others'
            END as customer_tier
        FROM customer_rankings
        ORDER BY sales_rank
        """
        
        df = pd.read_sql_query(query, self.connection)
        logger.info(f"Métricas de clientes creadas: {df.shape[0]} clientes")
        return df
    
    def _create_product_metrics(self) -> pd.DataFrame:
        """Crear métricas de productos."""
        query = """
        WITH product_performance AS (
            SELECT 
                PRODUCTCODE,
                PRODUCTLINE,
                COUNT(*) as order_count,
                SUM(SALES) as total_sales,
                SUM(QUANTITYORDERED) as total_quantity,
                AVG(PRICEEACH) as avg_price,
                ROW_NUMBER() OVER (ORDER BY SUM(SALES) DESC) as sales_rank,
                ROW_NUMBER() OVER (ORDER BY SUM(QUANTITYORDERED) DESC) as quantity_rank
            FROM sales_data
            WHERE STATUS != 'Cancelled'
            GROUP BY PRODUCTCODE, PRODUCTLINE
        )
        SELECT 
            *,
            CASE 
                WHEN sales_rank <= 10 THEN 'Top 10'
                WHEN sales_rank <= 25 THEN 'Top 25'
                WHEN sales_rank <= 50 THEN 'Top 50'
                ELSE 'Others'
            END as product_tier
        FROM product_performance
        ORDER BY sales_rank
        """
        
        df = pd.read_sql_query(query, self.connection)
        logger.info(f"Métricas de productos creadas: {df.shape[0]} productos")
        return df
    
    def _create_temporal_analysis(self) -> pd.DataFrame:
        """Crear análisis temporal detallado."""
        query = """
        SELECT 
            YEAR,
            MONTH,
            QUARTER,
            DAY_OF_WEEK,
            COUNT(*) as order_count,
            SUM(SALES) as total_sales,
            COUNT(DISTINCT CUSTOMERNAME) as unique_customers,
            COUNT(DISTINCT PRODUCTCODE) as unique_products,
            AVG(SALES) as avg_order_value,
            SUM(QUANTITYORDERED) as total_quantity
        FROM sales_data
        WHERE STATUS != 'Cancelled'
        GROUP BY YEAR, MONTH, QUARTER, DAY_OF_WEEK
        ORDER BY YEAR, MONTH, DAY_OF_WEEK
        """
        
        df = pd.read_sql_query(query, self.connection)
        logger.info(f"Análisis temporal creado: {df.shape[0]} registros")
        return df
    
    def _create_geographic_analysis(self) -> pd.DataFrame:
        """Crear análisis geográfico."""
        query = """
        SELECT 
            COUNTRY,
            CITY,
            COUNT(*) as order_count,
            SUM(SALES) as total_sales,
            COUNT(DISTINCT CUSTOMERNAME) as unique_customers,
            COUNT(DISTINCT PRODUCTCODE) as unique_products,
            AVG(SALES) as avg_order_value,
            SUM(QUANTITYORDERED) as total_quantity
        FROM sales_data
        WHERE STATUS != 'Cancelled'
        GROUP BY COUNTRY, CITY
        ORDER BY total_sales DESC
        """
        
        df = pd.read_sql_query(query, self.connection)
        logger.info(f"Análisis geográfico creado: {df.shape[0]} ubicaciones")
        return df
    
    def export_to_excel(self, datasets: Dict[str, pd.DataFrame], output_path: str = "data/final/powerbi_data.xlsx"):
        """
        Exportar datasets a Excel para Power BI.
        
        Args:
            datasets: Diccionario con los datasets
            output_path: Ruta del archivo Excel de salida
        """
        logger.info(f"Exportando datasets a Excel: {output_path}")
        
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            for sheet_name, df in datasets.items():
                # Limitar el nombre de la hoja a 31 caracteres (límite de Excel)
                sheet_name = sheet_name[:31]
                df.to_excel(writer, sheet_name=sheet_name, index=False)
                logger.info(f"Hoja '{sheet_name}' exportada: {df.shape[0]} filas, {df.shape[1]} columnas")
        
        logger.info(f"Archivo Excel creado exitosamente: {output_path}")
    
    def export_to_csv(self, datasets: Dict[str, pd.DataFrame], output_dir: str = "data/final/powerbi_csv/"):
        """
        Exportar datasets a archivos CSV separados.
        
        Args:
            datasets: Diccionario con los datasets
            output_dir: Directorio de salida para los archivos CSV
        """
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        logger.info(f"Exportando datasets a CSV en: {output_dir}")
        
        for dataset_name, df in datasets.items():
            csv_path = Path(output_dir) / f"{dataset_name}.csv"
            df.to_csv(csv_path, index=False, encoding='utf-8')
            logger.info(f"CSV '{dataset_name}' exportado: {df.shape[0]} filas, {df.shape[1]} columnas")
        
        logger.info(f"Archivos CSV creados exitosamente en: {output_dir}")
    
    def create_powerbi_queries(self) -> Dict[str, str]:
        """
        Crear consultas SQL optimizadas para Power BI.
        
        Returns:
            Diccionario con las consultas SQL
        """
        queries = {
            'sales_overview': """
                SELECT 
                    DATE(ORDERDATE) as order_date,
                    SUM(SALES) as daily_sales,
                    COUNT(*) as daily_orders,
                    COUNT(DISTINCT CUSTOMERNAME) as daily_customers
                FROM sales_data
                WHERE STATUS != 'Cancelled'
                GROUP BY DATE(ORDERDATE)
                ORDER BY order_date
            """,
            
            'top_customers': """
                SELECT 
                    CUSTOMERNAME,
                    COUNTRY,
                    SUM(SALES) as total_sales,
                    COUNT(*) as order_count,
                    AVG(SALES) as avg_order_value
                FROM sales_data
                WHERE STATUS != 'Cancelled'
                GROUP BY CUSTOMERNAME, COUNTRY
                ORDER BY total_sales DESC
                LIMIT 20
            """,
            
            'product_performance': """
                SELECT 
                    PRODUCTLINE,
                    PRODUCTCODE,
                    SUM(SALES) as total_sales,
                    SUM(QUANTITYORDERED) as total_quantity,
                    COUNT(*) as order_count
                FROM sales_data
                WHERE STATUS != 'Cancelled'
                GROUP BY PRODUCTLINE, PRODUCTCODE
                ORDER BY total_sales DESC
            """,
            
            'geographic_sales': """
                SELECT 
                    COUNTRY,
                    CITY,
                    SUM(SALES) as total_sales,
                    COUNT(*) as order_count,
                    COUNT(DISTINCT CUSTOMERNAME) as unique_customers
                FROM sales_data
                WHERE STATUS != 'Cancelled'
                GROUP BY COUNTRY, CITY
                ORDER BY total_sales DESC
            """,
            
            'monthly_trends': """
                SELECT 
                    YEAR,
                    MONTH,
                    SUM(SALES) as monthly_sales,
                    COUNT(*) as monthly_orders,
                    AVG(SALES) as avg_order_value
                FROM sales_data
                WHERE STATUS != 'Cancelled'
                GROUP BY YEAR, MONTH
                ORDER BY YEAR, MONTH
            """
        }
        
        return queries
    
    def generate_powerbi_guide(self, output_path: str = "data/final/powerbi_guide.md"):
        """
        Generar guía para Power BI.
        
        Args:
            output_path: Ruta del archivo de guía
        """
        guide_content = """# Guía para Power BI - Análisis de Ventas

## 📊 Datasets Disponibles

### 1. **sales_fact** - Tabla Principal de Hechos
- **Descripción**: Datos de ventas detallados
- **Registros**: ~2,800 ventas
- **Columnas clave**: ORDERNUMBER, ORDERDATE, CUSTOMERNAME, PRODUCTCODE, SALES

### 2. **dim_customers** - Dimensión de Clientes
- **Descripción**: Información agregada por cliente
- **Registros**: ~350 clientes únicos
- **Columnas clave**: CUSTOMERNAME, COUNTRY, total_sales, customer_tier

### 3. **dim_products** - Dimensión de Productos
- **Descripción**: Información agregada por producto
- **Registros**: ~100 productos únicos
- **Columnas clave**: PRODUCTCODE, PRODUCTLINE, total_sales, product_tier

### 4. **sales_metrics** - Métricas de Ventas
- **Descripción**: Métricas agregadas por día y mes
- **Registros**: ~200 registros temporales
- **Columnas clave**: date, daily_sales, daily_orders, avg_order_value

## 🎯 Visualizaciones Recomendadas

### Dashboard Principal
1. **KPI Cards**:
   - Total de Ventas
   - Número de Órdenes
   - Clientes Únicos
   - Valor Promedio por Orden

2. **Gráficos de Línea**:
   - Ventas por Mes
   - Órdenes por Día de la Semana
   - Tendencia de Clientes

3. **Gráficos de Barras**:
   - Top 10 Clientes por Ventas
   - Top 10 Productos por Ventas
   - Ventas por País

4. **Mapa**:
   - Ventas por País/Ciudad

### Dashboard de Análisis Detallado
1. **Tabla de Clientes**:
   - Ranking de clientes
   - Métricas por cliente
   - Segmentación

2. **Análisis de Productos**:
   - Performance por línea de producto
   - Cantidad vs. Valor
   - Productos más vendidos

3. **Análisis Temporal**:
   - Patrones estacionales
   - Comparación año a año
   - Análisis por trimestre

## 🔗 Relaciones en Power BI

### Modelo de Datos
```
sales_fact (1) → (1) dim_customers [CUSTOMERNAME]
sales_fact (1) → (1) dim_products [PRODUCTCODE]
sales_fact (1) → (1) dim_dates [ORDERDATE]
sales_fact (1) → (1) dim_countries [COUNTRY]
```

### Configuración de Relaciones
1. **sales_fact.CUSTOMERNAME** → **dim_customers.CUSTOMERNAME**
2. **sales_fact.PRODUCTCODE** → **dim_products.PRODUCTCODE**
3. **sales_fact.ORDERDATE** → **dim_dates.ORDERDATE**
4. **sales_fact.COUNTRY** → **dim_countries.COUNTRY**

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
VAR PreviousSales = CALCULATE([Total Sales], DATEADD(dim_dates[ORDERDATE], -1, MONTH))
RETURN
DIVIDE(CurrentSales - PreviousSales, PreviousSales)

Customer Retention = 
VAR CurrentCustomers = [Unique Customers]
VAR PreviousCustomers = CALCULATE([Unique Customers], DATEADD(dim_dates[ORDERDATE], -1, MONTH))
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
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(guide_content)
        
        logger.info(f"Guía de Power BI generada: {output_path}")
    
    def close_connection(self):
        """Cerrar conexión a la base de datos."""
        if self.connection:
            self.connection.close()
            logger.info("Conexión a la base de datos cerrada")


def main():
    """Función principal para preparar datos para Power BI."""
    print("🚀 Preparando datos para Power BI...")
    
    # Inicializar preparador
    preparator = PowerBIDataPreparator()
    
    try:
        # Conectar a la base de datos
        preparator.connect_db()
        
        # Crear datasets
        datasets = preparator.create_powerbi_datasets()
        
        # Exportar a Excel
        preparator.export_to_excel(datasets)
        
        # Exportar a CSV
        preparator.export_to_csv(datasets)
        
        # Generar guía
        preparator.generate_powerbi_guide()
        
        # Crear consultas SQL
        queries = preparator.create_powerbi_queries()
        
        # Guardar consultas SQL
        queries_path = "data/final/powerbi_queries.json"
        with open(queries_path, 'w', encoding='utf-8') as f:
            json.dump(queries, f, indent=2, ensure_ascii=False)
        
        print("✅ Datos preparados exitosamente para Power BI!")
        print(f"📊 Archivos generados:")
        print(f"   - Excel: data/final/powerbi_data.xlsx")
        print(f"   - CSV: data/final/powerbi_csv/")
        print(f"   - Guía: data/final/powerbi_guide.md")
        print(f"   - Consultas: data/final/powerbi_queries.json")
        
    except Exception as e:
        logger.error(f"Error en la preparación de datos: {e}")
        raise
    finally:
        preparator.close_connection()


if __name__ == "__main__":
    main()

