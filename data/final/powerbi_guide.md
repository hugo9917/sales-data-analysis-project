# Guía para Power BI - Análisis de Ventas

## 📊 Datasets Disponibles

### 1. **sales_fact** - Tabla Principal de Hechos
- **Descripción**: Datos de ventas detallados
- **Registros**: ~2,800 ventas
- **Columnas clave**: ORDERNUMBER, ORDERDATE, CUSTOMERNAME, PRODUCTCODE, SALES

### 2. **dim_customers** - Dimensión de Clientes
- **Descripción**: Información agregada por cliente
- **Registros**: ~350 clientes únicos
- **Columnas clave**: CUSTOMERNAME, COUNTRY, total_sales, avg_order_value

### 3. **dim_products** - Dimensión de Productos
- **Descripción**: Información agregada por producto
- **Registros**: ~100 productos únicos
- **Columnas clave**: PRODUCTCODE, PRODUCTLINE, total_sales, total_quantity

### 4. **dim_countries** - Dimensión de Países
- **Descripción**: Información agregada por país
- **Registros**: ~20 países
- **Columnas clave**: COUNTRY, total_sales, unique_customers

### 5. **sales_metrics** - Métricas de Ventas
- **Descripción**: Métricas agregadas por día
- **Registros**: ~200 días
- **Columnas clave**: order_date, daily_sales, daily_orders, avg_order_value

### 6. **temporal_analysis** - Análisis Temporal
- **Descripción**: Análisis por año, mes y día de la semana
- **Registros**: ~500 registros temporales
- **Columnas clave**: year, month, day_of_week, total_sales

### 7. **geographic_analysis** - Análisis Geográfico
- **Descripción**: Análisis por país y ciudad
- **Registros**: ~100 ubicaciones
- **Columnas clave**: COUNTRY, CITY, total_sales, unique_customers

## 🎯 Visualizaciones Recomendadas

### Dashboard Principal
1. **KPI Cards**:
   - Total de Ventas: `SUM(sales_fact[SALES])`
   - Número de Órdenes: `COUNTROWS(sales_fact)`
   - Clientes Únicos: `DISTINCTCOUNT(sales_fact[CUSTOMERNAME])`
   - Valor Promedio por Orden: `AVERAGE(sales_fact[SALES])`

2. **Gráficos de Línea**:
   - Ventas por Día: `sales_metrics[order_date]` vs `sales_metrics[daily_sales]`
   - Órdenes por Día: `sales_metrics[order_date]` vs `sales_metrics[daily_orders]`

3. **Gráficos de Barras**:
   - Top 10 Clientes: `dim_customers[CUSTOMERNAME]` vs `dim_customers[total_sales]`
   - Top 10 Productos: `dim_products[PRODUCTCODE]` vs `dim_products[total_sales]`
   - Ventas por País: `dim_countries[COUNTRY]` vs `dim_countries[total_sales]`

4. **Mapa**:
   - Ventas por País: Usar `geographic_analysis` con campo COUNTRY

### Dashboard de Análisis Detallado
1. **Tabla de Clientes**:
   - Todas las columnas de `dim_customers`
   - Filtros por país y rango de ventas

2. **Análisis de Productos**:
   - Todas las columnas de `dim_products`
   - Gráfico de dispersión: cantidad vs valor

3. **Análisis Temporal**:
   - Gráfico de calor: `temporal_analysis[month]` vs `temporal_analysis[day_of_week]`
   - Gráfico de líneas por año

## 🔗 Relaciones en Power BI

### Modelo de Datos
```
sales_fact (1) → (1) dim_customers [CUSTOMERNAME]
sales_fact (1) → (1) dim_products [PRODUCTCODE]
sales_fact (1) → (1) dim_countries [COUNTRY]
sales_fact (1) → (1) sales_metrics [ORDERDATE]
```

### Configuración de Relaciones
1. **sales_fact.CUSTOMERNAME** → **dim_customers.CUSTOMERNAME**
2. **sales_fact.PRODUCTCODE** → **dim_products.PRODUCTCODE**
3. **sales_fact.COUNTRY** → **dim_countries.COUNTRY**
4. **sales_fact.ORDERDATE** → **sales_metrics.order_date**

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
VAR PreviousSales = CALCULATE([Total Sales], DATEADD(sales_metrics[order_date], -1, MONTH))
RETURN
DIVIDE(CurrentSales - PreviousSales, PreviousSales)

Customer Retention = 
VAR CurrentCustomers = [Unique Customers]
VAR PreviousCustomers = CALCULATE([Unique Customers], DATEADD(sales_metrics[order_date], -1, MONTH))
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
