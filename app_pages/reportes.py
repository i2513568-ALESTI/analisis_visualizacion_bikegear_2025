# reportes.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import folium
from streamlit_folium import folium_static
from datetime import datetime
from config.supabase_client import get_client
from utils.helpers import to_python_type

supabase = get_client()

# Diccionario de coordenadas para ciudades principales de Sudamérica
CIUDADES_COORDENADAS = {
    # Perú (prioridad alta)
    'Lima': [-12.0464, -77.0428],
    'Arequipa': [-16.4090, -71.5375],
    'Trujillo': [-8.1090, -79.0215],
    'Chiclayo': [-6.7760, -79.8443],
    'Piura': [-5.1945, -80.6328],
    'Cusco': [-13.5167, -71.9789],
    'Iquitos': [-3.7491, -73.2538],
    'Chimbote': [-9.0745, -78.5936],
    'Huancayo': [-12.0677, -75.2096],
    'Tacna': [-18.0120, -70.2499],
    'Ica': [-14.0677, -75.7286],
    'Cajamarca': [-7.1617, -78.5128],
    'Pucallpa': [-8.3833, -74.5500],
    'Sullana': [-4.9039, -80.6853],
    'Chincha Alta': [-13.4500, -76.1333],
    'Huaraz': [-9.5333, -77.5333],
    'Ayacucho': [-13.1583, -74.2239],
    'Tarapoto': [-6.4833, -76.3667],
    'Puno': [-15.8333, -70.0333],
    'Tumbes': [-3.5667, -80.4500],
    'Moquegua': [-17.2000, -70.9333],
    'Huaral': [-11.5000, -77.2000],
    'Barranca': [-10.7500, -77.7667],
    'Huacho': [-11.1000, -77.6000],
    'Chancay': [-11.5667, -77.2667],
    'Cañete': [-13.0833, -76.4000],
    'Chincha Baja': [-13.4500, -76.1333],
    'Pisco': [-13.7167, -76.2000],
    'Nasca': [-14.8333, -74.9500],
    'Camana': [-16.6167, -72.7167],
    'Mollendo': [-17.0167, -72.0167],
    'Ilo': [-17.6333, -71.3333],
    'Tacna': [-18.0120, -70.2499],
    'Moquegua': [-17.2000, -70.9333],
    'Arequipa': [-16.4090, -71.5375],
    'Cusco': [-13.5167, -71.9789],
    'Puno': [-15.8333, -70.0333],
    'Juliaca': [-15.4833, -70.1333],
    'Ayacucho': [-13.1583, -74.2239],
    'Huancayo': [-12.0677, -75.2096],
    'Huaraz': [-9.5333, -77.5333],
    'Cajamarca': [-7.1617, -78.5128],
    'Chiclayo': [-6.7760, -79.8443],
    'Trujillo': [-8.1090, -79.0215],
    'Piura': [-5.1945, -80.6328],
    'Tumbes': [-3.5667, -80.4500],
    'Iquitos': [-3.7491, -73.2538],
    'Pucallpa': [-8.3833, -74.5500],
    'Tarapoto': [-6.4833, -76.3667],
    'Chimbote': [-9.0745, -78.5936],
    'Sullana': [-4.9039, -80.6853],
    'Chincha Alta': [-13.4500, -76.1333],
    'Huaral': [-11.5000, -77.2000],
    'Barranca': [-10.7500, -77.7667],
    'Huacho': [-11.1000, -77.6000],
    'Chancay': [-11.5667, -77.2667],
    'Cañete': [-13.0833, -76.4000],
    'Chincha Baja': [-13.4500, -76.1333],
    'Pisco': [-13.7167, -76.2000],
    'Nasca': [-14.8333, -74.9500],
    'Camana': [-16.6167, -72.7167],
    'Mollendo': [-17.0167, -72.0167],
    'Ilo': [-17.6333, -71.3333],
    'Juliaca': [-15.4833, -70.1333],
    
    # Otros países
    'Bogotá': [4.7110, -74.0721],
    'Medellín': [6.2442, -75.5812],
    'Cali': [3.4516, -76.5320],
    'Quito': [-0.2299, -78.5249],
    'Guayaquil': [-2.1894, -79.8891],
    'Santiago': [-33.4489, -70.6693],
    'Valparaíso': [-33.0472, -71.6127],
    'La Paz': [-16.4897, -68.1193],
    'Santa Cruz': [-17.7833, -63.1821],
    'Caracas': [10.4806, -66.9036],
    'Maracaibo': [10.6427, -71.6125],
    'Brasília': [-15.7942, -47.8822],
    'São Paulo': [-23.5505, -46.6333],
    'Rio de Janeiro': [-22.9068, -43.1729],
    'Buenos Aires': [-34.6118, -58.3960],
    'Córdoba': [-31.4167, -64.1833],
    'Montevideo': [-34.9011, -56.1645],
    'Asunción': [-25.2637, -57.5759],
    'Ciudad de México': [19.4326, -99.1332],
    'Guadalajara': [20.6597, -103.3496],
    'Monterrey': [25.6866, -100.3161],
    'Panamá': [8.5380, -80.7821],
    'San José': [9.9281, -84.0907],
    'Managua': [12.1364, -86.2514],
    'Tegucigalpa': [14.0723, -87.1921],
    'San Salvador': [13.6929, -89.2182],
    'Guatemala': [14.6349, -90.5069],
    'Belmopán': [17.2534, -88.7713],
    'Kingston': [17.9712, -76.7926],
    'Santo Domingo': [18.4861, -69.9312],
    'San Juan': [18.4655, -66.1057],
    'Havana': [23.1136, -82.3666]
}

