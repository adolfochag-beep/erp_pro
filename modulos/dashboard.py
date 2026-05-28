import streamlit as st
import pandas as pd
import plotly.express as px

from database.db import query

st.set_page_config(layout="wide")

# =========================
# CACHE (PERFORMANCE)
# =========================

@st.cache_data
def load_data():
    vendas = query("SELECT * FROM vendas")
    produtos = query("SELECT * FROM produtos")
    financeiro = query("SELECT * FROM financeiro")
    return vendas, produtos, financeiro


def show_dashboard():

    st.title("📊 Dashboard Executivo")

    vendas, produtos, financeiro = load_data()

    # =========================
    # TRATAMENTO
    # =========================

    if not vendas.empty:
        vendas["total"] = pd.to_numeric(vendas["total"], errors="coerce")
        vendas["lucro"] = pd.to_numeric(vendas["lucro"], errors="coerce")

        if "data" in vendas.columns:
            vendas["data"] = pd.to_datetime(vendas["data"])

    if not financeiro.empty:
        financeiro["valor"] = pd.to_numeric(financeiro["valor"], errors="coerce")

        if "data" in financeiro.columns:
            financeiro["data"] = pd.to_datetime(financeiro["data"])

    # =========================
    # FILTROS
    # =========================

    st.sidebar.header("🔎 Filtros")

    # Produto
    if not vendas.empty:
        lista_produtos = vendas["produto"].dropna().unique()
        produto_sel = st.sidebar.selectbox("Produto", ["Todos"] + list(lista_produtos))
    else:
        produto_sel = "Todos"

    # Data
    data_ini, data_fim = None, None
    if not vendas.empty and "data" in vendas.columns:
        data_ini = st.sidebar.date_input("Data início")
        data_fim = st.sidebar.date_input("Data fim")

    # Tipo financeiro
    if not financeiro.empty:
        tipos = financeiro["tipo"].dropna().unique()
        tipo_sel = st.sidebar.multiselect("Tipo financeiro", tipos, default=tipos)
    else:
        tipo_sel = []

    # =========================
    # APLICAR FILTROS
    # =========================

    if produto_sel != "Todos":
        vendas = vendas[vendas["produto"] == produto_sel]

    if data_ini and data_fim:
        vendas = vendas[
            (vendas["data"] >= pd.to_datetime(data_ini)) &
            (vendas["data"] <= pd.to_datetime(data_fim))
        ]

    if not financeiro.empty and tipo_sel:
        financeiro = financeiro[financeiro["tipo"].isin(tipo_sel)]

    # =========================
    # KPIs
    # =========================

    faturamento = vendas["total"].sum() if not vendas.empty else 0
    lucro = vendas["lucro"].sum() if not vendas.empty else 0

    total_produtos = len(produtos) if not produtos.empty else 0

    estoque_baixo = len(
        produtos[
            produtos["estoque"] <= produtos["estoque_min"]
        ]
    ) if not produtos.empty else 0

    percentual_critico = (estoque_baixo / total_produtos * 100) if total_produtos > 0 else 0

    # =========================
    # CARDS
    # =========================

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("💰 Faturamento", f"R$ {faturamento:,.2f}")
    col2.metric("📈 Lucro", f"R$ {lucro:,.2f}")
    col3.metric("📦 Produtos", total_produtos)
    col4.metric("⚠️ Estoque Crítico", f"{estoque_baixo}", f"{percentual_critico:.1f}%")

    st.divider()

    # =========================
    # ABAS
    # =========================

    tab1, tab2, tab3 = st.tabs(["📊 Vendas", "💰 Financeiro", "📦 Estoque"])

    # =========================
    # VENDAS
    # =========================

    with tab1:

        st.subheader("Vendas por Produto")

        if not vendas.empty:
            grafico = vendas.groupby("produto")["total"].sum().reset_index()

            fig = px.bar(
                grafico,
                x="produto",
                y="total",
                text_auto=True,
                color="produto"
            )

            st.plotly_chart(fig, use_container_width=True)

        else:
            st.info("Sem vendas")

        # Evolução
        if not vendas.empty and "data" in vendas.columns:

            serie = vendas.groupby("data")["total"].sum().reset_index()

            st.subheader("📅 Evolução de Vendas")

            fig2 = px.line(
                serie,
                x="data",
                y="total"
            )

            st.plotly_chart(fig2, use_container_width=True)

    # =========================
    # FINANCEIRO
    # =========================

    with tab2:

        st.subheader("Resumo Financeiro")

        if not financeiro.empty:

            entradas = financeiro[financeiro["tipo"] == "Entrada"]["valor"].sum()
            saidas = financeiro[financeiro["tipo"] == "Saída"]["valor"].sum()
            saldo = entradas - saidas

            c1, c2, c3 = st.columns(3)

            c1.metric("Entradas", f"R$ {entradas:,.2f}")
            c2.metric("Saídas", f"R$ {saidas:,.2f}")
            c3.metric("Saldo", f"R$ {saldo:,.2f}")

            resumo = financeiro.groupby("tipo")["valor"].sum().reset_index()

            fig3 = px.bar(
                resumo,
                x="tipo",
                y="valor",
                text_auto=True,
                color="tipo"
            )

            st.plotly_chart(fig3, use_container_width=True)

        else:
            st.info("Sem dados financeiros")

    # =========================
    # ESTOQUE
    # =========================

    with tab3:

        st.subheader("Estoque Crítico")

        if not produtos.empty:

            criticos = produtos[
                produtos["estoque"] <= produtos["estoque_min"]
            ]

            if not criticos.empty:
                st.dataframe(criticos, use_container_width=True)
            else:
                st.success("Nenhum produto crítico")

        else:
            st.info("Sem dados de produtos")
