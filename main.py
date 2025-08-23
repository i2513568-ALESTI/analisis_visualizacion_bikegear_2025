import streamlit as st
from streamlit_option_menu import option_menu
from app_pages.productos import productos_page
from app_pages.ventas import ventas_page
from app_pages.reportes import reportes_page

st.set_page_config(
    page_title="Bike&Gear Admin", 
    page_icon="🚴", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---- SIDEBAR ----
with st.sidebar:
    st.title("🚴 Bike&Gear")

    menu_seleccionado = option_menu(
        "Navegación",
        ["Productos", "Registrar Ventas", "Reportes"],
        icons=["box", "cart-plus", "bar-chart"],  # iconos de Bootstrap
        menu_icon="list",  
        default_index=0
    )

# ---- CONTENIDO ----
if menu_seleccionado == "Productos":
    productos_page()
elif menu_seleccionado == "Registrar Ventas":
    ventas_page()
elif menu_seleccionado == "Reportes":
    reportes_page()
