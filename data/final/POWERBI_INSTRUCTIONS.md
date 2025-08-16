# 🚀 Instrucciones Paso a Paso para Power BI

## 📋 Resumen de Archivos Preparados

Hemos preparado todos los datos necesarios para crear un dashboard profesional en Power BI:

### 📊 Archivos de Datos
- **`powerbi_data.xlsx`** - Archivo Excel con 7 hojas optimizadas
- **`powerbi_csv/`** - Archivos CSV separados (alternativa)
- **`powerbi_guide.md`** - Guía técnica completa
- **`powerbi_dashboard_preview.html`** - Vista previa del dashboard

### 📈 Datasets Incluidos
1. **sales_fact** - 2,763 registros de ventas
2. **dim_customers** - 92 clientes únicos
3. **dim_products** - 109 productos únicos
4. **dim_countries** - 19 países
5. **sales_metrics** - 248 días de métricas
6. **temporal_analysis** - 132 registros temporales
7. **geographic_analysis** - 73 ubicaciones

---

## 🎯 Instrucciones Paso a Paso

### Paso 1: Preparar Power BI Desktop
1. **Abrir Power BI Desktop**
2. **Cerrar cualquier proyecto abierto**
3. **Asegurar que tienes la versión más reciente**

### Paso 2: Importar Datos
1. **Hacer clic en "Obtener datos"**
2. **Seleccionar "Excel"**
3. **Navegar a: `data/final/powerbi_data.xlsx`**
4. **Seleccionar todas las hojas:**
   - ✅ sales_fact
   - ✅ dim_customers
   - ✅ dim_products
   - ✅ dim_countries
   - ✅ sales_metrics
   - ✅ temporal_analysis
   - ✅ geographic_analysis
5. **Hacer clic en "Cargar"**

### Paso 3: Configurar Relaciones
1. **Ir a la vista "Modelo"**
2. **Crear las siguientes relaciones:**

```
sales_fact.CUSTOMERNAME → dim_customers.CUSTOMERNAME
sales_fact.PRODUCTCODE → dim_products.PRODUCTCODE
sales_fact.COUNTRY → dim_countries.COUNTRY
sales_fact.ORDERDATE → sales_metrics.order_date
```

3. **Configurar cardinalidad:**
   - Tipo: Muchos a uno (*:1)
   - Dirección de filtro: Única
   - Hacer activa: Sí

### Paso 4: Crear Medidas DAX

#### Medidas Básicas
```dax
Total Sales = SUM(sales_fact[SALES])
Total Orders = COUNTROWS(sales_fact)
Unique Customers = DISTINCTCOUNT(sales_fact[CUSTOMERNAME])
Average Order Value = DIVIDE([Total Sales], [Total Orders])
```

#### Medidas Avanzadas
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

### Paso 5: Crear Visualizaciones

#### Dashboard Principal

**1. KPI Cards (Tarjetas)**
- **Total Ventas**: Usar medida `[Total Sales]`
- **Total Órdenes**: Usar medida `[Total Orders]`
- **Clientes Únicos**: Usar medida `[Unique Customers]`
- **Valor Promedio**: Usar medida `[Average Order Value]`

**2. Gráfico de Línea - Tendencia de Ventas**
- **Eje X**: `sales_metrics[order_date]`
- **Eje Y**: `sales_metrics[daily_sales]`
- **Título**: "Tendencia de Ventas Diarias"

**3. Gráfico de Barras - Top Clientes**
- **Eje X**: `dim_customers[CUSTOMERNAME]`
- **Eje Y**: `dim_customers[total_sales]`
- **Filtro**: Top 10 por `total_sales`
- **Título**: "Top 10 Clientes por Ventas"

**4. Gráfico de Barras - Top Productos**
- **Eje X**: `dim_products[PRODUCTCODE]`
- **Eje Y**: `dim_products[total_sales]`
- **Color**: `dim_products[PRODUCTLINE]`
- **Filtro**: Top 15 por `total_sales`
- **Título**: "Top 15 Productos por Ventas"

**5. Mapa - Ventas por País**
- **Ubicación**: `dim_countries[COUNTRY]`
- **Tamaño**: `dim_countries[total_sales]`
- **Color**: `dim_countries[total_sales]`
- **Título**: "Ventas por País"