def get_coordinates(ciudad):
    """Obtener coordenadas para una ciudad"""
    return CIUDADES_COORDENADAS.get(ciudad, [0, 0])

def reportes_page():
    st.header("📊 Dashboard de Reportes")

    try:
        # --- Obtener datos desde Supabase ---
        ventas = supabase.table("analisis_ventas_bikegear_2025").select("*").execute().data

        if ventas:
            df_ventas = pd.DataFrame(ventas)

            # --- Conversión de tipos ---
            if "Ingreso_Total" in df_ventas.columns:
                df_ventas["Ingreso_Total"] = df_ventas["Ingreso_Total"].apply(to_python_type)
            if "Ganancia" in df_ventas.columns:
                df_ventas["Ganancia"] = df_ventas["Ganancia"].apply(to_python_type)

            # =====================
            #  MÉTRICAS PRINCIPALES
            # =====================
            st.markdown("### 📌 Métricas Principales")
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                ingreso_total = df_ventas['Ingreso_Total'].sum() if 'Ingreso_Total' in df_ventas.columns else 0
                st.metric("Ingreso Total", f"S/. {ingreso_total:,.2f}")
            with col2:
                ganancia_total = df_ventas['Ganancia'].sum() if 'Ganancia' in df_ventas.columns else 0
                st.metric("Ganancias", f"S/. {ganancia_total:,.2f}")
            with col3:
                ticket_promedio = df_ventas['Ingreso_Total'].mean() if 'Ingreso_Total' in df_ventas.columns and len(df_ventas) > 0 else 0
                st.metric("Ticket Promedio", f"S/. {ticket_promedio:,.2f}")
            with col4:
                st.metric("Número de Ventas", f"{len(df_ventas)}")

            st.markdown("---")

            # =====================
            #  GRAFICA DE INGRESO POR UBICACIÓN
            # =====================
            st.markdown("### 📈 Total de Ingreso por Ubicación")

            # Verificar si existe la columna Ciudad_Cliente para ubicación
            if "Ciudad_Cliente" in df_ventas.columns:
                ingresos_ubicacion = df_ventas.groupby("Ciudad_Cliente")["Ingreso_Total"].sum()
                
                # Crear gráfico de barras
                fig, ax = plt.subplots(figsize=(10, 6))
                ingresos_ubicacion.plot(kind="bar", ax=ax, color="orange")
                ax.set_title("Total de Ingresos por Ubicación", fontsize=14, fontweight='bold')
                ax.set_ylabel("Ingresos (S/.)", fontsize=12)
                ax.set_xlabel("Ubicación", fontsize=12)
                ax.tick_params(axis='x', rotation=45)
                
                # Agregar valores en las barras
                for i, v in enumerate(ingresos_ubicacion.values):
                    ax.text(i, v + (v * 0.01), f'S/. {v:,.0f}', ha='center', va='bottom', fontweight='bold')
                
                plt.tight_layout()
                st.pyplot(fig)
                
                # =====================
                #  MAPA DE GOOGLE MAPS (ESTILO LOOKER)
                # =====================
                st.markdown("### 🗺️ Mapa de Ingresos por Ubicación")
                
                # Crear mapa centrado en Perú (como en la imagen)
                mapa = folium.Map(
                    location=[-9.1900, -75.0152],  # Centro de Perú
                    zoom_start=5,
                    tiles='https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',
                    attr='Google Maps'
                )
                
                # Calcular estadísticas para el escalado
                min_ingreso = ingresos_ubicacion.min()
                max_ingreso = ingresos_ubicacion.max()
                mean_ingreso = ingresos_ubicacion.mean()
                
                # Agregar marcadores para cada ciudad
                for ciudad, ingreso in ingresos_ubicacion.items():
                    coords = get_coordinates(ciudad)
                    if coords != [0, 0]:  # Solo agregar si tenemos coordenadas
                        # Calcular el tamaño del círculo basado en el ingreso (escalado como en Looker)
                        radio = max(8, min(40, 8 + ((ingreso - min_ingreso) / (max_ingreso - min_ingreso)) * 32))
                        
                        # Color basado en el ingreso (rojo para alto, naranja para bajo)
                        color = '#FF0000' if ingreso > mean_ingreso else '#FFA500'
                        
                        folium.CircleMarker(
                            location=coords,
                            radius=radio,
                            popup=f"<b>{ciudad}</b><br><b>Ingreso_Total:</b> {ingreso:,.2f}",
                            tooltip=f"{ciudad}<br>Ingreso_Total: {ingreso:,.2f}",
                            color=color,
                            fill=True,
                            fillOpacity=0.8,
                            weight=1
                        ).add_to(mapa)
                
                # Mostrar el mapa
                folium_static(mapa, width=900, height=600)
                
                # Leyenda del mapa (estilo Looker)
                st.markdown("### 📊 Escala de Datos")
                
                # Crear leyenda visual
                col1, col2, col3, col4 = st.columns([1, 1, 1, 2])
                
                with col1:
                    st.markdown(f"**{min_ingreso:,.2f}**")
                with col2:
                    st.markdown("🟠")
                with col3:
                    st.markdown("🔴")
                with col4:
                    st.markdown(f"**{max_ingreso:,.2f}**")
                
                st.markdown("""
                **📋 Información del Mapa:**
                - 🔴 **Círculos Rojos**: Ingresos por encima del promedio ({:,.2f})
                - 🟠 **Círculos Naranjas**: Ingresos por debajo del promedio
                - **Tamaño del círculo**: Proporcional al Ingreso_Total
                - **Datos**: Ciudad_Cliente vs Ingreso_Total
                """.format(mean_ingreso))
                
                # Mostrar tabla de datos
                st.markdown("### 📊 Datos por Ciudad del Cliente")
                df_ubicacion = ingresos_ubicacion.reset_index()
                df_ubicacion.columns = ['Ciudad del Cliente', 'Ingreso Total']
                df_ubicacion['Ingreso Total'] = df_ubicacion['Ingreso Total'].apply(lambda x: f"S/. {x:,.2f}")
                st.dataframe(df_ubicacion, use_container_width=True, hide_index=True)
                
                # Información adicional
                st.markdown("### 📋 Información Adicional")
                col1, col2 = st.columns(2)
                
                with col1:
                    if "Tipo_Tienda" in df_ventas.columns:
                        tipo_tienda_counts = df_ventas["Tipo_Tienda"].value_counts()
                        st.markdown("**Ventas por Tipo de Tienda:**")
                        for tipo, count in tipo_tienda_counts.items():
                            st.write(f"• {tipo}: {count} ventas")
                    
                    if "Categoria" in df_ventas.columns:
                        categoria_ingresos = df_ventas.groupby("Categoria")["Ingreso_Total"].sum().sort_values(ascending=False)
                        st.markdown("**Top Categorías por Ingreso:**")
                        for categoria, ingreso in categoria_ingresos.head(3).items():
                            st.write(f"• {categoria}: S/. {ingreso:,.2f}")
                
                with col2:
                    if "Pais" in df_ventas.columns:
                        pais_counts = df_ventas["Pais"].value_counts()
                        st.markdown("**Ventas por País:**")
                        for pais, count in pais_counts.items():
                            st.write(f"• {pais}: {count} ventas")
                    
                    if "Año" in df_ventas.columns:
                        año_ingresos = df_ventas.groupby("Año")["Ingreso_Total"].sum()
                        st.markdown("**Ingresos por Año:**")
                        for año, ingreso in año_ingresos.items():
                            st.write(f"• {año}: S/. {ingreso:,.2f}")
                
            else:
                st.info("⚠️ No existe columna 'Ciudad_Cliente' en la tabla analisis_ventas_bikegear_2025. Verifica la estructura de la tabla.")

        else:
            st.info("📭 No hay datos disponibles en la tabla analisis_ventas_bikegear_2025.")

    except Exception as e:
        st.error(f"❌ Error al cargar reportes: {e}")
        st.error(f"Detalles del error: {str(e)}")
