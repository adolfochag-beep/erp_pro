import streamlit as st
from database.db import query

def show_compras():

    st.title("⚠️ Lista de Compras")

    df = query("""
    SELECT *,
    (estoque_min - estoque) AS comprar
    FROM produtos
    WHERE estoque <= estoque_min
    """)

    if df.empty:
        st.success("Estoque OK")
    else:
        st.warning("Itens para reposição")
        st.dataframe(df, use_container_width=True)