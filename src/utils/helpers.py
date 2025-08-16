"""
Funciones auxiliares para el proyecto de análisis de ventas.

Este módulo contiene funciones utilitarias que pueden ser utilizadas
en diferentes partes del proyecto.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
import logging
from pathlib import Path
import json
from datetime import datetime


def setup_logging(log_level: str = "INFO") -> logging.Logger:
    """
    Configurar logging para el proyecto.
    
    Args:
        log_level: Nivel de logging (DEBUG, INFO, WARNING, ERROR)
        
    Returns:
        Logger configurado
    """
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('project.log'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)


def save_json(data: Dict[str, Any], filepath: str) -> None:
    """
    Guardar datos en formato JSON.
    
    Args:
        data: Datos a guardar
        filepath: Ruta del archivo
    """
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False, default=str)


def load_json(filepath: str) -> Dict[str, Any]:
    """
    Cargar datos desde archivo JSON.
    
    Args:
        filepath: Ruta del archivo
        
    Returns:
        Datos cargados
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def format_currency(amount: float, currency: str = "USD") -> str:
    """
    Formatear cantidad como moneda.
    
    Args:
        amount: Cantidad a formatear
        currency: Código de moneda
        
    Returns:
        Cantidad formateada
    """
    if currency == "USD":
        return f"${amount:,.2f}"
    elif currency == "EUR":
        return f"€{amount:,.2f}"
    else:
        return f"{amount:,.2f} {currency}"


def calculate_percentage_change(current: float, previous: float) -> float:
    """
    Calcular cambio porcentual.
    
    Args:
        current: Valor actual
        previous: Valor anterior
        
    Returns:
        Cambio porcentual
    """
    if previous == 0:
        return 0.0
    return ((current - previous) / previous) * 100


def get_top_n(df: pd.DataFrame, column: str, n: int = 10) -> pd.DataFrame:
    """
    Obtener los top N valores de una columna.
    
    Args:
        df: DataFrame
        column: Columna a analizar
        n: Número de elementos a retornar
        
    Returns:
        DataFrame con los top N valores
    """
    return df[column].value_counts().head(n).reset_index()


def validate_file_exists(filepath: str) -> bool:
    """
    Validar que un archivo existe.
    
    Args:
        filepath: Ruta del archivo
        
    Returns:
        True si el archivo existe, False en caso contrario
    """
    return Path(filepath).exists()


def create_directory_if_not_exists(dirpath: str) -> None:
    """
    Crear directorio si no existe.
    
    Args:
        dirpath: Ruta del directorio
    """
    Path(dirpath).mkdir(parents=True, exist_ok=True)


def get_file_size_mb(filepath: str) -> float:
    """
    Obtener tamaño de archivo en MB.
    
    Args:
        filepath: Ruta del archivo
        
    Returns:
        Tamaño en MB
    """
    return Path(filepath).stat().st_size / (1024 * 1024)


def format_timestamp(timestamp: datetime) -> str:
    """
    Formatear timestamp para logging.
    
    Args:
        timestamp: Timestamp a formatear
        
    Returns:
        Timestamp formateado
    """
    return timestamp.strftime("%Y-%m-%d %H:%M:%S")


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """
    División segura que evita división por cero.
    
    Args:
        numerator: Numerador
        denominator: Denominador
        default: Valor por defecto si el denominador es cero
        
    Returns:
        Resultado de la división o valor por defecto
    """
    if denominator == 0:
        return default
    return numerator / denominator


def round_to_decimals(value: float, decimals: int = 2) -> float:
    """
    Redondear valor a un número específico de decimales.
    
    Args:
        value: Valor a redondear
        decimals: Número de decimales
        
    Returns:
        Valor redondeado
    """
    return round(value, decimals)


def is_numeric_column(df: pd.DataFrame, column: str) -> bool:
    """
    Verificar si una columna es numérica.
    
    Args:
        df: DataFrame
        column: Nombre de la columna
        
    Returns:
        True si la columna es numérica, False en caso contrario
    """
    return pd.api.types.is_numeric_dtype(df[column])


def get_memory_usage_mb(df: pd.DataFrame) -> float:
    """
    Obtener uso de memoria de un DataFrame en MB.
    
    Args:
        df: DataFrame
        
    Returns:
        Uso de memoria en MB
    """
    return df.memory_usage(deep=True).sum() / (1024 * 1024)

