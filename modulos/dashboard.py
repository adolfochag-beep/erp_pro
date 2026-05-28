import streamlit as st
import pandas as pd

from database.db import query


def show_dashboard():

    st.title("📊 Dashboard Executivo")

    # =========================
    # DADOS
    # =========================

    vendas = query("""
    SELECT *
    FROM vendas
    """)

    produtos = query("""
    SELECT *
    FROM produtos
    """)

    financeiro = query("""
    SELECT *
    FROM financeiro
    """)

    # =========================
    # FILTROS
    # =========================

    st.sidebar.header("🔎 Filtros")

    # Filtro de produto
    if not vendas.empty:
        lista_produtos = vendas["produto"].dropna().unique()
        produto_sel = st.sidebar.selectbox(
            "Produto",
            ["Todos"] + list(lista_produtos)
        )
    else:
        produto_sel = "Todos"

    # Filtro financeiro
    if not financeiro.empty:
        tipos = financeiro["tipo"].dropna().unique()
        tipo_sel = st.sidebar.multiselect(
            "Tipo financeiro",
            tipos,
            default=tipos
        )
    else:
        tipo_sel = []

    # =========================
    # APLICAR FILTROS
    # =========================

    if produto_sel != "Todos":
        vendas = vendas[vendas["produto"] == produto_sel]

    if not financeiro.empty and tipo_sel:
        financeiro = financeiro[financeiro["tipo"].isin(tipo_sel)]

    # =========================
    # KPIs
    # =========================

    faturamento = 0
    lucro = 0
    total_produtos = 0
    estoque_baixo = 0

    if not vendas.empty:
        faturamento = vendas["total"].sum()
        lucro = vendas["lucro"].sum()

    if not produtos.empty:
        total_produtos = len(produtos)
        estoque_baixo = len(
            produtos[
                produtos["estoque"]
                <=
                produtos["estoque_min"]
            ]
        )

    # =========================
    # CARDS
    # =========================

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "💰 Faturamento",
            f"R$ {faturamento:,.2f}"
        )

    with col2:
        st.metric(
            "📈 Lucro",
            f"R$ {lucro:,.2f}"
        )

    with col3:
        st.metric(
            "📦 Produtos",
            total_produtos
        )

    with col4:
        st.metric(
            "⚠️ Estoque Baixo",
            estoque_baixo
        )

    st.divider()

    # =========================
    # GRÁFICO VENDAS
    # =========================

    st.subheader("📈 Vendas por Produto")

    if not vendas.empty:
        grafico = (
            vendas
            .groupby("produto")["total"]
            .sum()
            .reset_index()
        )

        st.bar_chart(
            grafico,
            x="produto",
            y="total",
            use_container_width=True
        )
    else:
        st.info("Sem vendas registradas")

    # =========================
    # ESTOQUE CRÍTICO
    # =========================

    st.divider()

    st.subheader("⚠️ Estoque Crítico")

    if not produtos.empty:

        criticos = produtos[
            produtos["estoque"]
            <=
            produtos["estoque_min"]
        ]

        if not criticos.empty:
            st.dataframe(
                criticos,
                use_container_width=True
            )
        else:
            st.success("Nenhum produto crítico")

    # =========================
    # FINANCEIRO
    # =========================

    st.divider()

    st.subheader("💰 Resumo Financeiro")

    if not financeiro.empty:

        entradas = financeiro[
            financeiro["tipo"] == "Entrada"
        ]["valor"].sum()

        saidas = financeiro[
            financeiro["tipo"] == "Saída"
        ]["valor"].sum()

        saldo = entradas - saidas

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric(
                "Entradas",
                f"R$ {entradas:,.2f}"
            )

        with c2:
            st.metric(
                "Saídas",
                f"R$ {saidas:,.2f}"
            )

        with c3:
            st.metric(
                "Saldo",
                f"R$ {saldo:,.2f}"
            )

    else:
        st.info("Sem movimentações financeiras")
