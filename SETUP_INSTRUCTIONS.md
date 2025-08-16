# 🚀 Instrucciones de Configuración del Proyecto

## 📋 Archivos Eliminados para GitHub

Los siguientes archivos fueron eliminados para mantener el repositorio ligero:

### **Archivos de Datos (se regeneran automáticamente):**
- `data/processed/sales_analysis.db` - Base de datos SQLite
- `data/final/powerbi_data.xlsx` - Datos para Power BI
- `data/final/*.png` - Imágenes de análisis
- `data/final/interactive_dashboard.html` - Dashboard interactivo

### **Archivos de Desarrollo:**
- `venv/` - Entorno virtual (se recrea)
- `.pytest_cache/` - Cache de tests
- `logs/` - Archivos de log
- `*.pbix` - Archivos Power BI locales

## 🔄 Cómo Regenerar los Archivos

### **1. Configurar el entorno:**
```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno (Windows)
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### **2. Ejecutar el análisis completo:**
```bash
# Ejecutar todo el pipeline
python main.py
```

### **3. Generar datos para Power BI:**
```bash
# Generar archivos Power BI
python src/analysis/powerbi_simple.py
```

### **4. Crear visualizaciones:**
```bash
# Generar dashboard preview
python src/analysis/powerbi_dashboard_preview.py
```

## 📊 Resultados Esperados

Después de ejecutar los comandos anteriores, tendrás:

- ✅ **Base de datos SQLite** con datos limpios
- ✅ **Archivo Excel** para Power BI
- ✅ **Imágenes de análisis** (PNG)
- ✅ **Dashboard interactivo** (HTML)
- ✅ **Logs de procesamiento**

## 🎯 Archivos Importantes que se Mantienen

- 📁 **Código fuente** (`src/`)
- 📁 **Tests** (`tests/`)
- 📁 **Documentación** (`docs/`, `README.md`)
- 📁 **Datos originales** (`data/raw/sales_data_sample.csv`)
- 📁 **Datos procesados** (`data/processed/sales_data_cleaned.csv`)
- 📁 **Guías Power BI** (`data/final/POWERBI_INSTRUCTIONS.md`)

## ⚡ Comando Rápido

Para configurar todo de una vez:
```bash
python setup.py
```

---

**Nota**: Todos los archivos eliminados se pueden regenerar ejecutando el pipeline de análisis. Esto mantiene el repositorio limpio y profesional para GitHub.
