import streamlit as st
import pandas as pd
from config.supabase_client import get_client

supabase = get_client()

def ventas_page():
    st.header("🛒 Registrar Venta")

    # --- Inicializar estados ---
    if "voucher" not in st.session_state:
        st.session_state.voucher = None
    if "refresh" not in st.session_state:
        st.session_state.refresh = False

    try:
        productos = supabase.table("productos").select("*").execute().data
        df = pd.DataFrame(productos)

        if not df.empty:
            st.subheader("Nueva Venta")

            # --- Selección de producto ---
            col1, col2 = st.columns(2)

            with col1:
                producto_sel = st.selectbox(
                    "Selecciona producto",
                    df["nombre"],
                    index=None,
                    placeholder="Elige un producto..."
                )
                cantidad = st.number_input(
                    "Cantidad",
                    min_value=1,
                    step=1,
                    value=1,
                    format="%d"
                )

            with col2:
                if producto_sel:
                    prod = df.loc[df["nombre"] == producto_sel].iloc[0]
                    st.markdown("### 📦 Información del Producto")
                    st.markdown(f"**Precio Unitario:** S/. {prod['precio']:,.2f}")
                    st.markdown(f"**Costo Unitario:** S/. {prod['costo']:,.2f}")
                    st.markdown(f"**Stock Disponible:** {prod['stock']} unidades")
                    st.markdown(f"**Categoría:** {prod['categoria']}")

                    ingreso_total = cantidad * prod['precio']
                    ganancia_total = cantidad * (prod['precio'] - prod['costo'])

                    st.markdown("### 💰 Totales")
                    st.markdown(f"**Pago Total (Ingreso):** S/. {ingreso_total:,.2f}")
                    st.markdown(f"**Ganancia Estimada:** S/. {ganancia_total:,.2f}")

            # --- Botón para registrar venta ---
            if st.button("💾 Registrar Venta", use_container_width=True):
                if producto_sel:
                    prod = df.loc[df["nombre"] == producto_sel].iloc[0]

                    if cantidad <= prod["stock"]:
                        ingreso = cantidad * prod["precio"]
                        ganancia = cantidad * (prod["precio"] - prod["costo"])

                        try:
                            # Insertar venta
                            supabase.table("ventas").insert({
                                "producto_id": int(prod["id"]),
                                "cantidad": int(cantidad),
                                "ingreso": float(ingreso),
                                "ganancia": float(ganancia)
                            }).execute()

                            # Actualizar stock
                            supabase.table("productos").update(
                                {"stock": int(prod["stock"]) - int(cantidad)}
                            ).eq("id", int(prod["id"])).execute()

                            # Guardar voucher en sesión
                            st.session_state.voucher = {
                                "producto": prod["nombre"],
                                "cantidad": cantidad,
                                "precio": prod["precio"],
                                "total": ingreso,
                                "ganancia": ganancia
                            }

                            st.session_state.refresh = True  # marcar refresh
                            st.rerun()

                        except Exception as e:
                            st.error(f"❌ Error al registrar venta: {e}")
                    else:
                        st.warning(f"⚠️ Stock insuficiente. Disponible: {prod['stock']} unidades")

            # --- Mostrar Voucher tipo "alert" ---
            if st.session_state.voucher:
                v = st.session_state.voucher
                with st.container(border=True):
                    st.success("✅ Venta registrada exitosamente")
                    st.markdown(
                        f"""
                        ### 🧾 Detalle de la Venta  
                        - Producto: **{v['producto']}**  
                        - Cantidad: **{v['cantidad']}**  
                        - Precio Unitario: **S/. {v['precio']:,.2f}**  
                        - Total Pagado: **S/. {v['total']:,.2f}**  
                        - Ganancia: **S/. {v['ganancia']:,.2f}**
                        """
                    )
                    if st.button("❌ Cerrar voucher"):
                        st.session_state.voucher = None

            # --- Tabla de productos disponibles ---
            st.subheader("📋 Productos Disponibles")

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
                    hide_index=True
                )

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Productos con Stock", len(df_con_stock))
                with col2:
                    st.metric("Stock Total Disponible", f"{df_con_stock['stock'].sum()} unidades")
                with col3:
                    st.metric("Valor Total", f"S/. {df_con_stock['precio'].sum():,.2f}")
            else:
                st.warning("📦 No hay productos con stock disponible para vender")

        else:
            st.info("📭 No hay productos disponibles. Agrega productos primero!")

    except Exception as e:
        st.error(f"❌ Error al cargar productos: {e}")