**6. Mapa de Calor - Análisis Temporal**
- **Eje X**: `temporal_analysis[month]`
- **Eje Y**: `temporal_analysis[day_of_week]`
- **Valores**: `temporal_analysis[total_sales]`
- **Título**: "Ventas por Día y Mes"

### Paso 6: Configurar Filtros y Segmentadores

**Filtros de Página:**
- **Período**: `sales_metrics[order_date]`
- **País**: `dim_countries[COUNTRY]`
- **Línea de Producto**: `dim_products[PRODUCTLINE]`

**Segmentadores:**
- **Año**: `temporal_analysis[year]`
- **Mes**: `temporal_analysis[month]`
- **Tamaño de Trato**: `sales_fact[DEALSIZE]`

### Paso 7: Aplicar Tema y Colores

**Tema Personalizado:**
- **Color Primario**: #1f77b4 (Azul)
- **Color Secundario**: #ff7f0e (Naranja)
- **Color Éxito**: #2ca02c (Verde)
- **Color Advertencia**: #d62728 (Rojo)
- **Color Neutro**: #7f7f7f (Gris)

**Tipografía:**
- **Títulos**: Segoe UI Bold, 16pt
- **Subtítulos**: Segoe UI Semibold, 14pt
- **Texto**: Segoe UI Regular, 12pt

### Paso 8: Optimizar Rendimiento

1. **Verificar relaciones**
2. **Optimizar consultas DAX**
3. **Comprimir datos**
4. **Probar interactividad**
5. **Verificar filtros**

---

## 🎨 Consejos de Diseño

### Layout Recomendado
```
┌─────────────────────────────────────────────────────────┐
│                    TÍTULO DEL DASHBOARD                 │
├─────────────────────────────────────────────────────────┤
│ [KPI1] [KPI2] [KPI3] [KPI4]                            │
├─────────────────────────────────────────────────────────┤
│ [Tendencia Ventas]        │ [Top Clientes]             │
│                           │                            │
├─────────────────────────────────────────────────────────┤
│ [Top Productos]           │ [Mapa de Calor]            │
│                           │                            │
├─────────────────────────────────────────────────────────┤
│                    [Mapa de Países]                    │
└─────────────────────────────────────────────────────────┘
```

### Mejores Prácticas
- **Usar colores consistentes**
- **Mantener jerarquía visual**
- **Incluir títulos descriptivos**
- **Agregar tooltips informativos**
- **Probar en diferentes dispositivos**

---

## 🔧 Solución de Problemas

### Error: "No se pueden crear relaciones"
- Verificar que los campos tengan el mismo tipo de datos
- Asegurar que no haya valores duplicados en las dimensiones

### Error: "Medida DAX no funciona"
- Verificar la sintaxis de la fórmula
- Asegurar que las relaciones estén configuradas correctamente

### Error: "Visualización no muestra datos"
- Verificar filtros aplicados
- Comprobar que los campos estén en los ejes correctos

---

## 📱 Optimización para Móvil

1. **Ajustar tamaño de visualizaciones**
2. **Usar fuentes legibles**
3. **Simplificar filtros**
4. **Probar en Power BI Mobile**

---

## 🚀 Próximos Pasos

### Análisis Avanzado
1. **Crear segmentación de clientes**
2. **Implementar análisis predictivo**
3. **Agregar alertas automáticas**
4. **Configurar actualizaciones programadas**

### Colaboración
1. **Publicar en Power BI Service**
2. **Compartir con stakeholders**
3. **Configurar permisos**
4. **Crear aplicaciones**

---

## 📞 Recursos Adicionales

- **Documentación oficial**: [Power BI Documentation](https://docs.microsoft.com/power-bi/)
- **Comunidad**: [Power BI Community](https://community.powerbi.com/)
- **Videos tutoriales**: [Power BI YouTube Channel](https://www.youtube.com/c/MicrosoftPowerBI)

---

*¡Tu dashboard está listo para impresionar! 🎉*

**Fecha de generación**: 2024-12-19
**Versión**: 1.0

