"""
Módulo de análisis exploratorio de datos de ventas.

Este módulo contiene funciones para realizar análisis exploratorio
completo con visualizaciones avanzadas usando matplotlib, seaborn y plotly.

Autor: [Tu Nombre]
Fecha: [Fecha]
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import logging
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import warnings

# Configurar logging
logger = logging.getLogger(__name__)

# Configurar estilo de matplotlib y seaborn
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")
warnings.filterwarnings('ignore')

# Configurar plotly para modo offline
import plotly.offline as pyo
pyo.init_notebook_mode(connected=True)


class SalesExploratoryAnalyzer:
    """
    Clase para realizar análisis exploratorio completo de datos de ventas.
    
    Esta clase implementa métodos para:
    - Análisis estadístico descriptivo
    - Visualizaciones temporales
    - Análisis de productos y clientes
    - Correlaciones y patrones
    - Generación de reportes
    """
    
    def __init__(self, data_path: str):
        """
        Inicializar el analizador exploratorio.
        
        Args:
            data_path: Ruta al archivo CSV limpio
        """
        self.data_path = Path(data_path)
        self.df: Optional[pd.DataFrame] = None
        self.analysis_results: Dict = {}
        
        logger.info(f"Inicializando SalesExploratoryAnalyzer con datos en: {data_path}")
    
    def load_data(self) -> pd.DataFrame:
        """
        Cargar datos limpios para análisis.
        
        Returns:
            DataFrame con los datos cargados
        """
        try:
            logger.info("Cargando datos para análisis exploratorio...")
            self.df = pd.read_csv(self.data_path)
            
            # Convertir columnas de fecha si existen
            date_columns = [col for col in self.df.columns if 'DATE' in col.upper()]
            for col in date_columns:
                self.df[col] = pd.to_datetime(self.df[col], errors='coerce')
            
            logger.info(f"Datos cargados: {self.df.shape[0]} filas, {self.df.shape[1]} columnas")
            return self.df
            
        except Exception as e:
            logger.error(f"Error al cargar datos: {str(e)}")
            raise
    
    def basic_statistics(self) -> Dict:
        """
        Calcular estadísticas básicas del dataset.
        
        Returns:
            Diccionario con estadísticas descriptivas
        """
        if self.df is None:
            raise ValueError("No hay datos cargados")
        
        logger.info("Calculando estadísticas básicas...")
        
        # Estadísticas numéricas
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        stats = {
            'dataset_info': {
                'total_rows': len(self.df),
                'total_columns': len(self.df.columns),
                'numeric_columns': len(numeric_cols),
                'categorical_columns': len(self.df.select_dtypes(include=['object', 'category']).columns)
            },
            'numeric_summary': self.df[numeric_cols].describe().to_dict(),
            'missing_values': self.df.isnull().sum().to_dict(),
            'unique_values': {col: self.df[col].nunique() for col in self.df.columns}
        }
        
        # Estadísticas específicas de ventas
        if 'SALES' in self.df.columns:
            sales_stats = {
                'total_sales': self.df['SALES'].sum(),
                'avg_sales': self.df['SALES'].mean(),
                'median_sales': self.df['SALES'].median(),
                'sales_std': self.df['SALES'].std(),
                'min_sales': self.df['SALES'].min(),
                'max_sales': self.df['SALES'].max(),
                'sales_skewness': self.df['SALES'].skew(),
                'sales_kurtosis': self.df['SALES'].kurtosis()
            }
            stats['sales_statistics'] = sales_stats
        
        self.analysis_results['basic_statistics'] = stats
        logger.info("Estadísticas básicas calculadas")
        return stats
    
    def temporal_analysis(self, save_plots: bool = True) -> Dict:
        """
        Análisis temporal de las ventas.
        
        Args:
            save_plots: Si guardar las visualizaciones
            
        Returns:
            Diccionario con análisis temporal
        """
        if self.df is None:
            raise ValueError("No hay datos cargados")
        
        logger.info("Realizando análisis temporal...")
        
        # Preparar datos temporales
        if 'ORDERDATE' in self.df.columns:
            df_temp = self.df.copy()
            df_temp['ORDERDATE'] = pd.to_datetime(df_temp['ORDERDATE'])
            df_temp['YEAR'] = df_temp['ORDERDATE'].dt.year
            df_temp['MONTH'] = df_temp['ORDERDATE'].dt.month
            df_temp['QUARTER'] = df_temp['ORDERDATE'].dt.quarter
            df_temp['DAY_OF_WEEK'] = df_temp['ORDERDATE'].dt.dayofweek
            df_temp['DAY_NAME'] = df_temp['ORDERDATE'].dt.day_name()
        else:
            logger.warning("No se encontró columna ORDERDATE para análisis temporal")
            return {}
        
        temporal_results = {}
        
        # 1. Ventas por año
        yearly_sales = df_temp.groupby('YEAR')['SALES'].agg(['sum', 'mean', 'count']).reset_index()
        temporal_results['yearly_sales'] = yearly_sales.to_dict('records')
        
        # 2. Ventas por mes
        monthly_sales = df_temp.groupby(['YEAR', 'MONTH'])['SALES'].sum().reset_index()
        temporal_results['monthly_sales'] = monthly_sales.to_dict('records')
        
        # 3. Ventas por día de la semana
        dow_sales = df_temp.groupby('DAY_NAME')['SALES'].agg(['sum', 'mean', 'count']).reset_index()
        temporal_results['day_of_week_sales'] = dow_sales.to_dict('records')
        
        # Crear visualizaciones
        if save_plots:
            self._create_temporal_visualizations(df_temp)
        
        self.analysis_results['temporal_analysis'] = temporal_results
        logger.info("Análisis temporal completado")
        return temporal_results
    
    def _create_temporal_visualizations(self, df_temp: pd.DataFrame) -> None:
        """
        Crear visualizaciones temporales.
        
        Args:
            df_temp: DataFrame con datos temporales
        """
        # Configurar figura
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Análisis Temporal de Ventas', fontsize=16, fontweight='bold')
        
        # 1. Ventas por año
        yearly_sales = df_temp.groupby('YEAR')['SALES'].sum()
        axes[0, 0].bar(yearly_sales.index, yearly_sales.values, color='skyblue', alpha=0.7)
        axes[0, 0].set_title('Ventas Totales por Año')
        axes[0, 0].set_xlabel('Año')
        axes[0, 0].set_ylabel('Ventas Totales ($)')
        axes[0, 0].grid(True, alpha=0.3)
        
        # 2. Ventas por mes (promedio)
        monthly_avg = df_temp.groupby('MONTH')['SALES'].mean()
        axes[0, 1].plot(monthly_avg.index, monthly_avg.values, marker='o', linewidth=2, color='orange')
        axes[0, 1].set_title('Promedio de Ventas por Mes')
        axes[0, 1].set_xlabel('Mes')
        axes[0, 1].set_ylabel('Ventas Promedio ($)')
        axes[0, 1].grid(True, alpha=0.3)
        
        # 3. Ventas por día de la semana
        dow_sales = df_temp.groupby('DAY_NAME')['SALES'].sum()
        dow_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        dow_sales_ordered = dow_sales.reindex(dow_order)
        axes[1, 0].bar(range(len(dow_sales_ordered)), dow_sales_ordered.values, color='lightgreen', alpha=0.7)
        axes[1, 0].set_title('Ventas por Día de la Semana')
        axes[1, 0].set_xlabel('Día de la Semana')
        axes[1, 0].set_ylabel('Ventas Totales ($)')
        axes[1, 0].set_xticks(range(len(dow_order)))
        axes[1, 0].set_xticklabels([d[:3] for d in dow_order], rotation=45)
        axes[1, 0].grid(True, alpha=0.3)
        
        # 4. Serie temporal de ventas
        df_temp_sorted = df_temp.sort_values('ORDERDATE')
        monthly_timeline = df_temp_sorted.groupby(df_temp_sorted['ORDERDATE'].dt.to_period('M'))['SALES'].sum()
        axes[1, 1].plot(range(len(monthly_timeline)), monthly_timeline.values, linewidth=2, color='red')
        axes[1, 1].set_title('Serie Temporal de Ventas Mensuales')
        axes[1, 1].set_xlabel('Período')
        axes[1, 1].set_ylabel('Ventas Mensuales ($)')
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Guardar figura
        output_path = Path("data/final/temporal_analysis.png")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Visualizaciones temporales guardadas en: {output_path}")
    
    def product_analysis(self, save_plots: bool = True) -> Dict:
        """
        Análisis de productos y líneas de producto.
        
        Args:
            save_plots: Si guardar las visualizaciones
            
        Returns:
            Diccionario con análisis de productos
        """
        if self.df is None:
            raise ValueError("No hay datos cargados")
        
        logger.info("Realizando análisis de productos...")
        
        product_results = {}
        
        # Análisis por línea de producto
        if 'PRODUCTLINE' in self.df.columns:
            productline_analysis = self.df.groupby('PRODUCTLINE').agg({
                'SALES': ['sum', 'mean', 'count'],
                'QUANTITYORDERED': ['sum', 'mean'],
                'PRICEEACH': ['mean', 'std']
            }).round(2)
            
            product_results['productline_summary'] = productline_analysis.to_dict()
            
            # Top productos por ventas
            if 'PRODUCTCODE' in self.df.columns:
                top_products = self.df.groupby('PRODUCTCODE').agg({
                    'SALES': 'sum',
                    'QUANTITYORDERED': 'sum',
                    'PRODUCTLINE': 'first'
                }).sort_values('SALES', ascending=False).head(10)
                
                product_results['top_products'] = top_products.to_dict('index')
        
        # Crear visualizaciones
        if save_plots:
            self._create_product_visualizations()
        
        self.analysis_results['product_analysis'] = product_results
        logger.info("Análisis de productos completado")
        return product_results
    
    def _create_product_visualizations(self) -> None:
        """
        Crear visualizaciones de análisis de productos.
        """
        # Configurar figura
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Análisis de Productos', fontsize=16, fontweight='bold')
        
        # 1. Ventas por línea de producto
        productline_sales = self.df.groupby('PRODUCTLINE')['SALES'].sum().sort_values(ascending=True)
        axes[0, 0].barh(range(len(productline_sales)), productline_sales.values, color='coral', alpha=0.7)
        axes[0, 0].set_yticks(range(len(productline_sales)))
        axes[0, 0].set_yticklabels(productline_sales.index)
        axes[0, 0].set_title('Ventas Totales por Línea de Producto')
        axes[0, 0].set_xlabel('Ventas Totales ($)')
        axes[0, 0].grid(True, alpha=0.3)
        
        # 2. Distribución de precios por línea de producto
        if 'PRICEEACH' in self.df.columns:
            self.df.boxplot(column='PRICEEACH', by='PRODUCTLINE', ax=axes[0, 1])
            axes[0, 1].set_title('Distribución de Precios por Línea de Producto')
            axes[0, 1].set_xlabel('Línea de Producto')
            axes[0, 1].set_ylabel('Precio Unitario ($)')
            axes[0, 1].tick_params(axis='x', rotation=45)
        
        # 3. Cantidad vs Precio (scatter plot)
        if 'QUANTITYORDERED' in self.df.columns and 'PRICEEACH' in self.df.columns:
            axes[1, 0].scatter(self.df['QUANTITYORDERED'], self.df['PRICEEACH'], 
                             alpha=0.6, c=self.df['SALES'], cmap='viridis')
            axes[1, 0].set_title('Cantidad vs Precio (coloreado por ventas)')
            axes[1, 0].set_xlabel('Cantidad Ordenada')
            axes[1, 0].set_ylabel('Precio Unitario ($)')
            axes[1, 0].grid(True, alpha=0.3)
        
        # 4. Top 10 productos por ventas
        if 'PRODUCTCODE' in self.df.columns:
            top_products = self.df.groupby('PRODUCTCODE')['SALES'].sum().sort_values(ascending=False).head(10)
            axes[1, 1].bar(range(len(top_products)), top_products.values, color='gold', alpha=0.7)
            axes[1, 1].set_title('Top 10 Productos por Ventas')
            axes[1, 1].set_xlabel('Producto')
            axes[1, 1].set_ylabel('Ventas Totales ($)')
            axes[1, 1].set_xticks(range(len(top_products)))
            axes[1, 1].set_xticklabels([code[:8] + '...' for code in top_products.index], rotation=45)
            axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Guardar figura
        output_path = Path("data/final/product_analysis.png")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Visualizaciones de productos guardadas en: {output_path}")
    
    def customer_analysis(self, save_plots: bool = True) -> Dict:
        """
        Análisis de clientes y comportamiento de compra.
        
        Args:
            save_plots: Si guardar las visualizaciones
            
        Returns:
            Diccionario con análisis de clientes
        """
        if self.df is None:
            raise ValueError("No hay datos cargados")
        
        logger.info("Realizando análisis de clientes...")
        
        customer_results = {}
        
        # Análisis por cliente
        if 'CUSTOMERNAME' in self.df.columns:
            customer_analysis = self.df.groupby('CUSTOMERNAME').agg({
                'SALES': ['sum', 'mean', 'count'],
                'QUANTITYORDERED': 'sum',
                'PRODUCTLINE': 'nunique'
            }).round(2)
            
            customer_results['customer_summary'] = customer_analysis.to_dict()
            
            # Top clientes
            top_customers = self.df.groupby('CUSTOMERNAME')['SALES'].sum().sort_values(ascending=False).head(10)
            customer_results['top_customers'] = top_customers.to_dict()
        
        # Análisis geográfico
        if 'COUNTRY' in self.df.columns:
            country_analysis = self.df.groupby('COUNTRY').agg({
                'SALES': ['sum', 'mean', 'count'],
                'CUSTOMERNAME': 'nunique'
            }).round(2)
            
            customer_results['country_analysis'] = country_analysis.to_dict()
        
        # Crear visualizaciones
        if save_plots:
            self._create_customer_visualizations()
        
        self.analysis_results['customer_analysis'] = customer_results
        logger.info("Análisis de clientes completado")
        return customer_results
    
    def _create_customer_visualizations(self) -> None:
        """
        Crear visualizaciones de análisis de clientes.
        """
        # Configurar figura
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Análisis de Clientes', fontsize=16, fontweight='bold')
        
        # 1. Top 10 clientes por ventas
        if 'CUSTOMERNAME' in self.df.columns:
            top_customers = self.df.groupby('CUSTOMERNAME')['SALES'].sum().sort_values(ascending=True).tail(10)
            axes[0, 0].barh(range(len(top_customers)), top_customers.values, color='lightblue', alpha=0.7)
            axes[0, 0].set_yticks(range(len(top_customers)))
            axes[0, 0].set_yticklabels([name[:20] + '...' if len(name) > 20 else name for name in top_customers.index])
            axes[0, 0].set_title('Top 10 Clientes por Ventas')
            axes[0, 0].set_xlabel('Ventas Totales ($)')
            axes[0, 0].grid(True, alpha=0.3)
        
        # 2. Distribución de ventas por cliente
        if 'CUSTOMERNAME' in self.df.columns:
            customer_sales = self.df.groupby('CUSTOMERNAME')['SALES'].sum()
            axes[0, 1].hist(customer_sales, bins=30, color='lightgreen', alpha=0.7, edgecolor='black')
            axes[0, 1].set_title('Distribución de Ventas por Cliente')
            axes[0, 1].set_xlabel('Ventas Totales ($)')
            axes[0, 1].set_ylabel('Número de Clientes')
            axes[0, 1].grid(True, alpha=0.3)
        
        # 3. Ventas por país
        if 'COUNTRY' in self.df.columns:
            country_sales = self.df.groupby('COUNTRY')['SALES'].sum().sort_values(ascending=True)
            axes[1, 0].barh(range(len(country_sales)), country_sales.values, color='orange', alpha=0.7)
            axes[1, 0].set_yticks(range(len(country_sales)))
            axes[1, 0].set_yticklabels(country_sales.index)
            axes[1, 0].set_title('Ventas Totales por País')
            axes[1, 0].set_xlabel('Ventas Totales ($)')
            axes[1, 0].grid(True, alpha=0.3)
        
        # 4. Relación entre número de órdenes y ventas totales
        if 'CUSTOMERNAME' in self.df.columns:
            customer_orders = self.df.groupby('CUSTOMERNAME').agg({
                'SALES': 'sum',
                'ORDERNUMBER': 'nunique'
            })
            axes[1, 1].scatter(customer_orders['ORDERNUMBER'], customer_orders['SALES'], 
                             alpha=0.6, color='purple')
            axes[1, 1].set_title('Número de Órdenes vs Ventas Totales')
            axes[1, 1].set_xlabel('Número de Órdenes')
            axes[1, 1].set_ylabel('Ventas Totales ($)')
            axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Guardar figura
        output_path = Path("data/final/customer_analysis.png")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Visualizaciones de clientes guardadas en: {output_path}")
    
    def correlation_analysis(self, save_plots: bool = True) -> Dict:
        """
        Análisis de correlaciones entre variables.
        
        Args:
            save_plots: Si guardar las visualizaciones
            
        Returns:
            Diccionario con análisis de correlaciones
        """
        if self.df is None:
            raise ValueError("No hay datos cargados")
        
        logger.info("Realizando análisis de correlaciones...")
        
        # Seleccionar variables numéricas
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        correlation_matrix = self.df[numeric_cols].corr()
        
        correlation_results = {
            'correlation_matrix': correlation_matrix.to_dict(),
            'sales_correlations': correlation_matrix['SALES'].sort_values(ascending=False).to_dict()
        }
        
        # Crear visualización
        if save_plots:
            self._create_correlation_visualization(correlation_matrix)
        
        self.analysis_results['correlation_analysis'] = correlation_results
        logger.info("Análisis de correlaciones completado")
        return correlation_results
    
    def _create_correlation_visualization(self, correlation_matrix: pd.DataFrame) -> None:
        """
        Crear visualización de matriz de correlación.
        
        Args:
            correlation_matrix: Matriz de correlación
        """
        plt.figure(figsize=(10, 8))
        
        # Crear heatmap
        mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))
        sns.heatmap(correlation_matrix, mask=mask, annot=True, cmap='coolwarm', 
                   center=0, square=True, linewidths=0.5, cbar_kws={"shrink": .8})
        
        plt.title('Matriz de Correlación de Variables Numéricas', fontsize=14, fontweight='bold')
        plt.tight_layout()
        
        # Guardar figura
        output_path = Path("data/final/correlation_analysis.png")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Visualización de correlaciones guardada en: {output_path}")
    
    def create_interactive_dashboard(self) -> None:
        """
        Crear dashboard interactivo con Plotly.
        """
        if self.df is None:
            raise ValueError("No hay datos cargados")
        
        logger.info("Creando dashboard interactivo...")
        
        # Crear subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Ventas por Línea de Producto', 'Ventas Temporales',
                          'Top Clientes', 'Distribución de Ventas'),
            specs=[[{"type": "bar"}, {"type": "scatter"}],
                   [{"type": "bar"}, {"type": "histogram"}]]
        )
        
        # 1. Ventas por línea de producto
        if 'PRODUCTLINE' in self.df.columns:
            productline_sales = self.df.groupby('PRODUCTLINE')['SALES'].sum()
            fig.add_trace(
                go.Bar(x=productline_sales.values, y=productline_sales.index, 
                      orientation='h', name='Ventas por Producto'),
                row=1, col=1
            )
        
        # 2. Serie temporal de ventas
        if 'ORDERDATE' in self.df.columns:
            df_temp = self.df.copy()
            df_temp['ORDERDATE'] = pd.to_datetime(df_temp['ORDERDATE'])
            monthly_sales = df_temp.groupby(df_temp['ORDERDATE'].dt.to_period('M'))['SALES'].sum()
            
            fig.add_trace(
                go.Scatter(x=list(range(len(monthly_sales))), y=monthly_sales.values,
                          mode='lines+markers', name='Ventas Mensuales'),
                row=1, col=2
            )
        
        # 3. Top clientes
        if 'CUSTOMERNAME' in self.df.columns:
            top_customers = self.df.groupby('CUSTOMERNAME')['SALES'].sum().sort_values(ascending=False).head(10)
            fig.add_trace(
                go.Bar(x=list(range(len(top_customers))), y=top_customers.values,
                      name='Top Clientes'),
                row=2, col=1
            )
        
        # 4. Distribución de ventas
        if 'SALES' in self.df.columns:
            fig.add_trace(
                go.Histogram(x=self.df['SALES'], nbinsx=30, name='Distribución de Ventas'),
                row=2, col=2
            )
        
        # Actualizar layout
        fig.update_layout(
            title_text="Dashboard Interactivo de Análisis de Ventas",
            showlegend=False,
            height=800
        )
        
        # Guardar dashboard
        output_path = Path("data/final/interactive_dashboard.html")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        fig.write_html(str(output_path))
        
        logger.info(f"Dashboard interactivo guardado en: {output_path}")
    
    def generate_analysis_report(self) -> str:
        """
        Generar reporte completo del análisis exploratorio.
        
        Returns:
            Ruta al archivo de reporte generado
        """
        if not self.analysis_results:
            raise ValueError("No hay resultados de análisis disponibles")
        
        logger.info("Generando reporte de análisis...")
        
        report_content = []
        report_content.append("# REPORTE DE ANÁLISIS EXPLORATORIO DE VENTAS")
        report_content.append("=" * 50)
        report_content.append("")
        
        # Resumen ejecutivo
        report_content.append("## RESUMEN EJECUTIVO")
        report_content.append("")
        
        if 'basic_statistics' in self.analysis_results:
            stats = self.analysis_results['basic_statistics']
            report_content.append(f"- **Total de registros**: {stats['dataset_info']['total_rows']:,}")
            report_content.append(f"- **Total de columnas**: {stats['dataset_info']['total_columns']}")
            report_content.append(f"- **Columnas numéricas**: {stats['dataset_info']['numeric_columns']}")
            report_content.append(f"- **Columnas categóricas**: {stats['dataset_info']['categorical_columns']}")
            report_content.append("")
        
        # Insights clave
        report_content.append("## INSIGHTS CLAVE")
        report_content.append("")
        
        # Insights de productos
        if 'product_analysis' in self.analysis_results:
            report_content.append("### Productos")
            product_stats = self.analysis_results['product_analysis']
            if 'productline_summary' in product_stats:
                report_content.append("- Análisis de líneas de producto completado")
                report_content.append("- Identificados productos de mayor rendimiento")
            report_content.append("")
        
        # Insights de clientes
        if 'customer_analysis' in self.analysis_results:
            report_content.append("### Clientes")
            customer_stats = self.analysis_results['customer_analysis']
            if 'top_customers' in customer_stats:
                report_content.append("- Identificados clientes de mayor valor")
                report_content.append("- Análisis geográfico completado")
            report_content.append("")
        
        # Insights temporales
        if 'temporal_analysis' in self.analysis_results:
            report_content.append("### Análisis Temporal")
            report_content.append("- Patrones estacionales identificados")
            report_content.append("- Tendencias de crecimiento analizadas")
            report_content.append("")
        
        # Recomendaciones
        report_content.append("## RECOMENDACIONES")
        report_content.append("")
        report_content.append("1. **Enfoque en productos de alto rendimiento**")
        report_content.append("2. **Desarrollo de estrategias para clientes VIP**")
        report_content.append("3. **Optimización de precios basada en análisis de correlación**")
        report_content.append("4. **Planificación estacional de inventario**")
        report_content.append("")
        
        # Guardar reporte
        output_path = Path("data/final/analysis_report.md")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report_content))
        
        logger.info(f"Reporte de análisis guardado en: {output_path}")
        return str(output_path)


def main():
    """
    Función principal para ejecutar el análisis exploratorio completo.
    """
    try:
        # Inicializar analizador
        analyzer = SalesExploratoryAnalyzer("data/processed/sales_data_cleaned.csv")
        
        # Cargar datos
        analyzer.load_data()
        
        # Ejecutar análisis completo
        print("=== ANÁLISIS EXPLORATORIO DE VENTAS ===")
        
        print("\n1. Estadísticas básicas...")
        basic_stats = analyzer.basic_statistics()
        print(f"   - Dataset: {basic_stats['dataset_info']['total_rows']:,} registros")
        
        print("\n2. Análisis temporal...")
        temporal_results = analyzer.temporal_analysis()
        print("   - Visualizaciones temporales creadas")
        
        print("\n3. Análisis de productos...")
        product_results = analyzer.product_analysis()
        print("   - Análisis de productos completado")
        
        print("\n4. Análisis de clientes...")
        customer_results = analyzer.customer_analysis()
        print("   - Análisis de clientes completado")
        
        print("\n5. Análisis de correlaciones...")
        correlation_results = analyzer.correlation_analysis()
        print("   - Matriz de correlación generada")
        
        print("\n6. Dashboard interactivo...")
        analyzer.create_interactive_dashboard()
        print("   - Dashboard interactivo creado")
        
        print("\n7. Generando reporte...")
        report_path = analyzer.generate_analysis_report()
        print(f"   - Reporte guardado en: {report_path}")
        
        print("\n✅ Análisis exploratorio completado exitosamente!")
        print("\n📊 Archivos generados:")
        print("   - data/final/temporal_analysis.png")
        print("   - data/final/product_analysis.png")
        print("   - data/final/customer_analysis.png")
        print("   - data/final/correlation_analysis.png")
        print("   - data/final/interactive_dashboard.html")
        print("   - data/final/analysis_report.md")
        
    except Exception as e:
        logger.error(f"Error en análisis exploratorio: {str(e)}")
        raise


if __name__ == "__main__":
    main()
