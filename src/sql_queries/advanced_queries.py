"""
Módulo de consultas SQL avanzadas para análisis de ventas.

Este módulo contiene consultas SQL que demuestran:
- Window Functions (ROW_NUMBER, RANK, DENSE_RANK, LAG, LEAD)
- CTEs (Common Table Expressions)
- Subqueries (correlated, EXISTS, IN)
- Joins avanzados
- Optimización con índices

Autor: [Tu Nombre]
Fecha: [Fecha]
"""

import sqlite3
import pandas as pd
import logging
from typing import Dict, List, Optional, Tuple
from pathlib import Path

# Configurar logging
logger = logging.getLogger(__name__)


class SalesSQLAnalyzer:
    """
    Clase para ejecutar consultas SQL avanzadas en datos de ventas.
    
    Esta clase implementa consultas que demuestran técnicas avanzadas de SQL
    para análisis de datos de ventas.
    """
    
    def __init__(self, db_path: str = "data/processed/sales_analysis.db"):
        """
        Inicializar el analizador SQL.
        
        Args:
            db_path: Ruta a la base de datos SQLite
        """
        self.db_path = db_path
        self.conn: Optional[sqlite3.Connection] = None
        
        logger.info(f"Inicializando SalesSQLAnalyzer con DB en: {db_path}")
    
    def connect_db(self) -> sqlite3.Connection:
        """
        Conectar a la base de datos SQLite.
        
        Returns:
            Conexión a la base de datos
        """
        try:
            self.conn = sqlite3.connect(self.db_path)
            logger.info("Conexión a base de datos establecida")
            return self.conn
        except Exception as e:
            logger.error(f"Error al conectar a la base de datos: {str(e)}")
            raise
    
    def create_tables_from_csv(self, csv_path: str) -> None:
        """
        Crear tablas en SQLite desde archivo CSV.
        
        Args:
            csv_path: Ruta al archivo CSV limpio
        """
        if self.conn is None:
            self.connect_db()
        
        try:
            # Leer CSV
            df = pd.read_csv(csv_path)
            
            # Crear tabla sales_data
            df.to_sql('sales_data', self.conn, if_exists='replace', index=False)
            
            logger.info(f"Tabla sales_data creada con {len(df)} registros")
            
            # Crear índices para optimización
            self._create_indexes()
            
        except Exception as e:
            logger.error(f"Error al crear tablas: {str(e)}")
            raise
    
    def _create_indexes(self) -> None:
        """
        Crear índices para optimizar consultas.
        """
        if self.conn is None:
            return
        
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_orderdate ON sales_data(ORDERDATE)",
            "CREATE INDEX IF NOT EXISTS idx_productline ON sales_data(PRODUCTLINE)",
            "CREATE INDEX IF NOT EXISTS idx_country ON sales_data(COUNTRY)",
            "CREATE INDEX IF NOT EXISTS idx_status ON sales_data(STATUS)",
            "CREATE INDEX IF NOT EXISTS idx_year_month ON sales_data(YEAR_ID, MONTH_ID)",
            "CREATE INDEX IF NOT EXISTS idx_sales ON sales_data(SALES)",
            "CREATE INDEX IF NOT EXISTS idx_customer ON sales_data(CUSTOMERNAME)"
        ]
        
        for index_sql in indexes:
            try:
                self.conn.execute(index_sql)
                logger.info(f"Índice creado: {index_sql}")
            except Exception as e:
                logger.warning(f"No se pudo crear índice: {str(e)}")
        
        self.conn.commit()
    
    def window_functions_demo(self) -> pd.DataFrame:
        """
        Demostrar Window Functions avanzadas.
        
        Returns:
            DataFrame con resultados de Window Functions
        """
        query = """
        WITH sales_ranked AS (
            SELECT 
                ORDERNUMBER,
                CUSTOMERNAME,
                PRODUCTLINE,
                SALES,
                ORDERDATE,
                COUNTRY,
                -- ROW_NUMBER: Número de fila dentro de cada partición
                ROW_NUMBER() OVER (
                    PARTITION BY PRODUCTLINE 
                    ORDER BY SALES DESC
                ) as row_num,
                
                -- RANK: Rango con gaps para valores iguales
                RANK() OVER (
                    PARTITION BY COUNTRY 
                    ORDER BY SALES DESC
                ) as country_rank,
                
                -- DENSE_RANK: Rango sin gaps
                DENSE_RANK() OVER (
                    PARTITION BY YEAR_ID 
                    ORDER BY SALES DESC
                ) as year_dense_rank,
                
                -- LAG: Valor anterior en la secuencia
                LAG(SALES, 1) OVER (
                    PARTITION BY CUSTOMERNAME 
                    ORDER BY ORDERDATE
                ) as prev_sale,
                
                -- LEAD: Valor siguiente en la secuencia
                LEAD(SALES, 1) OVER (
                    PARTITION BY PRODUCTLINE 
                    ORDER BY ORDERDATE
                ) as next_sale,
                
                -- Promedio móvil de 3 períodos
                AVG(SALES) OVER (
                    PARTITION BY PRODUCTLINE 
                    ORDER BY ORDERDATE 
                    ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
                ) as moving_avg_3,
                
                -- Suma acumulativa por cliente
                SUM(SALES) OVER (
                    PARTITION BY CUSTOMERNAME 
                    ORDER BY ORDERDATE
                ) as cumulative_sales,
                
                -- Porcentaje del total por producto
                ROUND(
                    (SALES * 100.0) / SUM(SALES) OVER (PARTITION BY PRODUCTLINE), 
                    2
                ) as pct_of_product_total
                
            FROM sales_data
            WHERE SALES > 0
        )
        SELECT 
            ORDERNUMBER,
            CUSTOMERNAME,
            PRODUCTLINE,
            SALES,
            ORDERDATE,
            COUNTRY,
            row_num,
            country_rank,
            year_dense_rank,
            prev_sale,
            next_sale,
            ROUND(moving_avg_3, 2) as moving_avg_3,
            ROUND(cumulative_sales, 2) as cumulative_sales,
            pct_of_product_total
        FROM sales_ranked
        WHERE row_num <= 5  -- Top 5 por línea de producto
        ORDER BY PRODUCTLINE, SALES DESC
        """
        
        try:
            result = pd.read_sql_query(query, self.conn)
            logger.info(f"Window Functions ejecutadas: {len(result)} registros")
            return result
        except Exception as e:
            logger.error(f"Error en Window Functions: {str(e)}")
            raise
    
    def cte_complex_analysis(self) -> pd.DataFrame:
        """
        Demostrar CTEs complejas para análisis multi-dimensional.
        
        Returns:
            DataFrame con análisis complejo usando CTEs
        """
        query = """
        -- CTE 1: Ventas por cliente y producto
        WITH customer_product_sales AS (
            SELECT 
                CUSTOMERNAME,
                PRODUCTLINE,
                COUNT(*) as order_count,
                SUM(SALES) as total_sales,
                AVG(SALES) as avg_sales,
                MIN(SALES) as min_sale,
                MAX(SALES) as max_sale
            FROM sales_data
            WHERE STATUS = 'Shipped'
            GROUP BY CUSTOMERNAME, PRODUCTLINE
        ),
        
        -- CTE 2: Ranking de clientes por ventas totales
        customer_ranking AS (
            SELECT 
                CUSTOMERNAME,
                SUM(total_sales) as customer_total_sales,
                COUNT(DISTINCT PRODUCTLINE) as products_purchased,
                RANK() OVER (ORDER BY SUM(total_sales) DESC) as customer_rank
            FROM customer_product_sales
            GROUP BY CUSTOMERNAME
        ),
        
        -- CTE 3: Análisis temporal por trimestre
        quarterly_analysis AS (
            SELECT 
                YEAR_ID,
                QTR_ID,
                PRODUCTLINE,
                COUNT(*) as orders,
                SUM(SALES) as quarterly_sales,
                AVG(SALES) as avg_order_value,
                LAG(SUM(SALES)) OVER (
                    PARTITION BY PRODUCTLINE 
                    ORDER BY YEAR_ID, QTR_ID
                ) as prev_quarter_sales
            FROM sales_data
            WHERE STATUS = 'Shipped'
            GROUP BY YEAR_ID, QTR_ID, PRODUCTLINE
        ),
        
        -- CTE 4: Cálculo de crecimiento trimestral
        growth_analysis AS (
            SELECT 
                YEAR_ID,
                QTR_ID,
                PRODUCTLINE,
                orders,
                quarterly_sales,
                avg_order_value,
                prev_quarter_sales,
                CASE 
                    WHEN prev_quarter_sales IS NOT NULL 
                    THEN ROUND(
                        ((quarterly_sales - prev_quarter_sales) / prev_quarter_sales) * 100, 
                        2
                    )
                    ELSE NULL 
                END as qoq_growth_pct
            FROM quarterly_analysis
        )
        
        -- Consulta principal combinando todas las CTEs
        SELECT 
            cr.CUSTOMERNAME,
            cr.customer_total_sales,
            cr.customer_rank,
            cr.products_purchased,
            cps.PRODUCTLINE,
            cps.order_count,
            cps.total_sales as product_sales,
            cps.avg_sales,
            ga.YEAR_ID,
            ga.QTR_ID,
            ga.quarterly_sales,
            ga.qoq_growth_pct
        FROM customer_ranking cr
        INNER JOIN customer_product_sales cps 
            ON cr.CUSTOMERNAME = cps.CUSTOMERNAME
        INNER JOIN growth_analysis ga 
            ON cps.PRODUCTLINE = ga.PRODUCTLINE
        WHERE cr.customer_rank <= 10  -- Top 10 clientes
        ORDER BY cr.customer_rank, cps.total_sales DESC
        """
        
        try:
            result = pd.read_sql_query(query, self.conn)
            logger.info(f"Análisis CTE complejo ejecutado: {len(result)} registros")
            return result
        except Exception as e:
            logger.error(f"Error en análisis CTE: {str(e)}")
            raise
    
    def subqueries_demo(self) -> pd.DataFrame:
        """
        Demostrar diferentes tipos de subqueries.
        
        Returns:
            DataFrame con ejemplos de subqueries
        """
        query = """
        SELECT 
            s1.ORDERNUMBER,
            s1.CUSTOMERNAME,
            s1.PRODUCTLINE,
            s1.SALES,
            s1.ORDERDATE,
            
            -- Subquery escalar: Promedio de ventas por cliente
            (SELECT AVG(SALES) 
             FROM sales_data s2 
             WHERE s2.CUSTOMERNAME = s1.CUSTOMERNAME) as customer_avg_sales,
            
            -- Subquery en WHERE con EXISTS
            CASE 
                WHEN EXISTS (
                    SELECT 1 
                    FROM sales_data s3 
                    WHERE s3.CUSTOMERNAME = s1.CUSTOMERNAME 
                    AND s3.SALES > s1.SALES * 2
                ) THEN 'High Value Customer'
                ELSE 'Regular Customer'
            END as customer_type,
            
            -- Subquery correlacionada: Ranking dentro del cliente
            (SELECT COUNT(*) + 1
             FROM sales_data s4 
             WHERE s4.CUSTOMERNAME = s1.CUSTOMERNAME 
             AND s4.SALES > s1.SALES) as customer_rank,
            
            -- Subquery con IN: Productos comprados por el mismo cliente
            (SELECT COUNT(DISTINCT PRODUCTLINE)
             FROM sales_data s5 
             WHERE s5.CUSTOMERNAME = s1.CUSTOMERNAME) as unique_products,
            
                        -- Subquery con comparación: Comparación con otros clientes
            CASE
                WHEN s1.SALES > (
                    SELECT AVG(SALES)
                    FROM sales_data s6
                    WHERE s6.CUSTOMERNAME != s1.CUSTOMERNAME
                ) THEN 'Above Average'
                ELSE 'Below Average'
            END as performance_category
            
        FROM sales_data s1
        WHERE s1.STATUS = 'Shipped'
        AND s1.SALES > (
            SELECT AVG(SALES) 
            FROM sales_data 
            WHERE STATUS = 'Shipped'
        )
        ORDER BY s1.SALES DESC
        LIMIT 50
        """
        
        try:
            result = pd.read_sql_query(query, self.conn)
            logger.info(f"Subqueries ejecutadas: {len(result)} registros")
            return result
        except Exception as e:
            logger.error(f"Error en subqueries: {str(e)}")
            raise
    
    def advanced_joins_demo(self) -> pd.DataFrame:
        """
        Demostrar joins avanzados y auto-joins.
        
        Returns:
            DataFrame con ejemplos de joins avanzados
        """
        query = """
        WITH customer_summary AS (
            SELECT 
                CUSTOMERNAME,
                COUNTRY,
                COUNT(*) as total_orders,
                SUM(SALES) as total_sales,
                AVG(SALES) as avg_order_value
            FROM sales_data
            GROUP BY CUSTOMERNAME, COUNTRY
        ),
        
        product_summary AS (
            SELECT 
                PRODUCTLINE,
                COUNT(*) as total_orders,
                SUM(SALES) as total_revenue,
                AVG(SALES) as avg_price
            FROM sales_data
            GROUP BY PRODUCTLINE
        )
        
        SELECT 
            cs.CUSTOMERNAME,
            cs.COUNTRY,
            cs.total_orders as customer_orders,
            cs.total_sales as customer_sales,
            cs.avg_order_value,
            
            -- Self join para comparar con otros clientes del mismo país
            COUNT(cs2.CUSTOMERNAME) as country_customers,
            AVG(cs2.total_sales) as country_avg_sales,
            
            -- Cross join para calcular métricas por producto
            ps.PRODUCTLINE,
            ps.total_revenue as product_revenue,
            ps.avg_price,
            
            -- Cálculo de participación en el mercado
            ROUND(
                (cs.total_sales * 100.0) / SUM(cs.total_sales) OVER (PARTITION BY cs.COUNTRY), 
                2
            ) as market_share_pct,
            
            -- Comparación con promedio del país
            CASE 
                WHEN cs.total_sales > AVG(cs.total_sales) OVER (PARTITION BY cs.COUNTRY)
                THEN 'Above Country Average'
                ELSE 'Below Country Average'
            END as country_performance
            
        FROM customer_summary cs
        
        -- Self join para comparar clientes del mismo país
        LEFT JOIN customer_summary cs2 
            ON cs.COUNTRY = cs2.COUNTRY 
            AND cs.CUSTOMERNAME != cs2.CUSTOMERNAME
        
        -- Cross join con resumen de productos
        CROSS JOIN product_summary ps
        
        WHERE cs.total_sales > (
            SELECT AVG(total_sales) 
            FROM customer_summary
        )
        
        GROUP BY cs.CUSTOMERNAME, cs.COUNTRY, cs.total_orders, 
                 cs.total_sales, cs.avg_order_value, ps.PRODUCTLINE,
                 ps.total_revenue, ps.avg_price
        
        ORDER BY cs.total_sales DESC
        LIMIT 30
        """
        
        try:
            result = pd.read_sql_query(query, self.conn)
            logger.info(f"Joins avanzados ejecutados: {len(result)} registros")
            return result
        except Exception as e:
            logger.error(f"Error en joins avanzados: {str(e)}")
            raise
    
    def performance_optimization_demo(self) -> Dict[str, any]:
        """
        Demostrar técnicas de optimización de consultas.
        
        Returns:
            Diccionario con métricas de performance
        """
        if self.conn is None:
            self.connect_db()
        
        # Habilitar timing
        self.conn.execute("PRAGMA timer = ON")
        
        performance_results = {}
        
        # Query 1: Sin optimización
        start_time = pd.Timestamp.now()
        query1 = """
        SELECT 
            CUSTOMERNAME,
            PRODUCTLINE,
            COUNT(*) as orders,
            SUM(SALES) as total_sales
        FROM sales_data
        WHERE STATUS = 'Shipped'
        GROUP BY CUSTOMERNAME, PRODUCTLINE
        ORDER BY total_sales DESC
        """
        
        result1 = pd.read_sql_query(query1, self.conn)
        end_time = pd.Timestamp.now()
        performance_results['query1_time'] = (end_time - start_time).total_seconds()
        performance_results['query1_rows'] = len(result1)
        
        # Query 2: Con optimización (usando índices y CTEs)
        start_time = pd.Timestamp.now()
        query2 = """
        WITH optimized_sales AS (
            SELECT 
                CUSTOMERNAME,
                PRODUCTLINE,
                SALES
            FROM sales_data
            WHERE STATUS = 'Shipped'
            AND SALES > 0
        )
        SELECT 
            CUSTOMERNAME,
            PRODUCTLINE,
            COUNT(*) as orders,
            SUM(SALES) as total_sales
        FROM optimized_sales
        GROUP BY CUSTOMERNAME, PRODUCTLINE
        ORDER BY total_sales DESC
        """
        
        result2 = pd.read_sql_query(query2, self.conn)
        end_time = pd.Timestamp.now()
        performance_results['query2_time'] = (end_time - start_time).total_seconds()
        performance_results['query2_rows'] = len(result2)
        
        # Calcular mejora de performance
        if performance_results['query1_time'] > 0:
            improvement = (
                (performance_results['query1_time'] - performance_results['query2_time']) 
                / performance_results['query1_time'] * 100
            )
            performance_results['improvement_pct'] = round(improvement, 2)
        
        logger.info(f"Análisis de performance completado: {performance_results}")
        return performance_results
    
    def get_query_plan(self, query: str) -> pd.DataFrame:
        """
        Obtener el plan de ejecución de una consulta.
        
        Args:
            query: Consulta SQL a analizar
            
        Returns:
            DataFrame con el plan de ejecución
        """
        if self.conn is None:
            self.connect_db()
        
        try:
            # Obtener plan de ejecución
            plan_query = f"EXPLAIN QUERY PLAN {query}"
            plan_result = pd.read_sql_query(plan_query, self.conn)
            
            logger.info("Plan de ejecución obtenido")
            return plan_result
        except Exception as e:
            logger.error(f"Error al obtener plan de ejecución: {str(e)}")
            raise
    
    def close_connection(self) -> None:
        """
        Cerrar conexión a la base de datos.
        """
        if self.conn:
            self.conn.close()
            logger.info("Conexión a base de datos cerrada")


