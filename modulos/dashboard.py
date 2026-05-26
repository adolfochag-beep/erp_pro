import streamlit as st
import pandas as pd
import plotly.express as px

from database.db import query

from utils.grid import tabela

def show_dashboard():

    st.title("📊 Dashboard Executivo")

    vendas = query(
        "SELECT * FROM vendas"
    )

    produtos = query(
        "SELECT * FROM produtos"
    )

    faturamento = (
        vendas["total"].sum()
        if not vendas.empty
        else 0
    )

    lucro = (
        vendas["lucro"].sum()
        if not vendas.empty
        else 0
    )

    qtd_vendas = len(vendas)

    ticket = (
        faturamento / qtd_vendas
        if qtd_vendas > 0
        else 0
    )

    estoque_baixo = produtos[
        produtos["estoque"] <= produtos["estoque_min"]
    ]

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "💰 Faturamento",
        f"R$ {faturamento:,.2f}"
    )

    c2.metric(
        "📈 Lucro",
        f"R$ {lucro:,.2f}"
    )

    c3.metric(
        "🧾 Ticket Médio",
        f"R$ {ticket:,.2f}"
    )

    c4.metric(
        "⚠️ Estoque Baixo",
        len(estoque_baixo)
    )

    st.divider()

    if not vendas.empty:

        vendas["data"] = pd.to_datetime(
            vendas["data"]
        )

        grafico = vendas.groupby(
            vendas["data"].dt.date
        )["total"].sum().reset_index()

        fig = px.line(
            grafico,
            x="data",
            y="total",
            title="Vendas por Dia"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    if not estoque_baixo.empty:

        st.warning(
            "Produtos com estoque baixo"
        )

        tabela(estoque_baixo)