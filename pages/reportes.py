# reportes.py
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from config.supabase_client import get_client
from utils.helpers import to_python_type

supabase = get_client()

def reportes_page():
    st.header("Dashboard de Reportes")

    try:
        ventas = supabase.table("ventas").select("*").execute().data
        productos = supabase.table("productos").select("*").execute().data

        if ventas and productos:
            df_ventas = pd.DataFrame(ventas)
            df_productos = pd.DataFrame(productos)
            
            df_ventas["ingreso"] = df_ventas["ingreso"].apply(to_python_type)
            df_ventas["ganancia"] = df_ventas["ganancia"].apply(to_python_type)
            
            df_ventas = df_ventas.merge(
                df_productos[['id', 'nombre', 'categoria']], 
                left_on='producto_id', 
                right_on='id', 
                suffixes=('', '_producto')
            )
            
            df_ventas['fecha'] = pd.date_range(
                start=datetime(2024, 1, 1),
                periods=len(df_ventas),
                freq='D'
            )

            st.markdown("### Métricas Principales")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "INGRESO TOTAL", 
                    f"S/. {df_ventas['ingreso'].sum():,.2f}"
                )
            
            with col2:
                st.metric(
                    "GANANCIAS", 
                    f"S/. {df_ventas['ganancia'].sum():,.2f}"
                )
            
            with col3:
                ticket_promedio = df_ventas['ingreso'].mean() if len(df_ventas) > 0 else 0
                st.metric(
                    "TICKET PROMEDIO", 
                    f"S/. {ticket_promedio:,.2f}"
                )
            
            with col4:
                st.metric(
                    "NUMERO DE VENTAS", 
                    f"{len(df_ventas)}"
                )

            st.markdown("---")

            st.markdown("### Detalle de Ventas")
            
            df_display = df_ventas.copy()
            df_display['ingreso'] = df_display['ingreso'].apply(lambda x: f"S/. {x:,.2f}")
            df_display['ganancia'] = df_display['ganancia'].apply(lambda x: f"S/. {x:,.2f}")
            df_display['fecha'] = df_display['fecha'].dt.strftime('%d/%m/%Y')
            
            df_display = df_display.rename(columns={
                'id': 'ID Venta',
                'producto_id': 'ID Producto',
                'nombre': 'Producto',
                'categoria': 'Categoría',
                'cantidad': 'Cantidad',
                'ingreso': 'Ingreso',
                'ganancia': 'Ganancia',
                'fecha': 'Fecha'
            })
            
            st.dataframe(
                df_display[['ID Venta', 'Producto', 'Categoría', 'Cantidad', 'Ingreso', 'Ganancia', 'Fecha']],
                use_container_width=True,
                hide_index=True,
                column_config={
                    "ID Venta": st.column_config.NumberColumn("ID", width="small"),
                    "Producto": st.column_config.TextColumn("Producto", width="large"),
                    "Categoría": st.column_config.SelectboxColumn("Categoría", width="medium"),
                    "Cantidad": st.column_config.NumberColumn("Cantidad", width="small"),
                    "Ingreso": st.column_config.TextColumn("Ingreso", width="medium"),
                    "Ganancia": st.column_config.TextColumn("Ganancia", width="medium"),
                    "Fecha": st.column_config.TextColumn("Fecha", width="medium")
                }
            )

        else:
            st.info("Aún no se han registrado ventas. Comienza a vender para ver los reportes!")
            
    except Exception as e:
        st.error(f"Error al cargar reportes: {e}")
