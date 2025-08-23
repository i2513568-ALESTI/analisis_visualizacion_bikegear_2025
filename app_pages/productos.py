import streamlit as st
import pandas as pd
from config.supabase_client import get_client

supabase = get_client()

def productos_page():
    st.header("Registro y Catálogo de Productos")

    st.subheader("Agregar Nuevo Producto")
    
    with st.form("registro_producto"):
        col1, col2 = st.columns(2)
        
        with col1:
            nombre = st.text_input("Nombre del producto")
            categoria = st.selectbox("Categoría", ["Bicicletas", "Accesorios", "Repuestos", "Ropa", "Herramientas"])
            precio = st.number_input("Precio unitario (S/.)", min_value=0.0, step=1.0, value=0.0)
        
        with col2:
            costo = st.number_input("Costo unitario (S/.)", min_value=0.0, step=1.0, value=0.0)
            stock = st.number_input("Stock disponible", min_value=0, step=1, value=0)
            
        submit = st.form_submit_button("Agregar Producto", use_container_width=True)

        if submit and nombre:
            try:
                supabase.table("productos").insert({
                    "nombre": nombre,
                    "categoria": categoria,
                    "precio": precio,
                    "costo": costo,
                    "stock": stock
                }).execute()
                st.success(f"Producto '{nombre}' agregado exitosamente")
                st.rerun()
            except Exception as e:
                st.error(f"Error al agregar producto: {e}")

    st.subheader("Catálogo de Productos")

    try:
        productos = supabase.table("productos").select("*").execute().data
        df = pd.DataFrame(productos)

        if not df.empty:
            df_display = df.copy()
            df_display['precio'] = df_display['precio'].apply(lambda x: f"S/. {x:,.2f}")
            df_display['costo'] = df_display['costo'].apply(lambda x: f"S/. {x:,.2f}")
            df_display['stock'] = df_display['stock'].apply(lambda x: f"{x} unidades")
            
            df_display = df_display.rename(columns={
                'id': 'ID',
                'nombre': 'Nombre del Producto',
                'categoria': 'Categoría',
                'precio': 'Precio',
                'costo': 'Costo',
                'stock': 'Stock Disponible'
            })
            
            st.dataframe(
                df_display,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "ID": st.column_config.NumberColumn("ID", width="small"),
                    "Nombre del Producto": st.column_config.TextColumn("Nombre del Producto", width="large"),
                    "Categoría": st.column_config.TextColumn("Categoría", width="medium"),
                    "Precio": st.column_config.TextColumn("Precio", width="medium"),
                    "Costo": st.column_config.TextColumn("Costo", width="medium"),
                    "Stock Disponible": st.column_config.TextColumn("Stock", width="medium")
                }
            )
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Productos", len(df))
            with col2:
                st.metric("Valor Total Inventario", f"S/. {df['precio'].sum():,.2f}")
            with col3:
                st.metric("Stock Total", f"{df['stock'].sum()} unidades")
            with col4:
                st.metric("Categorías", df['categoria'].nunique())
                
        else:
            st.info("No hay productos registrados aún. Agrega tu primer producto!")
            
    except Exception as e:
        st.error(f"Error al cargar productos: {e}")
