# 📊 Dashboard de Clientes 

Aplicación interactiva desarrollada con Streamlit para el análisis de
clientes y la predicción de riesgo de abandono (churn).

Este proyecto está orientado a apoyar la toma de decisiones en áreas
comerciales mediante el uso de datos.

------------------------------------------------------------------------

## 🚀 Demo de la aplicación

👉 Puedes probar la app aquí(Descargando el archivo de Data o teniendo un archivo con las columnas expuestas en el presente documento):\
[🔗 Ver aplicación en Streamlit](https://clientsprediction.streamlit.app/)

------------------------------------------------------------------------

## 🎯 Objetivo del proyecto

Analizar el comportamiento de clientes y detectar patrones que permitan:

-   Identificar clientes más relevantes
-   Detectar riesgo de abandono (churn)
-   Apoyar decisiones comerciales con datos

------------------------------------------------------------------------

## 📂 Funcionalidades principales

### 📌 1. Carga de datos

-   Permite subir archivos en formato **CSV o Excel**
-   Validación automática de columnas necesarias(se validaron columnas necesarias para tal proposito)
-   Visualización inicial del dataset

------------------------------------------------------------------------

### 📊 2. Indicadores clave

Se muestran métricas principales del negocio:

-   Total de clientes\
-   Ingreso promedio\
-   Tasa de churn (%)

------------------------------------------------------------------------

### 📈 3. Análisis de datos

#### 🔹 Distribución de ingresos

-   Muestra cómo se distribuyen los ingresos de los clientes
-   Incluye una línea de referencia con el promedio

#### 🔹 Tasa de abandono por tipo de cliente

-   Comparación del churn entre tipos de cliente

------------------------------------------------------------------------

### 🔎 4. Filtros interactivos

-   Filtrado por tipo de cliente
-   Actualización dinámica de métricas y gráficos

------------------------------------------------------------------------

### 🤖 5. Predicción de churn

Modelo de Machine Learning (Regresión Logística):

-   Predicción de riesgo de abandono
-   Probabilidad de churn (%)
-   Recomendación básica

------------------------------------------------------------------------

## 🛠️ Tecnologías utilizadas

-   Python\
-   Pandas\
-   Scikit-learn\
-   Matplotlib\
-   Streamlit

------------------------------------------------------------------------

## 📁 Estructura del proyecto

analisis_clientes_comerciales/

-   data/
-   app.py
-   requirements.txt
-   README.md

------------------------------------------------------------------------

## ▶️ Ejecución local

pip install -r requirements.txt\
streamlit run app.py

------------------------------------------------------------------------

## 📌 Notas

El archivo debe contener:

-   ingresos_mensuales\
-   antiguedad_meses\
-   tipo_cliente\
-   servicios_contratados\
-   reclamos\
-   churn

------------------------------------------------------------------------

## 👨‍💻 Autor

Jose Longa Mendoza

