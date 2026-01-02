# 🔬 Fluorescence Analysis Toolkit

Una suite de herramientas para automatizar el análisis de imágenes de microscopía confocal. Incluye una macro de **Fiji/ImageJ** para procesamiento de imágenes por lotes y una **aplicación GUI en Python** para el análisis estadístico de los datos.

## 🚀 Características

### 1. Macro de ImageJ (`.ijm`)
- Procesamiento automático de archivos `.LIF` (Bio-Formats).
- Separación de canales (Azul, Verde, Rojo).
- Segmentación automática basada en el canal nuclear (DAPI/Azul).
- Generación de máscaras y medición de ROI.
- Exportación automática de resultados CSV e imágenes de control.

### 2. Aplicación Python (`.py`)
- Interfaz gráfica moderna (basada en `customtkinter`).
- Consolidación de datos crudos (CSV) de ImageJ.
- Filtrado de calidad (basado en área mínima de célula).
- Cálculo automático de:
  - Ratios de fluorescencia (Target/Núcleo).
  - Intensidades normalizadas (0-100%).
- Exportación a Excel listo para graficar.

## 📋 Requisitos

- **Fiji (ImageJ)** instalado para ejecutar la macro.
- **Python 3.8+**
- Librerías listadas en `requirements.txt`.

## ⚙️ Instalación y Uso

### Paso 1: Extracción de Datos (Fiji)
1. Abre Fiji.
2. Arrastra el archivo `src/macro_fiji.ijm` a la ventana de Fiji.
3. Ejecuta la macro y selecciona tu archivo de microscopía (`.lif`).
4. La macro generará una carpeta con archivos `.csv`.

### Paso 2: Análisis de Datos (Python)
1. Clona este repositorio:
   ```bash
   git clone [https://github.com/TU_USUARIO/fluorescence-analysis.git](https://github.com/TU_USUARIO/fluorescence-analysis.git)