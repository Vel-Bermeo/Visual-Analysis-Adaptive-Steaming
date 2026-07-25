# Análisis Visual para la Exploración de Variables Asociadas a la Selección Adaptativa de Bitrate

## Introducción

Este proyecto desarrolla un dashboard interactivo para explorar las variables que influyen en la selección adaptativa de bitrate (Adaptive Bitrate, ABR) durante la transmisión de video en streaming.

El análisis utiliza el conjunto de datos **Stanford Puffer**, el cual contiene métricas reales de red, reproducción y calidad de video. El dashboard fue desarrollado en **Python** utilizando **Streamlit** y **Plotly**, permitiendo analizar variables como Throughput, RTT, Buffer, SSIM, Retardo ACK y Resolución.

El proyecto también incluye un notebook con el proceso de preparación y transformación de los datos.

---

# Estructura del proyecto

```
Proyecto/
│
├── assets/
│   Recursos gráficos utilizados por el dashboard.
│
├── output/
│   Archivos procesados utilizados por la aplicación.
│
├── 01_preparacion_y_dashboard_puffer.ipynb
│   Notebook para la preparación y procesamiento de los datos.
│
├── appv2.py
│   Aplicación principal del dashboard desarrollada en Streamlit.
│
├── requirements.txt
│   Dependencias necesarias para ejecutar el proyecto.
│
└── README.md
│   Instrucciones para reproducir el proyecto.
```

---

# Requisitos

- Python 3.10 o superior
- pip

---

# Instalación

Instalar las dependencias:

```bash
pip install -r requirements.txt
```

---

# Ejecución del dashboard

Desde la carpeta principal ejecutar:

```bash
streamlit run appv2.py
```

Luego abrir:

```
http://localhost:8501
```

si el navegador no se abre automáticamente.

---

# Reproducción del proyecto

El proyecto incluye todos los archivos necesarios para reproducir el dashboard.

1. Instalar las dependencias mediante `requirements.txt`.
2. Verificar que las carpetas `assets` y `output` permanezcan dentro del directorio principal.
3. Ejecutar:

```bash
streamlit run appv2.py
```

Si se desea reproducir el procesamiento de datos desde el inicio, abrir el notebook:

```
01_preparacion_y_dashboard_puffer.ipynb
```

y ejecutar todas las celdas en orden. Los archivos procesados se almacenarán nuevamente en la carpeta `output`.

---

# Tecnologías utilizadas

- Python
- Streamlit
- Plotly
- Pandas
- NumPy
- Jupyter Notebook

---

# Autor

Evelyn Bermeo
