"""
Configuración y constantes del proyecto de análisis de ventas.

Este módulo contiene todas las configuraciones, constantes y parámetros
utilizados en el proyecto.
"""

import os
from pathlib import Path
from typing import Dict, List

# Configuración de rutas
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
FINAL_DATA_DIR = DATA_DIR / "final"

# Archivos de datos
SALES_DATA_FILE = "sales_data_sample.csv"
CLEANED_DATA_FILE = "sales_data_cleaned.csv"
DATABASE_FILE = "sales_analysis.db"

# Configuración de logging
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = PROJECT_ROOT / "logs" / "sales_analysis.log"

# Configuración de visualizaciones
FIGURE_SIZE = (12, 8)
DPI = 300
COLOR_PALETTE = "husl"
STYLE = "seaborn-v0_8"

# Configuración de análisis
SALES_CATEGORIES = {
    'Small': (0, 1000),
    'Medium': (1000, 5000),
    'Large': (5000, 10000),
    'Very Large': (10000, float('inf'))
}

# Configuración de SQL
SQL_INDEXES = [
    "CREATE INDEX IF NOT EXISTS idx_orderdate ON sales_data(ORDERDATE)",
    "CREATE INDEX IF NOT EXISTS idx_productline ON sales_data(PRODUCTLINE)",
    "CREATE INDEX IF NOT EXISTS idx_country ON sales_data(COUNTRY)",
    "CREATE INDEX IF NOT EXISTS idx_status ON sales_data(STATUS)",
    "CREATE INDEX IF NOT EXISTS idx_year_month ON sales_data(YEAR_ID, MONTH_ID)",
    "CREATE INDEX IF NOT EXISTS idx_sales ON sales_data(SALES)",
    "CREATE INDEX IF NOT EXISTS idx_customer ON sales_data(CUSTOMERNAME)"
]

# Configuración de columnas
DATE_COLUMNS = ['ORDERDATE']
NUMERIC_COLUMNS = ['QUANTITYORDERED', 'PRICEEACH', 'SALES', 'MSRP']
CATEGORICAL_COLUMNS = ['PRODUCTLINE', 'STATUS', 'COUNTRY', 'TERRITORY', 'CUSTOMERNAME']

# Configuración de limpieza de datos
CLEANING_STRATEGIES = {
    'auto': 'Estrategia automática basada en tipo de columna',
    'drop': 'Eliminar filas con valores faltantes',
    'fill': 'Llenar con valores específicos'
}

# Configuración de reportes
REPORT_SECTIONS = [
    'resumen_ejecutivo',
    'analisis_temporal',
    'analisis_productos',
    'analisis_clientes',
    'correlaciones',
    'recomendaciones'
]

# Configuración de Power BI
POWERBI_CONFIG = {
    'data_source': 'sales_data_cleaned.csv',
    'refresh_frequency': 'daily',
    'export_format': 'pbix'
}

# Configuración de testing
TEST_DATA_SIZE = 100
TEST_COVERAGE_THRESHOLD = 80

# Configuración de performance
MEMORY_OPTIMIZATION_THRESHOLD = 0.5  # 50% de valores únicos para categorizar
BATCH_SIZE = 1000

# Configuración de exportación
EXPORT_FORMATS = ['csv', 'excel', 'json', 'parquet']
DEFAULT_EXPORT_FORMAT = 'csv'

# Configuración de validación
VALIDATION_RULES = {
    'sales_positive': 'SALES debe ser mayor que 0',
    'quantity_positive': 'QUANTITYORDERED debe ser mayor que 0',
    'price_positive': 'PRICEEACH debe ser mayor que 0',
    'date_valid': 'ORDERDATE debe ser una fecha válida'
}

# Configuración de alertas
ALERT_THRESHOLDS = {
    'missing_data_percentage': 0.1,  # 10%
    'duplicate_percentage': 0.05,    # 5%
    'outlier_threshold': 3.0         # 3 desviaciones estándar
}

# Configuración de documentación
DOCS_CONFIG = {
    'output_format': 'markdown',
    'include_code_examples': True,
    'include_visualizations': True,
    'auto_generate': True
}

# Configuración de seguridad
SECURITY_CONFIG = {
    'log_sensitive_data': False,
    'encrypt_output_files': False,
    'sanitize_logs': True
}

# Configuración de monitoreo
MONITORING_CONFIG = {
    'enable_performance_tracking': True,
    'enable_error_tracking': True,
    'enable_usage_analytics': False
}

# Configuración de backup
BACKUP_CONFIG = {
    'enable_auto_backup': True,
    'backup_frequency': 'daily',
    'retention_days': 30,
    'backup_location': PROJECT_ROOT / "backups"
}

# Configuración de cache
CACHE_CONFIG = {
    'enable_cache': True,
    'cache_ttl': 3600,  # 1 hora
    'cache_location': PROJECT_ROOT / "cache"
}

# Configuración de paralelización
PARALLEL_CONFIG = {
    'enable_parallel_processing': True,
    'max_workers': os.cpu_count(),
    'chunk_size': 1000
}

# Configuración de calidad de datos
DATA_QUALITY_CONFIG = {
    'enable_validation': True,
    'enable_profiling': True,
    'enable_monitoring': True,
    'quality_threshold': 0.95  # 95% de calidad mínima
}

