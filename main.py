#!/usr/bin/env python3
"""
Script principal del proyecto de análisis de ventas.

Este script ejecuta el pipeline completo del proyecto:
1. Limpieza de datos
2. Consultas SQL avanzadas
3. Análisis exploratorio
4. Generación de reportes

Autor: [Tu Nombre]
Fecha: [Fecha]
"""

import sys
import logging
from pathlib import Path
import time
from datetime import datetime

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from data_processing.data_cleaner import SalesDataCleaner
from sql_queries.advanced_queries import SalesSQLAnalyzer
from analysis.exploratory_analysis import SalesExploratoryAnalyzer
from utils.config import validate_config, get_logging_config


def setup_logging():
    """
    Configurar logging para el proyecto.
    """
    log_config = get_logging_config()
    
    # Crear directorio de logs si no existe
    log_file = Path(log_config['file'])
    log_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Configurar logging
    logging.basicConfig(
        level=getattr(logging, log_config['level']),
        format=log_config['format'],
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    return logging.getLogger(__name__)


def print_banner():
    """
    Imprimir banner del proyecto.
    """
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║           PROYECTO DE ANÁLISIS DE VENTAS                    ║
    ║                    ROADMAP DE DATOS                          ║
    ║                                                              ║
    ║  SQL Avanzado • Python para Datos • Buenas Prácticas        ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def print_progress(step: int, total_steps: int, message: str):
    """
    Imprimir progreso del pipeline.
    
    Args:
        step: Paso actual
        total_steps: Total de pasos
        message: Mensaje descriptivo
    """
    progress = (step / total_steps) * 100
    bar_length = 40
    filled_length = int(bar_length * step // total_steps)
    bar = '█' * filled_length + '-' * (bar_length - filled_length)
    
    print(f"\n[{bar}] {progress:.1f}% - Paso {step}/{total_steps}")
    print(f"📋 {message}")
    print("-" * 60)


def step_1_data_cleaning(logger):
    """
    Paso 1: Limpieza de datos.
    
    Args:
        logger: Logger configurado
        
    Returns:
        bool: True si el paso fue exitoso
    """
    try:
        print_progress(1, 4, "Limpieza y procesamiento de datos")
        
        # Configurar rutas
        input_file = "data/raw/sales_data_sample.csv"
        output_file = "data/processed/sales_data_cleaned.csv"
        
        # Verificar que existe el archivo de entrada
        if not Path(input_file).exists():
            logger.error(f"Archivo de entrada no encontrado: {input_file}")
            return False
        
        # Inicializar limpiador
        cleaner = SalesDataCleaner(input_file)
        
        # Ejecutar pipeline de limpieza
        logger.info("Iniciando limpieza de datos...")
        
        # Cargar datos
        df = cleaner.load_data()
        logger.info(f"Datos cargados: {len(df):,} registros, {len(df.columns)} columnas")
        
        # Validar estructura
        validation = cleaner.validate_data_structure()
        logger.info(f"Validación inicial completada")
        
        # Proceso de limpieza
        cleaner.clean_missing_values(strategy='auto')
        logger.info("Valores faltantes limpiados")
        
        removed_duplicates = cleaner.remove_duplicates()
        logger.info(f"Duplicados eliminados: {removed_duplicates}")
        
        cleaner.optimize_data_types()
        logger.info("Tipos de datos optimizados")
        
        cleaner.transform_dates()
        logger.info("Fechas transformadas")
        
        cleaner.create_derived_features()
        logger.info("Características derivadas creadas")
        
        # Guardar datos limpios
        cleaner.save_cleaned_data(output_file)
        logger.info(f"Datos limpios guardados en: {output_file}")
        
        # Mostrar resumen
        summary = cleaner.get_cleaning_summary()
        logger.info(f"Resumen final: {summary['final_shape'][0]:,} registros, "
                   f"{summary['final_shape'][1]} columnas")
        
        print("✅ Limpieza de datos completada exitosamente")
        return True
        
    except Exception as e:
        logger.error(f"Error en limpieza de datos: {str(e)}")
        print(f"❌ Error en limpieza de datos: {str(e)}")
        return False


def step_2_sql_analysis(logger):
    """
    Paso 2: Análisis SQL avanzado.
    
    Args:
        logger: Logger configurado
        
    Returns:
        bool: True si el paso fue exitoso
    """
    try:
        print_progress(2, 4, "Ejecutando consultas SQL avanzadas")
        
        # Configurar rutas
        csv_path = "data/processed/sales_data_cleaned.csv"
        
        # Verificar que existe el archivo limpio
        if not Path(csv_path).exists():
            logger.error(f"Archivo limpio no encontrado: {csv_path}")
            return False
        
        # Inicializar analizador SQL
        analyzer = SalesSQLAnalyzer()
        
        # Crear base de datos y tablas
        logger.info("Creando base de datos SQLite...")
        analyzer.create_tables_from_csv(csv_path)
        
        # Ejecutar consultas de demostración
        logger.info("Ejecutando Window Functions...")
        window_results = analyzer.window_functions_demo()
        logger.info(f"Window Functions: {len(window_results)} registros")
        
        logger.info("Ejecutando análisis CTE complejo...")
        cte_results = analyzer.cte_complex_analysis()
        logger.info(f"Análisis CTE: {len(cte_results)} registros")
        
        logger.info("Ejecutando subqueries...")
        subquery_results = analyzer.subqueries_demo()
        logger.info(f"Subqueries: {len(subquery_results)} registros")
        
        logger.info("Ejecutando joins avanzados...")
        joins_results = analyzer.advanced_joins_demo()
        logger.info(f"Joins avanzados: {len(joins_results)} registros")
        
        logger.info("Analizando performance...")
        perf_results = analyzer.performance_optimization_demo()
        logger.info(f"Resultados de performance: {perf_results}")
        
        # Cerrar conexión
        analyzer.close_connection()
        
        print("✅ Análisis SQL avanzado completado exitosamente")
        return True
        
    except Exception as e:
        logger.error(f"Error en análisis SQL: {str(e)}")
        print(f"❌ Error en análisis SQL: {str(e)}")
        return False


def step_3_exploratory_analysis(logger):
    """
    Paso 3: Análisis exploratorio.
    
    Args:
        logger: Logger configurado
        
    Returns:
        bool: True si el paso fue exitoso
    """
    try:
        print_progress(3, 4, "Realizando análisis exploratorio")
        
        # Configurar rutas
        csv_path = "data/processed/sales_data_cleaned.csv"
        
        # Verificar que existe el archivo limpio
        if not Path(csv_path).exists():
            logger.error(f"Archivo limpio no encontrado: {csv_path}")
            return False
        
        # Inicializar analizador exploratorio
        analyzer = SalesExploratoryAnalyzer(csv_path)
        
        # Cargar datos
        logger.info("Cargando datos para análisis exploratorio...")
        df = analyzer.load_data()
        logger.info(f"Datos cargados: {len(df):,} registros")
        
        # Ejecutar análisis completo
        logger.info("Calculando estadísticas básicas...")
        basic_stats = analyzer.basic_statistics()
        logger.info(f"Estadísticas calculadas para {basic_stats['dataset_info']['total_rows']:,} registros")
        
        logger.info("Realizando análisis temporal...")
        temporal_results = analyzer.temporal_analysis()
        logger.info("Análisis temporal completado")
        
        logger.info("Analizando productos...")
        product_results = analyzer.product_analysis()
        logger.info("Análisis de productos completado")
        
        logger.info("Analizando clientes...")
        customer_results = analyzer.customer_analysis()
        logger.info("Análisis de clientes completado")
        
        logger.info("Analizando correlaciones...")
        correlation_results = analyzer.correlation_analysis()
        logger.info("Análisis de correlaciones completado")
        
        logger.info("Creando dashboard interactivo...")
        analyzer.create_interactive_dashboard()
        logger.info("Dashboard interactivo creado")
        
        logger.info("Generando reporte...")
        report_path = analyzer.generate_analysis_report()
        logger.info(f"Reporte generado: {report_path}")
        
        print("✅ Análisis exploratorio completado exitosamente")
        return True
        
    except Exception as e:
        logger.error(f"Error en análisis exploratorio: {str(e)}")
        print(f"❌ Error en análisis exploratorio: {str(e)}")
        return False


def step_4_final_report(logger):
    """
    Paso 4: Generar reporte final.
    
    Args:
        logger: Logger configurado
        
    Returns:
        bool: True si el paso fue exitoso
    """
    try:
        print_progress(4, 4, "Generando reporte final del proyecto")
        
        # Crear reporte final
        report_content = []
        report_content.append("# REPORTE FINAL - PROYECTO DE ANÁLISIS DE VENTAS")
        report_content.append("=" * 60)
        report_content.append("")
        report_content.append(f"**Fecha de ejecución**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_content.append(f"**Versión del proyecto**: 1.0.0")
        report_content.append("")
        
        report_content.append("## RESUMEN EJECUTIVO")
        report_content.append("")
        report_content.append("Este proyecto ha demostrado exitosamente las siguientes técnicas avanzadas:")
        report_content.append("")
        report_content.append("### ✅ SQL Avanzado")
        report_content.append("- **Window Functions**: ROW_NUMBER(), RANK(), DENSE_RANK(), LAG(), LEAD()")
        report_content.append("- **CTEs**: Common Table Expressions para análisis complejos")
        report_content.append("- **Subqueries**: Correlated, EXISTS, IN, ANY, ALL")
        report_content.append("- **Joins avanzados**: SELF JOIN, CROSS JOIN")
        report_content.append("- **Optimización**: Índices y planes de ejecución")
        report_content.append("")
        
        report_content.append("### ✅ Python para Datos")
        report_content.append("- **Pandas avanzado**: Operaciones vectorizadas y optimización")
        report_content.append("- **Limpieza de datos**: Estrategias automáticas y manuales")
        report_content.append("- **Visualizaciones**: Matplotlib, Seaborn, Plotly")
        report_content.append("- **Análisis exploratorio**: Estadísticas descriptivas y correlaciones")
        report_content.append("")
        
        report_content.append("### ✅ Buenas Prácticas")
        report_content.append("- **PEP8**: Código Python bien estructurado")
        report_content.append("- **Logging**: Registro estructurado de eventos")
        report_content.append("- **Testing**: Tests unitarios con pytest")
        report_content.append("- **Documentación**: Docstrings y comentarios completos")
        report_content.append("- **Modularización**: Separación de responsabilidades")
        report_content.append("")
        
        report_content.append("## ARCHIVOS GENERADOS")
        report_content.append("")
        report_content.append("### Datos")
        report_content.append("- `data/raw/sales_data_sample.csv` - Datos originales")
        report_content.append("- `data/processed/sales_data_cleaned.csv` - Datos limpios")
        report_content.append("- `data/processed/sales_analysis.db` - Base de datos SQLite")
        report_content.append("")
        
        report_content.append("### Visualizaciones")
        report_content.append("- `data/final/temporal_analysis.png` - Análisis temporal")
        report_content.append("- `data/final/product_analysis.png` - Análisis de productos")
        report_content.append("- `data/final/customer_analysis.png` - Análisis de clientes")
        report_content.append("- `data/final/correlation_analysis.png` - Matriz de correlación")
        report_content.append("- `data/final/interactive_dashboard.html` - Dashboard interactivo")
        report_content.append("")
        
        report_content.append("### Reportes")
        report_content.append("- `data/final/analysis_report.md` - Reporte de análisis")
        report_content.append("- `data/processed/sales_data_cleaned_cleaning_log.txt` - Log de limpieza")
        report_content.append("")
        
        report_content.append("## INSIGHTS CLAVE DEL NEGOCIO")
        report_content.append("")
        report_content.append("1. **Patrones temporales**: Identificación de estacionalidad en ventas")
        report_content.append("2. **Productos estrella**: Análisis de líneas de producto más rentables")
        report_content.append("3. **Clientes VIP**: Segmentación de clientes por valor")
        report_content.append("4. **Correlaciones**: Relaciones entre variables de ventas")
        report_content.append("5. **Optimización**: Oportunidades de mejora en precios y cantidades")
        report_content.append("")
        
        report_content.append("## RECOMENDACIONES")
        report_content.append("")
        report_content.append("1. **Enfoque en productos de alto rendimiento**")
        report_content.append("2. **Desarrollo de estrategias para clientes VIP**")
        report_content.append("3. **Optimización de precios basada en análisis de correlación**")
        report_content.append("4. **Planificación estacional de inventario**")
        report_content.append("5. **Implementación de dashboard en Power BI**")
        report_content.append("")
        
        report_content.append("## PRÓXIMOS PASOS")
        report_content.append("")
        report_content.append("1. **Dashboard en Power BI**: Crear visualizaciones interactivas")
        report_content.append("2. **Análisis predictivo**: Implementar modelos de ML")
        report_content.append("3. **Automatización**: Pipeline de datos automatizado")
        report_content.append("4. **Monitoreo**: Sistema de alertas y métricas")
        report_content.append("5. **Escalabilidad**: Preparar para datasets más grandes")
        report_content.append("")
        
        report_content.append("## CONCLUSIÓN")
        report_content.append("")
        report_content.append("Este proyecto ha sentado las bases sólidas para el análisis de datos avanzado,")
        report_content.append("demostrando competencias en SQL, Python y buenas prácticas de desarrollo.")
        report_content.append("Los resultados obtenidos proporcionan insights valiosos para la toma de decisiones")
        report_content.append("y establecen un framework robusto para futuros análisis.")
        report_content.append("")
        
        report_content.append("---")
        report_content.append("**Proyecto completado exitosamente** 🎉")
        report_content.append("")
        
        # Guardar reporte final
        output_path = Path("data/final/final_project_report.md")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report_content))
        
        logger.info(f"Reporte final guardado en: {output_path}")
        
        print("✅ Reporte final generado exitosamente")
        return True
        
    except Exception as e:
        logger.error(f"Error generando reporte final: {str(e)}")
        print(f"❌ Error generando reporte final: {str(e)}")
        return False


def main():
    """
    Función principal del proyecto.
    """
    # Configurar logging
    logger = setup_logging()
    
    # Imprimir banner
    print_banner()
    
    # Validar configuración
    logger.info("Validando configuración del proyecto...")
    if not validate_config():
        logger.error("Error en la configuración del proyecto")
        print("❌ Error en la configuración del proyecto")
        return False
    
    print("✅ Configuración validada correctamente")
    
    # Registrar inicio
    start_time = time.time()
    logger.info("Iniciando pipeline del proyecto de análisis de ventas")
    
    # Ejecutar pipeline
    steps = [
        ("Limpieza de datos", step_1_data_cleaning),
        ("Análisis SQL avanzado", step_2_sql_analysis),
        ("Análisis exploratorio", step_3_exploratory_analysis),
        ("Reporte final", step_4_final_report)
    ]
    
    successful_steps = 0
    
    for step_name, step_function in steps:
        try:
            logger.info(f"Iniciando paso: {step_name}")
            
            if step_function(logger):
                successful_steps += 1
                logger.info(f"Paso completado exitosamente: {step_name}")
            else:
                logger.error(f"Paso falló: {step_name}")
                print(f"❌ El paso '{step_name}' falló. Continuando con el siguiente...")
                
        except Exception as e:
            logger.error(f"Error inesperado en paso '{step_name}': {str(e)}")
            print(f"❌ Error inesperado en '{step_name}': {str(e)}")
    
    # Calcular tiempo total
    total_time = time.time() - start_time
    
    # Mostrar resumen final
    print("\n" + "=" * 60)
    print("🎯 RESUMEN FINAL DEL PROYECTO")
    print("=" * 60)
    print(f"✅ Pasos completados: {successful_steps}/{len(steps)}")
    print(f"⏱️  Tiempo total: {total_time:.2f} segundos")
    print(f"📊 Archivos generados en: data/final/")
    print(f"📝 Logs disponibles en: logs/sales_analysis.log")
    
    if successful_steps == len(steps):
        print("\n🎉 ¡PROYECTO COMPLETADO EXITOSAMENTE!")
        print("📋 Todos los objetivos han sido alcanzados:")
        print("   • SQL avanzado con Window Functions, CTEs y subqueries")
        print("   • Python para datos con Pandas y visualizaciones")
        print("   • Buenas prácticas con PEP8, logging y testing")
        print("   • Análisis completo de datos de ventas")
        print("   • Documentación y reportes profesionales")
    else:
        print(f"\n⚠️  Proyecto completado parcialmente ({successful_steps}/{len(steps)} pasos)")
        print("Revisa los logs para más detalles sobre los errores.")
    
    print("\n" + "=" * 60)
    print("🚀 ¡Listo para el siguiente nivel!")
    print("=" * 60)
    
    logger.info(f"Pipeline completado: {successful_steps}/{len(steps)} pasos exitosos")
    return successful_steps == len(steps)


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Proyecto interrumpido por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error crítico: {str(e)}")
        sys.exit(1)
