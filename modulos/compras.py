import streamlit as st
import pandas as pd
from database.db import query


def show_compras():

    st.title("⚠️ Lista de Compras")

    try:

        df = query("""
        SELECT *,
            (estoque_min - estoque) AS comprar
        FROM produtos
        WHERE estoque <= estoque_min
        """)

    except Exception as e:
        st.error("Erro ao consultar dados")
        st.write(e)
        return

    if df is None or df.empty:
        st.success("✅ Estoque OK")
        return

    # tratamento
    df["comprar"] = df["comprar"].clip(lower=0)

    # ordena mais crítico primeiro
    df = df.sort_values(by="estoque")

    # KPI
    total_itens = len(df)
    st.metric("Itens críticos", total_itens)

    st.warning("Produtos que precisam reposição")

    # destaque
    def highlight(row):
        if row["estoque"] == 0:
            return ['background-color: red; color: white'] * len(row)
        return ['background-color: #fff3cd'] * len(row)

    st.dataframe(
        df.style.apply(highlight, axis=1),
        use_container_width=True,
        height=400
    )
