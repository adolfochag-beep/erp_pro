import streamlit as st
import pandas as pd
from database.db import query


def show_compras():

    st.title("⚠️ Lista de Compras")

    sql = """
        SELECT
            nome,
            tipo,
            unidade,
            estoque,
            estoque_min,
            (estoque_min - estoque) AS comprar
        FROM produtos
        WHERE estoque <= estoque_min
    """

    df = query(sql)

    if df is None or df.empty:
        st.success("✅ Estoque OK. Nenhum item precisa de reposicao.")
        return

    df["comprar"] = df["comprar"].clip(lower=0)

    st.warning("Itens que precisam de reposicao")

    def destaque(row):
        if row["estoque"] == 0:
            return ["background-color: #fee2e2"] * len(row)
        return ["background-color: #fff7ed"] * len(row)

    st.dataframe(
        df.style.apply(destaque, axis=1),
        use_container_width=True,
        height=400
    )
