import streamlit as st
import pandas as pd
from config.supabase_client import get_client

supabase = get_client()

def ventas_page():
    st.header("Registrar Venta")

    try:
        productos = supabase.table("productos").select("*").execute().data
        df = pd.DataFrame(productos)

        if not df.empty:
            st.subheader("Nueva Venta")
            
            with st.form("registro_venta"):
                col1, col2 = st.columns(2)
                
                with col1:
                    producto_sel = st.selectbox(
                        "Selecciona producto", 
                        df["nombre"]
                    )
                    cantidad = st.number_input(
                        "Cantidad", 
                        min_value=1, 
                        step=1, 
                        value=1
                    )
                
                with col2:
                    if producto_sel:
                        prod = df.loc[df["nombre"] == producto_sel].iloc[0]
                        st.markdown("### Información del Producto")
                        st.markdown(f"**Precio:** S/. {prod['precio']:,.2f}")
                        st.markdown(f"**Stock disponible:** {prod['stock']} unidades")
                        st.markdown(f"**Categoría:** {prod['categoria']}")
                        
                        ingreso_total = cantidad * prod['precio']
                        ganancia_total = cantidad * (prod['precio'] - prod['costo'])
                        
                        st.markdown("### Totales")
                        st.markdown(f"**Ingreso:** S/. {ingreso_total:,.2f}")
                        st.markdown(f"**Ganancia:** S/. {ganancia_total:,.2f}")
                
                submit = st.form_submit_button("Registrar Venta", use_container_width=True)

                if submit:
                    prod = df.loc[df["nombre"] == producto_sel].iloc[0]

                    if cantidad <= prod["stock"]:
                        ingreso = cantidad * prod["precio"]
                        ganancia = cantidad * (prod["precio"] - prod["costo"])

                        try:
                            supabase.table("ventas").insert({
                                "producto_id": int(prod["id"]),
                                "cantidad": int(cantidad),
                                "ingreso": float(ingreso),
                                "ganancia": float(ganancia)
                            }).execute()

                            supabase.table("productos").update(
                                {"stock": int(prod["stock"]) - int(cantidad)}
                            ).eq("id", int(prod["id"])).execute()

                            st.success(f"Venta registrada exitosamente: {cantidad} x {prod['nombre']}")
                            st.success(f"Ingreso: S/. {ingreso:,.2f} | Ganancia: S/. {ganancia:,.2f}")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error al registrar venta: {e}")
                    else:
                        st.warning(f"Stock insuficiente. Disponible: {prod['stock']} unidades")

            st.subheader("Productos Disponibles")

            df_con_stock = df[df['stock'] > 0].copy()
            
            if not df_con_stock.empty:
                df_display = df_con_stock.copy()
                df_display['precio'] = df_display['precio'].apply(lambda x: f"S/. {x:,.2f}")
                df_display['stock'] = df_display['stock'].apply(lambda x: f"{x} unidades")
                
                df_display = df_display.rename(columns={
                    'id': 'ID',
                    'nombre': 'Nombre del Producto',
                    'categoria': 'Categoría',
                    'precio': 'Precio',
                    'stock': 'Stock Disponible'
                })
                
                st.dataframe(
                    df_display[['Nombre del Producto', 'Categoría', 'Precio', 'Stock Disponible']],
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "Nombre del Producto": st.column_config.TextColumn("Producto", width="large"),
                        "Categoría": st.column_config.SelectboxColumn("Categoría", width="medium"),
                        "Precio": st.column_config.TextColumn("Precio", width="medium"),
                        "Stock Disponible": st.column_config.TextColumn("Stock", width="medium")
                    }
                )
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Productos con Stock", len(df_con_stock))
                with col2:
                    st.metric("Stock Total Disponible", f"{df_con_stock['stock'].sum()} unidades")
                with col3:
                    st.metric("Valor Total", f"S/. {df_con_stock['precio'].sum():,.2f}")
            else:
                st.warning("No hay productos con stock disponible para vender")
                
        else:
            st.info("No hay productos disponibles. Agrega productos primero!")
            
    except Exception as e:
        st.error(f"Error al cargar productos: {e}")
