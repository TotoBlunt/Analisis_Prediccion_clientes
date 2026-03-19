import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression

# -------------------------
# CONFIG
# -------------------------
st.set_page_config(
    page_title="Dashboard Comercial",
    layout="wide"
)

# -------------------------
# ESTILO
# -------------------------
st.markdown("""
    <style>
    body {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    .metric-card {
        background-color: #1c1f26;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0px 0px 10px rgba(0,0,0,0.3);
    }
    </style>
""", unsafe_allow_html=True)

# -------------------------
# TÍTULO
# -------------------------
st.title("📊 Dashboard de Clientes Comerciales")
st.caption("Análisis de comportamiento y predicción de abandono")

# -------------------------
# INSTRUCCIONES
# -------------------------
st.info("""
📌 El archivo debe contener las siguientes columnas:
- ingresos_mensuales  
- antiguedad_meses  
- tipo_cliente  
- servicios_contratados  
- reclamos  
- churn  
""")

# -------------------------
# CARGA DE ARCHIVO
# -------------------------
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
else:
    st.warning("Sube un archivo para comenzar")
    st.stop()

# -------------------------
# VALIDACIÓN
# -------------------------
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

# -------------------------
# VISTA PREVIA
# -------------------------
st.subheader("👀 Vista previa de datos")
st.dataframe(df.head())

# -------------------------
# FILTROS
# -------------------------
st.sidebar.header("🔎 Filtros")

tipo_cliente = st.sidebar.multiselect(
    "Tipo de cliente",
    options=df["tipo_cliente"].unique(),
    default=df["tipo_cliente"].unique()
)

df_filtrado = df[df["tipo_cliente"].isin(tipo_cliente)]

# -------------------------
# MÉTRICAS
# -------------------------
st.subheader("📌 Indicadores clave")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <h3>{len(df_filtrado)}</h3>
        <p>Clientes</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <h3>S/ {round(df_filtrado["ingresos_mensuales"].mean(), 2)}</h3>
        <p>Ingreso promedio</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <h3>{round(df_filtrado["churn"].mean()*100, 2)}%</h3>
        <p>Churn</p>
    </div>
    """, unsafe_allow_html=True)

# -------------------------
# GRÁFICOS
# -------------------------
st.subheader("📈 Análisis de datos")

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots()
    ax.hist(df_filtrado["ingresos_mensuales"])
    ax.set_title("Distribución de ingresos")
    st.pyplot(fig)

with col2:
    churn_tipo = df_filtrado.groupby("tipo_cliente")["churn"].mean()
    st.bar_chart(churn_tipo)

# -------------------------
# MODELO
# -------------------------
X = df[[
    "ingresos_mensuales",
    "antiguedad_meses",
    "reclamos",
    "servicios_contratados"
]]
y = df["churn"]

model = LogisticRegression()
model.fit(X, y)

# -------------------------
# PREDICCIÓN
# -------------------------
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

# -------------------------
# FOOTER
# -------------------------
st.markdown("---")
st.caption("Proyecto de análisis de datos aplicado a negocio")