def main():
    """
    Función principal para ejecutar todas las consultas SQL avanzadas.
    """
    try:
        # Inicializar analizador
        analyzer = SalesSQLAnalyzer()
        
        # Crear tablas desde CSV limpio
        csv_path = "data/processed/sales_data_cleaned.csv"
        analyzer.create_tables_from_csv(csv_path)
        
        # Ejecutar todas las consultas de demostración
        print("\n=== WINDOW FUNCTIONS DEMO ===")
        window_results = analyzer.window_functions_demo()
        print(f"Window Functions: {len(window_results)} registros")
        print(window_results.head())
        
        print("\n=== CTE COMPLEX ANALYSIS ===")
        cte_results = analyzer.cte_complex_analysis()
        print(f"CTE Analysis: {len(cte_results)} registros")
        print(cte_results.head())
        
        print("\n=== SUBQUERIES DEMO ===")
        subquery_results = analyzer.subqueries_demo()
        print(f"Subqueries: {len(subquery_results)} registros")
        print(subquery_results.head())
        
        print("\n=== ADVANCED JOINS DEMO ===")
        joins_results = analyzer.advanced_joins_demo()
        print(f"Advanced Joins: {len(joins_results)} registros")
        print(joins_results.head())
        
        print("\n=== PERFORMANCE OPTIMIZATION ===")
        perf_results = analyzer.performance_optimization_demo()
        print(f"Performance Results: {perf_results}")
        
        # Cerrar conexión
        analyzer.close_connection()
        
        logger.info("Todas las consultas SQL avanzadas ejecutadas exitosamente")
        
    except Exception as e:
        logger.error(f"Error en ejecución de consultas SQL: {str(e)}")
        raise


if __name__ == "__main__":
    main()