# Configuración de versionado
VERSION_CONFIG = {
    'enable_versioning': True,
    'version_format': 'semantic',
    'auto_increment_patch': True
}

# Configuración de internacionalización
I18N_CONFIG = {
    'default_language': 'es',
    'supported_languages': ['es', 'en'],
    'date_format': '%Y-%m-%d',
    'number_format': 'en_US'
}

# Configuración de accesibilidad
ACCESSIBILITY_CONFIG = {
    'enable_alt_text': True,
    'enable_keyboard_navigation': True,
    'enable_screen_reader_support': True
}

# Configuración de compliance
COMPLIANCE_CONFIG = {
    'gdpr_compliant': True,
    'data_retention_policy': '30_days',
    'privacy_by_design': True
}

# Configuración de escalabilidad
SCALABILITY_CONFIG = {
    'enable_horizontal_scaling': True,
    'enable_vertical_scaling': True,
    'load_balancing': False,
    'auto_scaling': False
}

# Configuración de integración
INTEGRATION_CONFIG = {
    'enable_api': False,
    'enable_webhooks': False,
    'enable_scheduled_tasks': True,
    'enable_event_driven': False
}

# Configuración de desarrollo
DEV_CONFIG = {
    'debug_mode': False,
    'development_mode': True,
    'enable_hot_reload': False,
    'enable_profiling': False
}

# Configuración de producción
PROD_CONFIG = {
    'debug_mode': False,
    'development_mode': False,
    'enable_hot_reload': False,
    'enable_profiling': False,
    'enable_monitoring': True,
    'enable_logging': True
}

# Configuración de testing
TESTING_CONFIG = {
    'unit_testing': True,
    'integration_testing': True,
    'performance_testing': False,
    'security_testing': False,
    'coverage_threshold': 80
}

# Configuración de CI/CD
CICD_CONFIG = {
    'enable_automated_testing': True,
    'enable_automated_deployment': False,
    'enable_code_quality_checks': True,
    'enable_security_scans': False
}

# Configuración de documentación
DOCUMENTATION_CONFIG = {
    'auto_generate_docs': True,
    'include_api_docs': False,
    'include_user_guide': True,
    'include_developer_guide': True
}

# Configuración de soporte
SUPPORT_CONFIG = {
    'enable_error_reporting': True,
    'enable_user_feedback': False,
    'enable_help_system': True,
    'support_email': 'support@example.com'
}

# Configuración de licencia
LICENSE_CONFIG = {
    'license_type': 'MIT',
    'copyright_holder': '[Tu Nombre]',
    'year': '2024'
}

# Configuración de metadatos
METADATA_CONFIG = {
    'project_name': 'Sales Analysis Roadmap',
    'project_description': 'Análisis completo de datos de ventas con SQL avanzado y Python',
    'project_version': '1.0.0',
    'project_author': '[Tu Nombre]',
    'project_url': 'https://github.com/username/sales-analysis-roadmap',
    'project_license': 'MIT'
}

# Función para obtener configuración específica del entorno
def get_config(environment: str = 'development') -> Dict:
    """
    Obtener configuración específica del entorno.
    
    Args:
        environment: Entorno ('development', 'production', 'testing')
        
    Returns:
        Diccionario con la configuración del entorno
    """
    configs = {
        'development': DEV_CONFIG,
        'production': PROD_CONFIG,
        'testing': TESTING_CONFIG
    }
    
    return configs.get(environment, DEV_CONFIG)

# Función para validar configuración
def validate_config() -> bool:
    """
    Validar que la configuración sea correcta.
    
    Returns:
        True si la configuración es válida, False en caso contrario
    """
    try:
        # Verificar que las rutas existan o se puedan crear
        for path in [DATA_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR, FINAL_DATA_DIR]:
            path.mkdir(parents=True, exist_ok=True)
        
        # Verificar archivos de datos
        if not (RAW_DATA_DIR / SALES_DATA_FILE).exists():
            print(f"Warning: Archivo de datos no encontrado: {SALES_DATA_FILE}")
        
        return True
        
    except Exception as e:
        print(f"Error validando configuración: {e}")
        return False

# Función para obtener configuración de logging
def get_logging_config() -> Dict:
    """
    Obtener configuración de logging.
    
    Returns:
        Diccionario con configuración de logging
    """
    return {
        'level': LOG_LEVEL,
        'format': LOG_FORMAT,
        'file': LOG_FILE,
        'handlers': ['console', 'file']
    }

# Función para obtener configuración de base de datos
def get_database_config() -> Dict:
    """
    Obtener configuración de base de datos.
    
    Returns:
        Diccionario con configuración de base de datos
    """
    return {
        'path': PROCESSED_DATA_DIR / DATABASE_FILE,
        'indexes': SQL_INDEXES,
        'backup_enabled': BACKUP_CONFIG['enable_auto_backup']
    }

# Función para obtener configuración de exportación
def get_export_config() -> Dict:
    """
    Obtener configuración de exportación.
    
    Returns:
        Diccionario con configuración de exportación
    """
    return {
        'formats': EXPORT_FORMATS,
        'default_format': DEFAULT_EXPORT_FORMAT,
        'output_dir': FINAL_DATA_DIR,
        'include_metadata': True
    }
