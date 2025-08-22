import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from supabase import create_client, Client

# --- Configuración de página ---
st.set_page_config(
    page_title="Bike & Gear Dashboard",
    layout="wide"
)

st.title("📊 Dashboard Comercial - Bike & Gear")

# --- Conexión con Supabase ---
# ⚠️ Debes definir tus credenciales en "Secrets" de Streamlit Cloud
# En streamlit, pon en .streamlit/secrets.toml:
# [supabase]
# url = "https://TU_URL.supabase.co"
# key = "TU_API_KEY"

url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

# --- Cargar datos desde Supabase ---
@st.cache_data
def load_data():
    response = supabase.table("analisis_visualizacion_bikegear_2025").select("*").execute()
    df = pd.DataFrame(response.data)
    return df

df = load_data()

# --- Conversión de fechas ---
df["Fecha_Venta"] = pd.to_datetime(df["Fecha_Venta"], errors="coerce")

# --- KPIs ---
st.subheader("🔑 Indicadores Clave de Rendimiento (KPIs)")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Ventas Totales (S/.)", f"{df['Ingreso_Total'].sum():,.2f}")
with col2:
    st.metric("Ganancia Total (S/.)", f"{df['Ganancia'].sum():,.2f}")
with col3:
    st.metric("Número de Ventas", f"{df['ID_Venta'].count():,}")

# --- Evolución temporal ---
st.subheader("📈 Evolución Temporal de Ingresos")
df_sorted = df.groupby(df["Fecha_Venta"].dt.to_period("M")).sum(numeric_only=True).reset_index()
df_sorted["Fecha_Venta"] = df_sorted["Fecha_Venta"].astype(str)

fig, ax = plt.subplots()
ax.plot(df_sorted["Fecha_Venta"], df_sorted["Ingreso_Total"], marker="o")
ax.set_xlabel("Mes")
ax.set_ylabel("Ingresos Totales (S/.)")
ax.set_title("Tendencia de Ingresos Mensuales")
plt.xticks(rotation=45)
st.pyplot(fig)

# --- Top 5 productos más rentables ---
st.subheader("🏆 Top 5 Productos más Rentables")
top5 = df.groupby("Nombre_Producto")["Ganancia"].sum().nlargest(5)
st.bar_chart(top5)

# --- Filtros interactivos ---
st.subheader("🔍 Filtros Interactivos")
ciudad = st.selectbox("Selecciona una ciudad:", ["Todas"] + sorted(df["Ciudad_Tienda"].dropna().unique().tolist()))

df_filtrado = df.copy()
if ciudad != "Todas":
    df_filtrado = df_filtrado[df_filtrado["Ciudad_Tienda"] == ciudad]

st.write("📌 Mostrando datos para:", ciudad)
st.dataframe(df_filtrado.head(20))
