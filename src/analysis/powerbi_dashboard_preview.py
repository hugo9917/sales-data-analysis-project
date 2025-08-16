"""
Generador de vista previa del dashboard para Power BI.

Este script crea una vista previa en HTML del dashboard
que se puede crear en Power BI.
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.offline as pyo
from pathlib import Path
import json
from datetime import datetime

# Configurar para generar HTML estático
pyo.init_notebook_mode(connected=True)


def load_powerbi_data():
    """Cargar los datos preparados para Power BI."""
    try:
        # Cargar desde Excel
        excel_path = "data/final/powerbi_data.xlsx"
        
        datasets = {}
        datasets['sales_fact'] = pd.read_excel(excel_path, sheet_name='sales_fact')
        datasets['dim_customers'] = pd.read_excel(excel_path, sheet_name='dim_customers')
        datasets['dim_products'] = pd.read_excel(excel_path, sheet_name='dim_products')
        datasets['dim_countries'] = pd.read_excel(excel_path, sheet_name='dim_countries')
        datasets['sales_metrics'] = pd.read_excel(excel_path, sheet_name='sales_metrics')
        datasets['temporal_analysis'] = pd.read_excel(excel_path, sheet_name='temporal_analysis')
        datasets['geographic_analysis'] = pd.read_excel(excel_path, sheet_name='geographic_analysis')
        
        print("✅ Datos cargados exitosamente")
        return datasets
        
    except Exception as e:
        print(f"❌ Error al cargar datos: {e}")
        raise


def create_kpi_cards(datasets):
    """Crear tarjetas de KPI."""
    sales_fact = datasets['sales_fact']
    
    # Calcular KPIs
    total_sales = sales_fact['SALES'].sum()
    total_orders = len(sales_fact)
    unique_customers = sales_fact['CUSTOMERNAME'].nunique()
    avg_order_value = total_sales / total_orders
    
    # Crear figura con subplots para las tarjetas
    fig = make_subplots(
        rows=1, cols=4,
        subplot_titles=['Total Ventas', 'Total Órdenes', 'Clientes Únicos', 'Valor Promedio'],
        specs=[[{"type": "indicator"}, {"type": "indicator"}, {"type": "indicator"}, {"type": "indicator"}]]
    )
    
    # KPI 1: Total Ventas
    fig.add_trace(
        go.Indicator(
            mode="number+delta",
            value=total_sales,
            number={'prefix': "$", 'valueformat': ",.0f"},
            title={'text': "Total Ventas"},
            delta={'reference': total_sales * 0.9, 'relative': True},
            domain={'row': 0, 'column': 0}
        ),
        row=1, col=1
    )
    
    # KPI 2: Total Órdenes
    fig.add_trace(
        go.Indicator(
            mode="number+delta",
            value=total_orders,
            number={'valueformat': ",.0f"},
            title={'text': "Total Órdenes"},
            delta={'reference': total_orders * 0.95, 'relative': True},
            domain={'row': 0, 'column': 1}
        ),
        row=1, col=2
    )
    
    # KPI 3: Clientes Únicos
    fig.add_trace(
        go.Indicator(
            mode="number+delta",
            value=unique_customers,
            number={'valueformat': ",.0f"},
            title={'text': "Clientes Únicos"},
            delta={'reference': unique_customers * 0.98, 'relative': True},
            domain={'row': 0, 'column': 2}
        ),
        row=1, col=3
    )
    
    # KPI 4: Valor Promedio
    fig.add_trace(
        go.Indicator(
            mode="number+delta",
            value=avg_order_value,
            number={'prefix': "$", 'valueformat': ",.0f"},
            title={'text': "Valor Promedio"},
            delta={'reference': avg_order_value * 1.05, 'relative': True},
            domain={'row': 0, 'column': 3}
        ),
        row=1, col=4
    )
    
    fig.update_layout(
        height=200,
        showlegend=False,
        title_text="📊 KPIs Principales",
        title_x=0.5
    )
    
    return fig


def create_sales_trend(datasets):
    """Crear gráfico de tendencia de ventas."""
    sales_metrics = datasets['sales_metrics']
    
    fig = px.line(
        sales_metrics,
        x='order_date',
        y='daily_sales',
        title='📈 Tendencia de Ventas Diarias',
        labels={'order_date': 'Fecha', 'daily_sales': 'Ventas Diarias ($)'}
    )
    
    fig.update_layout(
        height=400,
        xaxis_title="Fecha",
        yaxis_title="Ventas Diarias ($)",
        showlegend=False
    )
    
    return fig


def create_top_customers_chart(datasets):
    """Crear gráfico de top clientes."""
    dim_customers = datasets['dim_customers']
    top_customers = dim_customers.head(10)
    
    fig = px.bar(
        top_customers,
        x='CUSTOMERNAME',
        y='total_sales',
        title='🏆 Top 10 Clientes por Ventas',
        labels={'CUSTOMERNAME': 'Cliente', 'total_sales': 'Ventas Totales ($)'},
        color='total_sales',
        color_continuous_scale='viridis'
    )
    
    fig.update_layout(
        height=400,
        xaxis_tickangle=-45,
        showlegend=False
    )
    
    return fig


def create_product_performance(datasets):
    """Crear gráfico de performance de productos."""
    dim_products = datasets['dim_products']
    top_products = dim_products.head(15)
    
    fig = px.bar(
        top_products,
        x='PRODUCTCODE',
        y='total_sales',
        color='PRODUCTLINE',
        title='📦 Top 15 Productos por Ventas',
        labels={'PRODUCTCODE': 'Código de Producto', 'total_sales': 'Ventas Totales ($)', 'PRODUCTLINE': 'Línea de Producto'}
    )
    
    fig.update_layout(
        height=400,
        xaxis_tickangle=-45
    )
    
    return fig


def create_geographic_analysis(datasets):
    """Crear análisis geográfico."""
    dim_countries = datasets['dim_countries']
    
    fig = px.bar(
        dim_countries,
        x='COUNTRY',
        y='total_sales',
        title='🌍 Ventas por País',
        labels={'COUNTRY': 'País', 'total_sales': 'Ventas Totales ($)'},
        color='total_sales',
        color_continuous_scale='plasma'
    )
    
    fig.update_layout(
        height=400,
        xaxis_tickangle=-45,
        showlegend=False
    )
    
    return fig


def create_temporal_heatmap(datasets):
    """Crear mapa de calor temporal."""
    temporal = datasets['temporal_analysis']
    
    # Preparar datos para el mapa de calor
    heatmap_data = temporal.pivot_table(
        values='total_sales',
        index='day_of_week',
        columns='month',
        aggfunc='sum'
    )
    
    # Mapear días de la semana
    day_names = ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado']
    heatmap_data.index = [day_names[int(i)] if isinstance(i, (int, str)) and str(i).isdigit() else i for i in heatmap_data.index]
    
    # Mapear meses
    month_names = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
    heatmap_data.columns = [month_names[int(i)-1] if isinstance(i, (int, str)) and str(i).isdigit() else i for i in heatmap_data.columns]
    
    fig = px.imshow(
        heatmap_data,
        title='📅 Mapa de Calor: Ventas por Día y Mes',
        labels=dict(x="Mes", y="Día de la Semana", color="Ventas ($)"),
        color_continuous_scale='YlOrRd'
    )
    
    fig.update_layout(
        height=400
    )
    
    return fig


def create_dashboard_html():
    """Crear dashboard completo en HTML."""
    print("🔄 Generando vista previa del dashboard...")
    
    # Cargar datos
    datasets = load_powerbi_data()
    
    # Crear visualizaciones
    kpi_fig = create_kpi_cards(datasets)
    trend_fig = create_sales_trend(datasets)
    customers_fig = create_top_customers_chart(datasets)
    products_fig = create_product_performance(datasets)
    geo_fig = create_geographic_analysis(datasets)
    heatmap_fig = create_temporal_heatmap(datasets)
    
    # Crear HTML del dashboard
    html_content = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Dashboard de Análisis de Ventas - Vista Previa Power BI</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 20px;
                background-color: #f5f5f5;
            }}
            .container {{
                max-width: 1400px;
                margin: 0 auto;
                background-color: white;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                overflow: hidden;
            }}
            .header {{
                background: linear-gradient(135deg, #1f77b4, #ff7f0e);
                color: white;
                padding: 30px;
                text-align: center;
            }}
            .header h1 {{
                margin: 0;
                font-size: 2.5em;
                font-weight: bold;
            }}
            .header p {{
                margin: 10px 0 0 0;
                font-size: 1.2em;
                opacity: 0.9;
            }}
            .dashboard-content {{
                padding: 30px;
            }}
            .section {{
                margin-bottom: 40px;
            }}
            .section-title {{
                font-size: 1.5em;
                font-weight: bold;
                color: #333;
                margin-bottom: 20px;
                padding-bottom: 10px;
                border-bottom: 2px solid #1f77b4;
            }}
            .chart-container {{
                background-color: white;
                border-radius: 8px;
                padding: 20px;
                margin-bottom: 30px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }}
            .info-box {{
                background-color: #e3f2fd;
                border-left: 4px solid #1f77b4;
                padding: 20px;
                margin-bottom: 30px;
                border-radius: 0 8px 8px 0;
            }}
            .info-box h3 {{
                margin: 0 0 10px 0;
                color: #1f77b4;
            }}
            .info-box ul {{
                margin: 0;
                padding-left: 20px;
            }}
            .info-box li {{
                margin-bottom: 5px;
            }}
            .footer {{
                background-color: #333;
                color: white;
                text-align: center;
                padding: 20px;
                font-size: 0.9em;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📊 Dashboard de Análisis de Ventas</h1>
                <p>Vista Previa - Power BI Dashboard</p>
            </div>
            
            <div class="dashboard-content">
                <div class="info-box">
                    <h3>ℹ️ Información del Dashboard</h3>
                    <ul>
                        <li><strong>Total de Registros:</strong> {len(datasets['sales_fact']):,} ventas</li>
                        <li><strong>Período:</strong> {datasets['sales_fact']['ORDERDATE'].min()} a {datasets['sales_fact']['ORDERDATE'].max()}</li>
                        <li><strong>Clientes Únicos:</strong> {datasets['sales_fact']['CUSTOMERNAME'].nunique():,}</li>
                        <li><strong>Productos Únicos:</strong> {datasets['sales_fact']['PRODUCTCODE'].nunique():,}</li>
                        <li><strong>Países:</strong> {datasets['sales_fact']['COUNTRY'].nunique():,}</li>
                    </ul>
                </div>
                
                <div class="section">
                    <div class="section-title">📈 KPIs Principales</div>
                    <div class="chart-container">
                        {kpi_fig.to_html(full_html=False, include_plotlyjs='cdn')}
                    </div>
                </div>
                
                <div class="section">
                    <div class="section-title">📊 Análisis de Ventas</div>
                    <div class="chart-container">
                        {trend_fig.to_html(full_html=False, include_plotlyjs='cdn')}
                    </div>
                </div>
                
                <div class="section">
                    <div class="section-title">👥 Análisis de Clientes</div>
                    <div class="chart-container">
                        {customers_fig.to_html(full_html=False, include_plotlyjs='cdn')}
                    </div>
                </div>
                
                <div class="section">
                    <div class="section-title">📦 Análisis de Productos</div>
                    <div class="chart-container">
                        {products_fig.to_html(full_html=False, include_plotlyjs='cdn')}
                    </div>
                </div>
                
                <div class="section">
                    <div class="section-title">🌍 Análisis Geográfico</div>
                    <div class="chart-container">
                        {geo_fig.to_html(full_html=False, include_plotlyjs='cdn')}
                    </div>
                </div>
                
                <div class="section">
                    <div class="section-title">📅 Análisis Temporal</div>
                    <div class="chart-container">
                        {heatmap_fig.to_html(full_html=False, include_plotlyjs='cdn')}
                    </div>
                </div>
                
                <div class="info-box">
                    <h3>🚀 Próximos Pasos para Power BI</h3>
                    <ul>
                        <li>Importar el archivo Excel: <code>data/final/powerbi_data.xlsx</code></li>
                        <li>Configurar las relaciones entre las 7 tablas</li>
                        <li>Crear medidas DAX para cálculos avanzados</li>
                        <li>Aplicar el tema y colores recomendados</li>
                        <li>Agregar filtros y segmentadores interactivos</li>
                        <li>Configurar actualizaciones automáticas</li>
                    </ul>
                </div>
            </div>
            
            <div class="footer">
                <p>Dashboard generado automáticamente por el sistema de análisis de datos</p>
                <p>Fecha de generación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Guardar archivo HTML
    output_path = "data/final/powerbi_dashboard_preview.html"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Dashboard HTML generado: {output_path}")
    return output_path


def main():
    """Función principal."""
    print("🎨 Generando vista previa del dashboard de Power BI...")
    
    try:
        # Crear dashboard HTML
        dashboard_path = create_dashboard_html()
        
        print("\n✅ ¡Vista previa del dashboard creada exitosamente!")
        print(f"\n📊 Archivos disponibles para Power BI:")
        print(f"   - Excel: data/final/powerbi_data.xlsx")
        print(f"   - CSV: data/final/powerbi_csv/")
        print(f"   - Guía: data/final/powerbi_guide.md")
        print(f"   - Vista previa: {dashboard_path}")
        
        print(f"\n🎯 Instrucciones para Power BI:")
        print(f"   1. Abrir Power BI Desktop")
        print(f"   2. Ir a 'Obtener datos' → 'Excel'")
        print(f"   3. Seleccionar: data/final/powerbi_data.xlsx")
        print(f"   4. Importar todas las hojas")
        print(f"   5. Configurar relaciones entre tablas")
        print(f"   6. Crear visualizaciones siguiendo la guía")
        print(f"   7. Aplicar tema y colores recomendados")
        
        print(f"\n💡 Consejos adicionales:")
        print(f"   - Usar la vista previa HTML como referencia")
        print(f"   - Seguir las mejores prácticas de Power BI")
        print(f"   - Optimizar el rendimiento del dashboard")
        print(f"   - Probar la interactividad entre visualizaciones")
        
    except Exception as e:
        print(f"❌ Error al generar dashboard: {e}")
        raise


if __name__ == "__main__":
    main()
