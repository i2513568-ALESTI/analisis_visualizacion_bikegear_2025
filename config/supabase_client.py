import streamlit as st
from supabase import create_client, Client

# Inicializar cliente Supabase
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]

def get_client() -> Client:
    return create_client(url, key)
