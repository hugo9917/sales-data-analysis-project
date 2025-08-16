# Proyecto de Análisis de Ventas - Roadmap de Datos

## 🎯 Objetivo del Proyecto

Este proyecto tiene como objetivo sentar bases sólidas en **SQL avanzado**, **Python para datos** y **buenas prácticas de desarrollo** mediante el análisis completo de un dataset de ventas.

## 📚 Aprendizajes Clave

### SQL Avanzado
- **Window Functions**: ROW_NUMBER(), RANK(), DENSE_RANK(), LAG(), LEAD()
- **CTEs (Common Table Expressions)**: WITH clauses para queries complejas
- **Subqueries**: Correlated, EXISTS, IN, ANY, ALL
- **Índices**: Optimización de consultas y performance
- **Joins avanzados**: SELF JOIN, CROSS JOIN, OUTER JOINs

### Pandas Avanzado y Optimización
- **Operaciones vectorizadas**: Aplicar funciones eficientemente
- **GroupBy avanzado**: Transform, filter, apply
- **Manejo de datos**: Merge, concat, pivot, melt
- **Optimización de memoria**: Dtypes, downcasting
- **Visualización**: Matplotlib, Seaborn, Plotly

### Buenas Prácticas de Código
- **PEP8**: Estilo de código Python
- **Logging**: Registro de eventos y debugging
- **Testing**: pytest para validación de datos
- **Documentación**: Docstrings y comentarios
- **Modularización**: Separación de responsabilidades

## 🏗️ Estructura del Proyecto

```
proyecto_analisis_roadmap/
├── data/
│   ├── raw/                    # Datos originales
│   ├── processed/              # Datos limpios
│   └── final/                  # Datos para visualización
├── src/
│   ├── data_processing/        # Scripts de limpieza
│   ├── sql_queries/           # Consultas SQL avanzadas
│   ├── analysis/              # Análisis exploratorio
│   └── utils/                 # Funciones auxiliares
├── tests/                     # Tests unitarios
├── notebooks/                 # Jupyter notebooks
├── docs/                      # Documentación
├── requirements.txt           # Dependencias
└── README.md                 # Este archivo
```

## 🚀 Recursos de Aprendizaje

### SQL
- [SQLBolt](https://sqlbolt.com/) - Tutorial interactivo
- [Mode Analytics SQL Tutorial](https://mode.com/sql-tutorial/)
- [DataCamp - Advanced SQL](https://www.datacamp.com/courses/advanced-sql)

### Python para Datos
- [Effective Pandas - Matt Harrison](https://github.com/mattharrison/effective-pandas)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Real Python - Pandas Tutorials](https://realpython.com/tutorials/pandas/)

### Buenas Prácticas
- [PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [Python Logging](https://docs.python.org/3/howto/logging.html)
- [pytest Documentation](https://docs.pytest.org/)

## 📊 Dataset: Sales Data Sample

El dataset contiene información de ventas con las siguientes características:

- **2,825 registros** de ventas
- **25 columnas** incluyendo:
  - Información de órdenes (ORDERNUMBER, ORDERDATE, STATUS)
  - Detalles de productos (PRODUCTLINE, PRODUCTCODE, MSRP)
  - Información de clientes (CUSTOMERNAME, COUNTRY, TERRITORY)
  - Métricas de ventas (QUANTITYORDERED, PRICEEACH, SALES)
  - Dimensiones temporales (YEAR_ID, MONTH_ID, QTR_ID)

## 🎯 Entregables del Proyecto

1. **Limpieza de datos en Pandas** con buenas prácticas
2. **Consultas SQL avanzadas** demostrando Window Functions, CTEs y subqueries
3. **Análisis exploratorio** con visualizaciones
4. **Dashboard en Power BI** con insights clave
5. **Documentación completa** del proceso y hallazgos

## 🛠️ Tecnologías Utilizadas

- **Python 3.8+**
- **Pandas** para manipulación de datos
- **SQLite/PostgreSQL** para consultas avanzadas
- **Jupyter Notebooks** para análisis exploratorio
- **Power BI** para visualización final
- **pytest** para testing
- **logging** para debugging

## 📈 Métricas de Éxito

- [ ] Implementar todas las Window Functions principales
- [ ] Crear CTEs complejas para análisis multi-dimensional
- [ ] Optimizar consultas con índices apropiados
- [ ] Aplicar PEP8 en todo el código Python
- [ ] Implementar logging estructurado
- [ ] Crear tests unitarios para funciones críticas
- [ ] Generar visualizaciones impactantes
- [ ] Documentar insights clave del negocio

---

**Autor**: [Tu Nombre]  
**Fecha**: [Fecha de inicio]  
**Versión**: 1.0.0
