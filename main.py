import streamlit as st
from pages.productos import productos_page
from pages.ventas import ventas_page
from pages.reportes import reportes_page

st.set_page_config(
    page_title="Bike&Gear Tienda", 
    page_icon="🚴", 
    layout="wide",
    initial_sidebar_state="expanded"
)

st.sidebar.title("Bike&Gear")
st.sidebar.markdown("**Gestión Inteligente de tu Tienda**")

if "menu" not in st.session_state:
    st.session_state["menu"] = "productos"

opciones_menu = {
    "Productos": "productos",
    "Registrar Ventas": "ventas", 
    "Reportes": "reportes"
}

menu_seleccionado = st.sidebar.selectbox(
    "Navegación",
    list(opciones_menu.keys()),
    index=list(opciones_menu.keys()).index([k for k, v in opciones_menu.items() if v == st.session_state["menu"]][0])
)

st.session_state["menu"] = opciones_menu[menu_seleccionado]

if st.session_state["menu"] == "productos":
    productos_page()
elif st.session_state["menu"] == "ventas":
    ventas_page()
elif st.session_state["menu"] == "reportes":
    reportes_page()
