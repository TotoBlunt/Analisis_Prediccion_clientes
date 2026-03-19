"""
Aplicación Streamlit para análisis de clientes comerciales.

Permite:
- Cargar archivos CSV o Excel
- Visualizar métricas clave
- Analizar distribución de ingresos y churn
- Predecir riesgo de abandono de clientes
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression


def configurar_app():
    """
    Configura los parámetros iniciales de la aplicación.
    """
    st.set_page_config(
        page_title="Dashboard Comercial",
        layout="wide"
    )


def aplicar_estilos():
    """
    Aplica estilos personalizados a la interfaz.
    """
    st.markdown("""
        <style>
        body {
            background-color: #0E1117;
            color: #FAFAFA;
        }
        .metric-card {
            background: linear-gradient(135deg, #1f77b4, #4CAF50);
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            color: white;
            font-weight: bold;
            box-shadow: 0px 4px 15px rgba(0,0,0,0.4);
        }
        </style>
    """, unsafe_allow_html=True)


def mostrar_titulo():
    """
    Muestra el título principal de la aplicación.
    """
    st.title("📊 Dashboard de Clientes Comerciales")
    st.caption("Análisis de comportamiento y predicción de abandono")


def mostrar_instrucciones():
    """
    Muestra las instrucciones para el usuario.
    """
    st.info("""
    📌 El archivo debe contener las siguientes columnas:
    - ingresos_mensuales  
    - antiguedad_meses  
    - tipo_cliente  
    - servicios_contratados  
    - reclamos  
    - churn  
    """)


def cargar_datos():
    """
    Permite cargar un archivo CSV o Excel desde la barra lateral.

    Returns:
        pd.DataFrame: DataFrame con los datos cargados.
    """
    st.sidebar.subheader("📂 Cargar archivo")

    file = st.sidebar.file_uploader(
        "Sube tu archivo (CSV o Excel)",
        type=["csv", "xlsx"]
    )

    if file is not None:
        if file.name.endswith(".csv"):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)

        st.success("Archivo cargado correctamente ✅")
        return df
    else:
        st.warning("Sube un archivo para comenzar")
        st.stop()


def validar_columnas(df):
    """
    Valida que el DataFrame contenga las columnas necesarias.

    Args:
        df (pd.DataFrame): DataFrame a validar.
    """
    columnas_necesarias = [
        "ingresos_mensuales",
        "antiguedad_meses",
        "tipo_cliente",
        "servicios_contratados",
        "reclamos",
        "churn"
    ]

    faltantes = [col for col in columnas_necesarias if col not in df.columns]

    if faltantes:
        st.error(f"Faltan columnas necesarias: {faltantes}")
        st.stop()


def mostrar_preview(df):
    """
    Muestra una vista previa de los datos.

    Args:
        df (pd.DataFrame): DataFrame a visualizar.
    """
    st.subheader("👀 Vista previa de datos")
    st.dataframe(df.head())


def aplicar_filtros(df):
    """
    Aplica filtros por tipo de cliente.

    Args:
        df (pd.DataFrame): DataFrame original.

    Returns:
        pd.DataFrame: DataFrame filtrado.
    """
    st.sidebar.header("🔎 Filtros")

    tipo_cliente = st.sidebar.multiselect(
        "Tipo de cliente",
        options=df["tipo_cliente"].unique(),
        default=df["tipo_cliente"].unique()
    )

    return df[df["tipo_cliente"].isin(tipo_cliente)]


def mostrar_metricas(df):
    """
    Muestra indicadores clave del negocio.

    Args:
        df (pd.DataFrame): DataFrame filtrado.
    """
    st.subheader("📌 Indicadores clave")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h2>{len(df)}</h2>
            <p>Total Clientes</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h2>S/ {round(df["ingresos_mensuales"].mean(), 2)}</h2>
            <p>Ingreso Promedio</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h2>{round(df["churn"].mean()*100, 2)}%</h2>
            <p>Tasa de Churn</p>
        </div>
        """, unsafe_allow_html=True)


def mostrar_graficos(df):
    """
    Muestra gráficos de análisis de datos.

    Args:
        df (pd.DataFrame): DataFrame filtrado.
    """
    st.subheader("📈 Análisis de datos")

    col1, col2 = st.columns(2)

    with col1:
        fig, ax = plt.subplots()
        ax.hist(df["ingresos_mensuales"], bins=15)
        ax.axvline(df["ingresos_mensuales"].mean(), linestyle="--")
        ax.set_title("Distribución de ingresos con promedio")
        ax.set_xlabel("Ingresos mensuales")
        ax.set_ylabel("Cantidad de clientes")
        st.pyplot(fig)

    with col2:
        churn_tipo = df.groupby("tipo_cliente")["churn"].mean()
        st.write("### Tasa de abandono por tipo de cliente")
        st.bar_chart(churn_tipo)


def entrenar_modelo(df):
    """
    Entrena un modelo de regresión logística.

    Args:
        df (pd.DataFrame): DataFrame completo.

    Returns:
        LogisticRegression: Modelo entrenado.
    """
    X = df[[
        "ingresos_mensuales",
        "antiguedad_meses",
        "reclamos",
        "servicios_contratados"
    ]]
    y = df["churn"]

    model = LogisticRegression()
    model.fit(X, y)

    return model


def predecir_cliente(model):
    """
    Permite ingresar datos y predecir el churn de un cliente.

    Args:
        model (LogisticRegression): Modelo entrenado.
    """
    st.subheader("🤖 Predicción de riesgo de cliente")

    col1, col2 = st.columns(2)

    with col1:
        ingresos = st.number_input("Ingresos mensuales", 500, 5000, 1000)
        antiguedad = st.number_input("Antigüedad (meses)", 1, 60, 12)

    with col2:
        reclamos = st.number_input("Reclamos", 0, 10, 1)
        servicios = st.number_input("Servicios contratados", 1, 5, 2)

    if st.button("🔍 Evaluar cliente"):
        pred = model.predict([[ingresos, antiguedad, reclamos, servicios]])
        prob = model.predict_proba([[ingresos, antiguedad, reclamos, servicios]])[0][1]

        st.markdown("---")

        if pred[0] == 1:
            st.error(f"⚠️ Alto riesgo de abandono ({round(prob*100,2)}%)")
            st.write("👉 Recomendación: priorizar seguimiento comercial.")
        else:
            st.success(f"✅ Cliente estable ({round(prob*100,2)}% riesgo)")
            st.write("👉 Recomendación: mantener estrategia actual.")


def main():
    """
    Función principal que ejecuta la aplicación.
    """
    configurar_app()
    aplicar_estilos()
    mostrar_titulo()
    mostrar_instrucciones()

    df = cargar_datos()
    validar_columnas(df)
    mostrar_preview(df)

    df_filtrado = aplicar_filtros(df)
    mostrar_metricas(df_filtrado)
    mostrar_graficos(df_filtrado)

    modelo = entrenar_modelo(df)
    predecir_cliente(modelo)

    st.markdown("---")
    st.caption("Proyecto de análisis de datos aplicado a negocio")


if __name__ == "__main__":
    main()