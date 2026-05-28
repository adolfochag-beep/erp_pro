import streamlit as st
import pandas as pd
from database.db import query


def show_compras():

    st.title("⚠️ Lista de Compras Inteligente")

    df = query("""
    SELECT *,
        (estoque_min - estoque) AS comprar,
        COALESCE(custo, 0) * (estoque_min - estoque) AS custo_total
    FROM produtos
    WHERE estoque <= estoque_min
    """)

    if df.empty:
        st.success("✅ Estoque OK — nenhum item precisa de reposição")
        return

    # =========================
    # TRATAMENTO
    # =========================

    df["comprar"] = df["comprar"].clip(lower=0)
    df = df.sort_values(by="estoque")  # mais crítico primeiro

    # =========================
    # KPIs
    # =========================

    total_itens = len(df)
    custo_total = df["custo_total"].sum()

    c1, c2 = st.columns(2)

    c1.metric("Itens para comprar", total_itens)
    c2.metric("💰 Custo estimado", f"R$ {custo_total:,.2f}")

    st.divider()

    # =========================
    # FILTRO
    # =========================

    filtro_tipo = st.selectbox(
        "Filtrar por tipo",
        ["Todos"] + list(df["tipo"].dropna().unique())
    )

    if filtro_tipo != "Todos":
        df = df[df["tipo"] == filtro_tipo]

    # =========================
    # HIGHLIGHT
    # =========================

    def destaque(row):
        if row["estoque"] == 0:
            return ['background-color: #ff4d4f; color: white'] * len(row)
        return ['background-color: #fff3cd'] * len(row)

    # formatação monetária segura
    df["custo_total"] = pd.to_numeric(df["custo_total"], errors="coerce").fillna(0)
    df["custo_total"] = df["custo_total"].apply(lambda x: f"R$ {x:,.2f}")

    # =========================
    # TABELA PROFISSIONAL
    # =========================

    st.subheader("📋 Itens a Comprar")

    st.dataframe(
        df.style.apply(destaque, axis=1),
        use_container_width=True,
        height=400
    )

    # =========================
    # RESUMO GERENCIAL
    # =========================

    st.divider()

    st.subheader("📊 Resumo")

    resumo = df.groupby("tipo")["custo_total"].count().reset_index()
    resumo.columns = ["Tipo", "Qtd Itens"]

    st.dataframe(resumo, use_container_width=True)
``
