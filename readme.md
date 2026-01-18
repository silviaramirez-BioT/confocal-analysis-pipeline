# 🔬 Fluorescence Analysis Pipeline: Membrane & Intracellular Quantification

[![Fiji](https://img.shields.io/badge/Platform-Fiji%2FImageJ-blue)](https://imagej.net/software/fiji/)
[![Python](https://img.shields.io/badge/Python-3.12-green)](https://www.python.org/)
[![Status](https://img.shields.io/badge/Status-Active-success)]()

Una suite de herramientas bioinformáticas diseñada para la **cuantificación semi-automatizada de biomoléculas parietales e intracelulares** (como Laminarina, Alginato y lípidos neutros) en imágenes de microscopía confocal.

Este repositorio contiene un flujo de trabajo dual:
1.  **Fiji (ImageJ) Macro:** Segmentación y extracción de datos (MFI, IntDen, %Área).
2.  **Python App:** Limpieza de datos, normalización y estadística robusta.

---

## 🚀 Características Principales

### 🟢 1. Procesamiento de Imágenes (Fiji/ImageJ)
El algoritmo utiliza una **estrategia de segmentación híbrida** basada en una proyección compuesta (*Merged Mask*). Suma las intensidades de todos los canales (Azul+Verde+Rojo) para asegurar la detección de células con baja señal nuclear pero alta expresión de marcadores.

* **Pre-procesamiento:** Sustracción de fondo (*Rolling Ball*, 50px) y suavizado (*Gaussian Blur*, sigma=2).
* **Segmentación:** Algoritmo *Triangle* (ideal para señales débiles) + *Watershed* para separación celular.
* **Formatos soportados:** Archivos nativos `.LIF` (Leica), `.CZI` (Zeiss) y `.TIF`.

### 🔵 2. Análisis Estadístico (Python)
Una aplicación gráfica (GUI) construida con `customtkinter` y `scipy.stats`.

* **Detección de Bits:** Identifica automáticamente si la imagen es de 8, 12 o 16 bits para escalar las intensidades correctamente.
* **Normalización:** Calcula Ratios (Señal/Núcleo) para mitigar la variabilidad técnica de la adquisición.
* **Estadística Robusta:** Evalúa la normalidad (Shapiro-Wilk) y reporta **Mediana + Rango Intercuartílico (IQR)** para evitar sesgos por *outliers* biológicos (células hiperfluorescentes).
* **Salida:** Excel multipestaña con datos crudos, resumen estadístico y guía de interpretación.

---

## 🛠️ Selección de la Macro (Fiji)

Este repositorio incluye **3 versiones** de la macro en lenguaje Java (`.ijm`), diseñadas para distintos niveles de intervención manual. Elige la que se adapte a la calidad de tus imágenes:

| Archivo                 | Nombre              | Descripción                                                                                                  | ¿Cuándo usarla?                                                                            |
| :---------------------- | :------------------ | :----------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------- |
| `fiji-no-editable.txt`  | **Modo Automático** | Procesa carpetas enteras a alta velocidad sin detenerse.                                                     | Imágenes limpias, sin "basura" y con células bien separadas.                               |
| `fiji-ROI-editable.txt` | **Modo Curaduría**  | Genera la máscara automática pero **se pausa** para que valides, borres errores o agregues células omitidas. | Imágenes estándar donde se requiere control de calidad humano.                             |
| `ROI-creado.txt`        | **Modo Manual**     | Prepara la imagen y canales, pero **no detecta nada**. Se pausa para que tú dibujes los ROIs desde cero.     | Imágenes muy complejas, con mucho ruido o células amontonadas que el auto-threshold falla. |

---

## 📖 Guía de Instalación y Uso

### Paso 1: Configurar Fiji (ImageJ)
1.  Descarga el archivo `.txt` de la macro que deseas usar (ver tabla arriba).
2.  Abre Fiji y ve a `Plugins > New > Macro`.
3.  Copia y pega el código del archivo de texto.
4.  Guarda el archivo con extensión `.ijm` (ej: `Analisis_Membrana.ijm`).
5.  Para ejecutar: `Plugins > Macros > Run...` y selecciona tu archivo.

### Paso 2: Ejecutar el Análisis
1.  Al correr la macro, selecciona si procesarás una **Carpeta** o un **Archivo único**.
2.  Si usas una macro editable, el programa se detendrá mostrando la ventana *Action Required*.
    * **Borrar:** Selecciona el ROI y pulsa `Delete`.
    * **Agregar:** Usa la herramienta *Freehand*, dibuja y pulsa `t`.
    * **Finalizar:** Pulsa `OK` para continuar con la siguiente imagen.

### Paso 3: Procesamiento de Datos (Python)
1.  Ejecuta `IR-2.1_GUI.exe` (o corre el script `.py`).
2.  Carga el archivo `.csv` generado por Fiji (usualmente en la carpeta `03_Resultados`).
3.  Haz clic en **"Generar Reporte"**.
4.  Obtendrás un Excel con 3 pestañas: Datos, Estadística y Guía.

---

## 📊 Interpretación de Resultados

El reporte final ofrece métricas clave para responder distintas preguntas biológicas:

### 1. ¿Cuánto marcador hay? (Intensidad/Abundancia)
* **Ratio Verde/Azul (o Rojo/Azul):** Es la métrica más fiable. Divide la señal del marcador entre la señal del núcleo (DAPI/Hoechst). Corrige errores de foco o iluminación.
* **IntDen (Densidad Integrada):** La suma total de fluorescencia. Útil para medir la "carga total" acumulada en la célula.

### 2. ¿Cómo está distribuido? (Cobertura)
* **Perc_Area (%):** Porcentaje de la célula ocupada por la señal.
    * *Bajo % + Alta Intensidad:* Señal puntual (vesículas).
    * *Alto % + Alta Intensidad:* Señal distribuida (pared celular completa).

---

## 📚 Referencias Metodológicas

Este flujo de trabajo sigue protocolos validados para cuantificación biológica:

1.  **do Couto, F. M., et al.** (2020). Measuring Intracellular Vesicle Density and Dispersion Using Fluorescence Microscopy. *Bio-protocol*. DOI: 10.21769/BioProtoc.3703.
2.  **Hulsey-Vincent, H., et al.** (2023). A Fiji process for quantifying fluorescent puncta. *microPublication Biology*. DOI: 10.17912/micropub.biology.001003.
3.  **Deng, L., et al.** (2025). Protocol for Quantifying Foci in Immunofluorescence. *Bio-protocol*. DOI: 10.21769/BioProtoc.5421.

---

### 📝 Créditos
Desarrollado para el análisis de biomoléculas en biotecnología.
**Autor:** M.Sc. Silvia Ramirez
