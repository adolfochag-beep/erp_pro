import streamlit as st
import pandas as pd
from database.db import query


def show_compras():

    st.title("⚠️ Lista de Compras")

    df = query("""
    SELECT *,
        (estoque_min - estoque) AS comprar,
        (estoque_min - estoque) * custo AS custo_total
    FROM produtos
    WHERE estoque <= estoque_min
    """)

    if df.empty:

        st.success("✅ Estoque OK")
        return

    # =========================
    # TRATAMENTO
    # =========================

    df["comprar"] = df["comprar"].clip(lower=0)

    # prioridade (mais crítico primeiro)
    df = df.sort_values(by="estoque")

    # =========================
    # KPI (VALOR TOTAL)
    # =========================

    total_compra = df["custo_total"].sum()

    st.metric(
        "💰 Custo estimado de reposição",
        f"R$ {total_compra:,.2f}"
    )

    st.warning("Itens para reposição")

    # =========================
    # DESTACAR CRÍTICO
    # =========================

    def highlight(row):
        if row["estoque"] == 0:
            return ['background-color: #ff4d4f; color: white'] * len(row)
        return ['background-color: #fff3cd'] * len(row)

    # formatação dinheiro
    df["custo_total"] = df["custo_total"].apply(lambda x: f"R$ {x:,.2f}")

    # =========================
    # TABELA MELHORADA
    # =========================

    st.dataframe(
        df.style.apply(highlight, axis=1),
        use_container_width=True,
        height=400
    )
``
