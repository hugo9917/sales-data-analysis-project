"""
Módulo de limpieza y procesamiento de datos de ventas.

Este módulo contiene funciones para limpiar, validar y transformar
el dataset de ventas siguiendo las mejores prácticas de Python.

Autor: [Tu Nombre]
Fecha: [Fecha]
"""

import logging
import pandas as pd
import numpy as np
from typing import Optional, Dict, List, Tuple
from pathlib import Path
import warnings

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Suprimir warnings de pandas
warnings.filterwarnings('ignore', category=FutureWarning)


class SalesDataCleaner:
    """
    Clase para limpiar y procesar datos de ventas.
    
    Esta clase implementa métodos para:
    - Cargar datos desde CSV
    - Validar estructura de datos
    - Limpiar valores faltantes y duplicados
    - Transformar tipos de datos
    - Optimizar uso de memoria
    """
    
    def __init__(self, data_path: str):
        """
        Inicializar el limpiador de datos.
        
        Args:
            data_path: Ruta al archivo CSV de datos
        """
        self.data_path = Path(data_path)
        self.df: Optional[pd.DataFrame] = None
        self.cleaning_log: List[str] = []
        
        logger.info(f"Inicializando SalesDataCleaner con datos en: {data_path}")
    
    def load_data(self) -> pd.DataFrame:
        """
        Cargar datos desde archivo CSV.
        
        Returns:
            DataFrame con los datos cargados
            
        Raises:
            FileNotFoundError: Si el archivo no existe
            pd.errors.EmptyDataError: Si el archivo está vacío
        """
        try:
            logger.info("Cargando datos desde CSV...")
            
            # Intentar con diferentes encodings
            encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
            
            for encoding in encodings:
                try:
                    self.df = pd.read_csv(self.data_path, encoding=encoding)
                    logger.info(f"Datos cargados exitosamente con encoding {encoding}: {self.df.shape[0]} filas, "
                               f"{self.df.shape[1]} columnas")
                    return self.df
                except UnicodeDecodeError:
                    continue
                except Exception as e:
                    logger.warning(f"Error con encoding {encoding}: {str(e)}")
                    continue
            
            # Si ningún encoding funciona, intentar con manejo de errores
            self.df = pd.read_csv(self.data_path, encoding='latin-1', on_bad_lines='skip')
            logger.info(f"Datos cargados con manejo de errores: {self.df.shape[0]} filas, "
                       f"{self.df.shape[1]} columnas")
            return self.df
            
        except FileNotFoundError:
            logger.error(f"Archivo no encontrado: {self.data_path}")
            raise
        except pd.errors.EmptyDataError:
            logger.error("El archivo CSV está vacío")
            raise
        except Exception as e:
            logger.error(f"Error al cargar datos: {str(e)}")
            raise
    
    def validate_data_structure(self) -> Dict[str, any]:
        """
        Validar la estructura de los datos.
        
        Returns:
            Diccionario con información de validación
        """
        if self.df is None:
            raise ValueError("No hay datos cargados. Ejecuta load_data() primero.")
        
        logger.info("Validando estructura de datos...")
        
        validation_results = {
            'total_rows': len(self.df),
            'total_columns': len(self.df.columns),
            'missing_values': self.df.isnull().sum().to_dict(),
            'duplicate_rows': self.df.duplicated().sum(),
            'data_types': self.df.dtypes.to_dict(),
            'memory_usage_mb': self.df.memory_usage(deep=True).sum() / 1024**2
        }
        
        # Log validation results
        logger.info(f"Filas totales: {validation_results['total_rows']}")
        logger.info(f"Columnas totales: {validation_results['total_columns']}")
        logger.info(f"Filas duplicadas: {validation_results['duplicate_rows']}")
        logger.info(f"Uso de memoria: {validation_results['memory_usage_mb']:.2f} MB")
        
        return validation_results
    
    def clean_missing_values(self, strategy: str = 'auto') -> None:
        """
        Limpiar valores faltantes según la estrategia especificada.
        
        Args:
            strategy: Estrategia de limpieza ('auto', 'drop', 'fill')
        """
        if self.df is None:
            raise ValueError("No hay datos cargados")
        
        logger.info(f"Limpiando valores faltantes con estrategia: {strategy}")
        
        initial_missing = self.df.isnull().sum().sum()
        
        if strategy == 'auto':
            # Estrategia automática basada en el tipo de columna
            for col in self.df.columns:
                missing_count = self.df[col].isnull().sum()
                if missing_count > 0:
                    if self.df[col].dtype in ['object', 'string']:
                        # Para columnas categóricas, usar 'Unknown'
                        self.df.loc[self.df[col].isnull(), col] = 'Unknown'
                        logger.info(f"Columna {col}: {missing_count} valores faltantes "
                                  f"reemplazados con 'Unknown'")
                    elif self.df[col].dtype in ['int64', 'float64']:
                        # Para columnas numéricas, usar mediana
                        median_val = self.df[col].median()
                        if pd.isna(median_val):
                            # Si la mediana es NaN, usar 0
                            median_val = 0
                        self.df.loc[self.df[col].isnull(), col] = median_val
                        logger.info(f"Columna {col}: {missing_count} valores faltantes "
                                  f"reemplazados con mediana ({median_val:.2f})")
        
        elif strategy == 'drop':
            self.df.dropna(inplace=True)
            logger.info("Eliminadas filas con valores faltantes")
        
        elif strategy == 'fill':
            # Llenar con valores específicos
            numeric_cols = self.df.select_dtypes(include=[np.number]).columns
            categorical_cols = self.df.select_dtypes(include=['object']).columns
            
            self.df[numeric_cols] = self.df[numeric_cols].fillna(0)
            self.df[categorical_cols] = self.df[categorical_cols].fillna('Unknown')
        
        final_missing = self.df.isnull().sum().sum()
        cleaned_count = initial_missing - final_missing
        
        logger.info(f"Valores faltantes limpiados: {cleaned_count}")
        self.cleaning_log.append(f"Missing values cleaned: {cleaned_count} values")
    
    def remove_duplicates(self) -> int:
        """
        Eliminar filas duplicadas.
        
        Returns:
            Número de filas duplicadas eliminadas
        """
        if self.df is None:
            raise ValueError("No hay datos cargados")
        
        initial_count = len(self.df)
        self.df.drop_duplicates(inplace=True)
        final_count = len(self.df)
        removed_count = initial_count - final_count
        
        logger.info(f"Filas duplicadas eliminadas: {removed_count}")
        self.cleaning_log.append(f"Duplicates removed: {removed_count} rows")
        
        return removed_count
    
    def optimize_data_types(self) -> None:
        """
        Optimizar tipos de datos para reducir uso de memoria.
        """
        if self.df is None:
            raise ValueError("No hay datos cargados")
        
        logger.info("Optimizando tipos de datos...")
        
        initial_memory = self.df.memory_usage(deep=True).sum() / 1024**2
        
        # Optimizar columnas numéricas
        for col in self.df.select_dtypes(include=['int64']).columns:
            col_min = self.df[col].min()
            col_max = self.df[col].max()
            
            if col_min >= np.iinfo(np.int8).min and col_max <= np.iinfo(np.int8).max:
                self.df[col] = self.df[col].astype(np.int8)
            elif col_min >= np.iinfo(np.int16).min and col_max <= np.iinfo(np.int16).max:
                self.df[col] = self.df[col].astype(np.int16)
            elif col_min >= np.iinfo(np.int32).min and col_max <= np.iinfo(np.int32).max:
                self.df[col] = self.df[col].astype(np.int32)
        
        # Optimizar columnas de punto flotante
        for col in self.df.select_dtypes(include=['float64']).columns:
            self.df[col] = pd.to_numeric(self.df[col], downcast='float')
        
        # Optimizar columnas categóricas
        for col in self.df.select_dtypes(include=['object']).columns:
            if self.df[col].nunique() / len(self.df) < 0.5:  # Si menos del 50% son únicos
                self.df[col] = self.df[col].astype('category')
        
        final_memory = self.df.memory_usage(deep=True).sum() / 1024**2
        memory_saved = initial_memory - final_memory
        
        logger.info(f"Memoria optimizada: {memory_saved:.2f} MB ahorrados "
                   f"({(memory_saved/initial_memory)*100:.1f}%)")
        self.cleaning_log.append(f"Memory optimized: {memory_saved:.2f} MB saved")
    
    def transform_dates(self) -> None:
        """
        Transformar columnas de fechas a formato datetime.
        """
        if self.df is None:
            raise ValueError("No hay datos cargados")
        
        logger.info("Transformando columnas de fechas...")
        
        # Buscar columnas que contengan 'DATE' en el nombre
        date_columns = [col for col in self.df.columns if 'DATE' in col.upper()]
        
        for col in date_columns:
            try:
                self.df[col] = pd.to_datetime(self.df[col], errors='coerce')
                logger.info(f"Columna {col} convertida a datetime")
                
                # Crear columnas adicionales de fecha
                self.df[f'{col}_YEAR'] = self.df[col].dt.year
                self.df[f'{col}_MONTH'] = self.df[col].dt.month
                self.df[f'{col}_DAY'] = self.df[col].dt.day
                self.df[f'{col}_DAYOFWEEK'] = self.df[col].dt.dayofweek
                
            except Exception as e:
                logger.warning(f"No se pudo convertir la columna {col}: {str(e)}")
        
        self.cleaning_log.append(f"Date columns transformed: {len(date_columns)} columns")
    
    def create_derived_features(self) -> None:
        """
        Crear características derivadas útiles para el análisis.
        """
        if self.df is None:
            raise ValueError("No hay datos cargados")
        
        logger.info("Creando características derivadas...")
        
        # Calcular margen si tenemos precio de venta y costo
        if 'PRICEEACH' in self.df.columns and 'MSRP' in self.df.columns:
            self.df['MARGIN'] = self.df['PRICEEACH'] - self.df['MSRP']
            self.df['MARGIN_PERCENTAGE'] = (
                (self.df['PRICEEACH'] - self.df['MSRP']) / self.df['PRICEEACH'] * 100
            )
            logger.info("Características de margen creadas")
        
        # Crear categorías de tamaño de venta
        if 'SALES' in self.df.columns:
            self.df['SALES_CATEGORY'] = pd.cut(
                self.df['SALES'],
                bins=[0, 1000, 5000, 10000, float('inf')],
                labels=['Small', 'Medium', 'Large', 'Very Large']
            )
            logger.info("Categorías de ventas creadas")
        
        # Crear indicador de trimestre
        if 'MONTH_ID' in self.df.columns:
            self.df['QUARTER'] = pd.cut(
                self.df['MONTH_ID'],
                bins=[0, 3, 6, 9, 12],
                labels=['Q1', 'Q2', 'Q3', 'Q4']
            )
            logger.info("Indicador de trimestre creado")
        
        self.cleaning_log.append("Derived features created")
    
    def save_cleaned_data(self, output_path: str) -> None:
        """
        Guardar datos limpios en formato CSV.
        
        Args:
            output_path: Ruta donde guardar el archivo limpio
        """
        if self.df is None:
            raise ValueError("No hay datos cargados")
        
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        self.df.to_csv(output_path, index=False)
        logger.info(f"Datos limpios guardados en: {output_path}")
        
        # Guardar log de limpieza
        log_file = output_file.parent / f"{output_file.stem}_cleaning_log.txt"
        with open(log_file, 'w') as f:
            f.write("Sales Data Cleaning Log\n")
            f.write("=" * 30 + "\n")
            for log_entry in self.cleaning_log:
                f.write(f"{log_entry}\n")
        
        logger.info(f"Log de limpieza guardado en: {log_file}")
    
    def get_cleaning_summary(self) -> Dict[str, any]:
        """
        Obtener resumen del proceso de limpieza.
        
        Returns:
            Diccionario con resumen de la limpieza
        """
        if self.df is None:
            raise ValueError("No hay datos cargados")
        
        return {
            'final_shape': self.df.shape,
            'memory_usage_mb': self.df.memory_usage(deep=True).sum() / 1024**2,
            'cleaning_log': self.cleaning_log,
            'data_types': self.df.dtypes.to_dict(),
            'missing_values': self.df.isnull().sum().to_dict()
        }


def main():
    """
    Función principal para ejecutar el proceso de limpieza.
    """
    # Configurar rutas
    input_file = "data/raw/sales_data_sample.csv"
    output_file = "data/processed/sales_data_cleaned.csv"
    
    try:
        # Inicializar limpiador
        cleaner = SalesDataCleaner(input_file)
        
        # Cargar datos
        cleaner.load_data()
        
        # Validar estructura
        validation = cleaner.validate_data_structure()
        print(f"Validación inicial: {validation}")
        
        # Proceso de limpieza
        cleaner.clean_missing_values(strategy='auto')
        cleaner.remove_duplicates()
        cleaner.optimize_data_types()
        cleaner.transform_dates()
        cleaner.create_derived_features()
        
        # Guardar datos limpios
        cleaner.save_cleaned_data(output_file)
        
        # Mostrar resumen
        summary = cleaner.get_cleaning_summary()
        print(f"Resumen final: {summary}")
        
        logger.info("Proceso de limpieza completado exitosamente")
        
    except Exception as e:
        logger.error(f"Error en el proceso de limpieza: {str(e)}")
        raise


if __name__ == "__main__":
    main()
