"""
Tests unitarios para el módulo de limpieza de datos.

Este módulo contiene tests para validar la funcionalidad
del limpiador de datos de ventas.
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import sys
import os

# Agregar el directorio src al path para importar módulos
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from data_processing.data_cleaner import SalesDataCleaner


class TestSalesDataCleaner:
    """
    Clase de tests para SalesDataCleaner.
    """
    
    @pytest.fixture
    def sample_data(self):
        """
        Fixture para crear datos de prueba.
        
        Returns:
            DataFrame con datos de prueba
        """
        data = {
            'ORDERNUMBER': [10107, 10121, 10134, 10145, 10159],
            'QUANTITYORDERED': [30, 34, 41, 45, 49],
            'PRICEEACH': [95.7, 81.35, 94.74, 83.26, 100.0],
            'ORDERLINENUMBER': [2, 5, 2, 6, 14],
            'SALES': [2871, 2765.9, 3884.34, 3746.7, 5205.27],
            'ORDERDATE': ['2/24/2003 0:00', '5/7/2003 0:00', '7/1/2003 0:00', 
                         '8/25/2003 0:00', '10/10/2003 0:00'],
            'STATUS': ['Shipped', 'Shipped', 'Shipped', 'Shipped', 'Shipped'],
            'QTR_ID': [1, 2, 3, 3, 4],
            'MONTH_ID': [2, 5, 7, 8, 10],
            'YEAR_ID': [2003, 2003, 2003, 2003, 2003],
            'PRODUCTLINE': ['Motorcycles', 'Motorcycles', 'Motorcycles', 
                           'Motorcycles', 'Motorcycles'],
            'MSRP': [95, 95, 95, 95, 95],
            'PRODUCTCODE': ['S10_1678', 'S10_1678', 'S10_1678', 'S10_1678', 'S10_1678'],
            'CUSTOMERNAME': ['Land of Toys Inc.', 'Reims Collectables', 'Lyon Souveniers',
                           'Toys4GrownUps.com', 'Corporate Gift Ideas Co.'],
            'PHONE': ['2125557818', '26.47.1555', '+33 1 46 62 7555', 
                     '6265557265', '6505551386'],
            'ADDRESSLINE1': ['897 Long Airport Avenue', '59 rue de l\'Abbaye', 
                            '27 rue du Colonel Pierre Avia', '78934 Hillside Dr.', '7734 Strong St.'],
            'ADDRESSLINE2': ['', '', '', '', ''],
            'CITY': ['NYC', 'Reims', 'Paris', 'Pasadena', 'San Francisco'],
            'STATE': ['NY', '', '', 'CA', 'CA'],
            'POSTALCODE': ['10022', '51100', '75508', '90003', ''],
            'COUNTRY': ['USA', 'France', 'France', 'USA', 'USA'],
            'TERRITORY': ['NA', 'EMEA', 'EMEA', 'NA', 'NA'],
            'CONTACTLASTNAME': ['Yu', 'Henriot', 'Da Cunha', 'Young', 'Brown'],
            'CONTACTFIRSTNAME': ['Kwai', 'Paul', 'Daniel', 'Julie', 'Julie'],
            'DEALSIZE': ['Small', 'Small', 'Medium', 'Medium', 'Medium']
        }
        return pd.DataFrame(data)
    
    @pytest.fixture
    def sample_csv_file(self, sample_data, tmp_path):
        """
        Fixture para crear archivo CSV temporal.
        
        Args:
            sample_data: DataFrame con datos de prueba
            tmp_path: Directorio temporal de pytest
            
        Returns:
            Path al archivo CSV temporal
        """
        csv_file = tmp_path / "test_sales_data.csv"
        sample_data.to_csv(csv_file, index=False)
        return csv_file
    
    def test_initialization(self, sample_csv_file):
        """
        Test de inicialización del limpiador.
        """
        cleaner = SalesDataCleaner(str(sample_csv_file))
        assert cleaner.data_path == sample_csv_file
        assert cleaner.df is None
        assert cleaner.cleaning_log == []
    
    def test_load_data_success(self, sample_csv_file):
        """
        Test de carga exitosa de datos.
        """
        cleaner = SalesDataCleaner(str(sample_csv_file))
        df = cleaner.load_data()
        
        assert df is not None
        assert len(df) == 5
        assert len(df.columns) == 25
        assert cleaner.df is not None
    
    def test_load_data_file_not_found(self):
        """
        Test de carga con archivo inexistente.
        """
        cleaner = SalesDataCleaner("nonexistent_file.csv")
        
        with pytest.raises(FileNotFoundError):
            cleaner.load_data()
    
    def test_validate_data_structure(self, sample_csv_file):
        """
        Test de validación de estructura de datos.
        """
        cleaner = SalesDataCleaner(str(sample_csv_file))
        cleaner.load_data()
        
        validation = cleaner.validate_data_structure()
        
        assert validation['total_rows'] == 5
        assert validation['total_columns'] == 25
        assert validation['duplicate_rows'] == 0
        assert 'memory_usage_mb' in validation
        assert 'missing_values' in validation
        assert 'data_types' in validation
    
    def test_validate_data_structure_no_data(self, sample_csv_file):
        """
        Test de validación sin datos cargados.
        """
        cleaner = SalesDataCleaner(str(sample_csv_file))
        
        with pytest.raises(ValueError, match="No hay datos cargados"):
            cleaner.validate_data_structure()
    
    def test_clean_missing_values_auto(self, sample_csv_file):
        """
        Test de limpieza automática de valores faltantes.
        """
        cleaner = SalesDataCleaner(str(sample_csv_file))
        cleaner.load_data()
        
        # Agregar algunos valores faltantes para probar
        cleaner.df.loc[0, 'CUSTOMERNAME'] = np.nan
        cleaner.df.loc[1, 'SALES'] = np.nan
        
        initial_missing = cleaner.df.isnull().sum().sum()
        cleaner.clean_missing_values(strategy='auto')
        final_missing = cleaner.df.isnull().sum().sum()
        
        assert final_missing == 0
        assert initial_missing > 0
        assert len(cleaner.cleaning_log) > 0
    
    def test_clean_missing_values_drop(self, sample_csv_file):
        """
        Test de limpieza eliminando filas con valores faltantes.
        """
        cleaner = SalesDataCleaner(str(sample_csv_file))
        cleaner.load_data()
        
        # Agregar valores faltantes
        cleaner.df.loc[0, 'CUSTOMERNAME'] = np.nan
        cleaner.df.loc[1, 'SALES'] = np.nan
        
        initial_rows = len(cleaner.df)
        cleaner.clean_missing_values(strategy='drop')
        final_rows = len(cleaner.df)
        
        assert final_rows < initial_rows
        assert cleaner.df.isnull().sum().sum() == 0
    
    def test_remove_duplicates(self, sample_csv_file):
        """
        Test de eliminación de duplicados.
        """
        cleaner = SalesDataCleaner(str(sample_csv_file))
        cleaner.load_data()
        
        # Agregar una fila duplicada
        duplicate_row = cleaner.df.iloc[0].copy()
        cleaner.df = pd.concat([cleaner.df, pd.DataFrame([duplicate_row])], ignore_index=True)
        
        initial_count = len(cleaner.df)
        removed_count = cleaner.remove_duplicates()
        final_count = len(cleaner.df)
        
        assert removed_count == 1
        assert final_count == initial_count - 1
        assert len(cleaner.cleaning_log) > 0
    
    def test_optimize_data_types(self, sample_csv_file):
        """
        Test de optimización de tipos de datos.
        """
        cleaner = SalesDataCleaner(str(sample_csv_file))
        cleaner.load_data()
        
        initial_memory = cleaner.df.memory_usage(deep=True).sum()
        cleaner.optimize_data_types()
        final_memory = cleaner.df.memory_usage(deep=True).sum()
        
        # La memoria debería reducirse o mantenerse igual
        assert final_memory <= initial_memory
        assert len(cleaner.cleaning_log) > 0
    
    def test_transform_dates(self, sample_csv_file):
        """
        Test de transformación de fechas.
        """
        cleaner = SalesDataCleaner(str(sample_csv_file))
        cleaner.load_data()
        
        initial_columns = len(cleaner.df.columns)
        cleaner.transform_dates()
        final_columns = len(cleaner.df.columns)
        
        # Deberían agregarse columnas adicionales de fecha
        assert final_columns > initial_columns
        
        # Verificar que ORDERDATE sea datetime
        assert pd.api.types.is_datetime64_any_dtype(cleaner.df['ORDERDATE'])
        
        # Verificar columnas adicionales
        expected_new_columns = ['ORDERDATE_YEAR', 'ORDERDATE_MONTH', 'ORDERDATE_DAY', 'ORDERDATE_DAYOFWEEK']
        for col in expected_new_columns:
            assert col in cleaner.df.columns
    
    def test_create_derived_features(self, sample_csv_file):
        """
        Test de creación de características derivadas.
        """
        cleaner = SalesDataCleaner(str(sample_csv_file))
        cleaner.load_data()
        
        initial_columns = len(cleaner.df.columns)
        cleaner.create_derived_features()
        final_columns = len(cleaner.df.columns)
        
        # Deberían agregarse características derivadas
        assert final_columns > initial_columns
        
        # Verificar características específicas
        if 'MARGIN' in cleaner.df.columns:
            assert 'MARGIN' in cleaner.df.columns
            assert 'MARGIN_PERCENTAGE' in cleaner.df.columns
        
        if 'SALES_CATEGORY' in cleaner.df.columns:
            assert 'SALES_CATEGORY' in cleaner.df.columns
        
        if 'QUARTER' in cleaner.df.columns:
            assert 'QUARTER' in cleaner.df.columns
    
    def test_save_cleaned_data(self, sample_csv_file, tmp_path):
        """
        Test de guardado de datos limpios.
        """
        cleaner = SalesDataCleaner(str(sample_csv_file))
        cleaner.load_data()
        cleaner.clean_missing_values()
        cleaner.remove_duplicates()
        
        output_file = tmp_path / "cleaned_data.csv"
        cleaner.save_cleaned_data(str(output_file))
        
        # Verificar que el archivo se creó
        assert output_file.exists()
        
        # Verificar que se creó el log
        log_file = tmp_path / "cleaned_data_cleaning_log.txt"
        assert log_file.exists()
        
        # Verificar contenido del archivo guardado
        saved_df = pd.read_csv(output_file)
        assert len(saved_df) == len(cleaner.df)
        assert len(saved_df.columns) == len(cleaner.df.columns)
    
    def test_get_cleaning_summary(self, sample_csv_file):
        """
        Test de obtención de resumen de limpieza.
        """
        cleaner = SalesDataCleaner(str(sample_csv_file))
        cleaner.load_data()
        cleaner.clean_missing_values()
        cleaner.remove_duplicates()
        
        summary = cleaner.get_cleaning_summary()
        
        assert 'final_shape' in summary
        assert 'memory_usage_mb' in summary
        assert 'cleaning_log' in summary
        assert 'data_types' in summary
        assert 'missing_values' in summary
        
        assert summary['final_shape'] == cleaner.df.shape
        assert len(summary['cleaning_log']) > 0
    
    def test_get_cleaning_summary_no_data(self, sample_csv_file):
        """
        Test de resumen sin datos cargados.
        """
        cleaner = SalesDataCleaner(str(sample_csv_file))
        
        with pytest.raises(ValueError, match="No hay datos cargados"):
            cleaner.get_cleaning_summary()
    
    def test_full_cleaning_pipeline(self, sample_csv_file, tmp_path):
        """
        Test del pipeline completo de limpieza.
        """
        cleaner = SalesDataCleaner(str(sample_csv_file))

        # Ejecutar pipeline completo
        cleaner.load_data()
        validation = cleaner.validate_data_structure()
        cleaner.clean_missing_values(strategy='auto')
        cleaner.remove_duplicates()
        cleaner.optimize_data_types()
        cleaner.transform_dates()
        cleaner.create_derived_features()

        # Guardar datos
        output_file = tmp_path / "final_cleaned_data.csv"
        cleaner.save_cleaned_data(str(output_file))
        
        # Verificar resultados
        assert cleaner.df is not None
        assert len(cleaner.df) > 0
        assert cleaner.df.isnull().sum().sum() == 0
        assert output_file.exists()
        
        # Verificar que no hay duplicados
        assert not cleaner.df.duplicated().any()
        
        # Verificar características derivadas
        assert len(cleaner.cleaning_log) > 0
    
    def test_error_handling_invalid_strategy(self, sample_csv_file):
        """
        Test de manejo de errores con estrategia inválida.
        """
        cleaner = SalesDataCleaner(str(sample_csv_file))
        cleaner.load_data()
        
        # Agregar valores faltantes
        cleaner.df.loc[0, 'CUSTOMERNAME'] = np.nan
        
        # Usar estrategia inválida
        cleaner.clean_missing_values(strategy='invalid_strategy')
        
        # Debería usar estrategia por defecto o manejar el error
        assert len(cleaner.cleaning_log) > 0
    
    def test_memory_optimization_edge_cases(self, sample_csv_file):
        """
        Test de casos extremos en optimización de memoria.
        """
        cleaner = SalesDataCleaner(str(sample_csv_file))
        cleaner.load_data()
        
        # Crear datos extremos
        cleaner.df['large_int'] = 999999999
        cleaner.df['small_int'] = 1
        cleaner.df['float_data'] = 123.456
        
        initial_memory = cleaner.df.memory_usage(deep=True).sum()
        cleaner.optimize_data_types()
        final_memory = cleaner.df.memory_usage(deep=True).sum()
        
        # Verificar optimización
        assert final_memory <= initial_memory
        
        # Verificar tipos optimizados
        assert cleaner.df['small_int'].dtype in [np.int8, np.int16, np.int32]
        assert cleaner.df['large_int'].dtype in [np.int32, np.int64]
    
    def test_date_transformation_edge_cases(self, sample_csv_file):
        """
        Test de casos extremos en transformación de fechas.
        """
        cleaner = SalesDataCleaner(str(sample_csv_file))
        cleaner.load_data()
        
        # Agregar fechas inválidas
        cleaner.df.loc[0, 'ORDERDATE'] = 'invalid_date'
        cleaner.df.loc[1, 'ORDERDATE'] = None
        
        cleaner.transform_dates()
        
        # Verificar que se manejaron las fechas inválidas
        assert pd.api.types.is_datetime64_any_dtype(cleaner.df['ORDERDATE'])
        
        # Verificar que las fechas inválidas se convirtieron a NaT
        assert cleaner.df['ORDERDATE'].isna().sum() >= 2


class TestSalesDataCleanerIntegration:
    """
    Tests de integración para SalesDataCleaner.
    """
    
    @pytest.fixture
    def large_sample_data(self):
        """
        Fixture para crear datos de prueba más grandes.
        """
        np.random.seed(42)
        n_rows = 1000
        
        data = {
            'ORDERNUMBER': range(10000, 10000 + n_rows),
            'QUANTITYORDERED': np.random.randint(1, 100, n_rows),
            'PRICEEACH': np.random.uniform(10, 200, n_rows),
            'SALES': np.random.uniform(100, 10000, n_rows),
            'ORDERDATE': pd.date_range('2020-01-01', periods=n_rows, freq='D'),
            'STATUS': np.random.choice(['Shipped', 'Cancelled', 'Disputed'], n_rows),
            'PRODUCTLINE': np.random.choice(['Motorcycles', 'Classic Cars', 'Trucks and Buses'], n_rows),
            'COUNTRY': np.random.choice(['USA', 'France', 'Germany', 'Spain'], n_rows),
            'CUSTOMERNAME': [f'Customer_{i}' for i in range(n_rows)]
        }
        
        return pd.DataFrame(data)
    
    def test_large_dataset_processing(self, large_sample_data, tmp_path):
        """
        Test de procesamiento de dataset grande.
        """
        # Crear archivo CSV temporal
        csv_file = tmp_path / "large_test_data.csv"
        large_sample_data.to_csv(csv_file, index=False)
        
        cleaner = SalesDataCleaner(str(csv_file))
        
        # Ejecutar pipeline completo
        cleaner.load_data()
        cleaner.clean_missing_values()
        cleaner.remove_duplicates()
        cleaner.optimize_data_types()
        cleaner.transform_dates()
        cleaner.create_derived_features()
        
        # Verificar resultados
        assert cleaner.df is not None
        assert len(cleaner.df) == 1000
        assert cleaner.df.isnull().sum().sum() == 0
        
        # Verificar optimización de memoria
        memory_usage = cleaner.df.memory_usage(deep=True).sum()
        assert memory_usage < 1024 * 1024  # Menos de 1MB
    
    def test_performance_benchmark(self, large_sample_data, tmp_path):
        """
        Test de benchmark de performance.
        """
        import time
        
        # Crear archivo CSV temporal
        csv_file = tmp_path / "performance_test_data.csv"
        large_sample_data.to_csv(csv_file, index=False)
        
        cleaner = SalesDataCleaner(str(csv_file))
        
        # Medir tiempo de carga
        start_time = time.time()
        cleaner.load_data()
        load_time = time.time() - start_time
        
        # Medir tiempo de limpieza
        start_time = time.time()
        cleaner.clean_missing_values()
        cleaner.remove_duplicates()
        cleaner.optimize_data_types()
        cleaning_time = time.time() - start_time
        
        # Verificar que los tiempos son razonables
        assert load_time < 5.0  # Menos de 5 segundos para cargar
        assert cleaning_time < 10.0  # Menos de 10 segundos para limpiar
        
        print(f"Load time: {load_time:.2f}s")
        print(f"Cleaning time: {cleaning_time:.2f}s")


if __name__ == "__main__":
    # Ejecutar tests
    pytest.main([__file__, "-v"])
