import streamlit as st
import pandas as pd
import plotly.express as px

from database.db import query


def show_dashboard():

    st.title("📊 Dashboard Executivo")

    # =========================
    # DADOS
    # =========================

    vendas = query("SELECT * FROM vendas")
    produtos = query("SELECT * FROM produtos")
    financeiro = query("SELECT * FROM financeiro")

    # =========================
    # TRATAMENTO
    # =========================

    if not vendas.empty:
        vendas["total"] = pd.to_numeric(vendas["total"], errors="coerce")
        vendas["lucro"] = pd.to_numeric(vendas["lucro"], errors="coerce")

    if not produtos.empty:
        produtos["estoque"] = pd.to_numeric(produtos["estoque"], errors="coerce")
        produtos["estoque_min"] = pd.to_numeric(produtos["estoque_min"], errors="coerce")

    if not financeiro.empty:
        financeiro["valor"] = pd.to_numeric(financeiro["valor"], errors="coerce")

    # =========================
    # KPIs
    # =========================

    faturamento = vendas["total"].sum() if not vendas.empty else 0
    lucro = vendas["lucro"].sum() if not vendas.empty else 0

    total_produtos = len(produtos) if not produtos.empty else 0

    estoque_baixo = len(
        produtos[produtos["estoque"] <= produtos["estoque_min"]]
    ) if not produtos.empty else 0

    percentual_critico = (
        (estoque_baixo / total_produtos) * 100
        if total_produtos > 0 else 0
    )

    # =========================
    # CARDS
    # =========================

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("💰 Faturamento", f"R$ {faturamento:,.2f}")
    c2.metric("📈 Lucro", f"R$ {lucro:,.2f}")
    c3.metric("📦 Produtos", total_produtos)
    c4.metric("⚠️ Estoque Crítico", f"{estoque_baixo}", f"{percentual_critico:.1f}%")

    st.divider()

    # =========================
    # GRÁFICO VENDAS
    # =========================

    st.subheader("📈 Vendas por Produto")

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
        st.info("Sem vendas registradas")

    # =========================
    # TABELA ESTOQUE PREMIUM
    # =========================

    st.divider()

    st.markdown("### ⚠️ Estoque Crítico")

    if not produtos.empty:

        criticos = produtos[
            produtos["estoque"] <= produtos["estoque_min"]
        ].copy()

        if not criticos.empty:

            # STATUS VISUAL
            criticos["Status"] = criticos.apply(
                lambda x: "🔴 Crítico" if x["estoque"] == 0
                else "🟠 Baixo",
                axis=1
            )

            # ORDENAÇÃO
            criticos = criticos.sort_values(by="estoque")

            # FORMATAÇÃO VISUAL
            def highlight(row):
                if row["estoque"] == 0:
                    return ['background-color: #ff4d4f; color: white'] * len(row)
                elif row["estoque"] <= row["estoque_min"]:
                    return ['background-color: #fff3cd'] * len(row)
                return [''] * len(row)

            styled = criticos.style.apply(highlight, axis=1)

            st.dataframe(
                styled,
                use_container_width=True,
                height=380
            )

        else:
            st.success("✅ Nenhum produto crítico")

    # =========================
    # FINANCEIRO
    # =========================

    st.divider()

    st.subheader("💰 Resumo Financeiro")

    if not financeiro.empty:

        entradas = financeiro[financeiro["tipo"] == "Entrada"]["valor"].sum()
        saidas = financeiro[financeiro["tipo"] == "Saída"]["valor"].sum()
        saldo = entradas - saidas

        f1, f2, f3 = st.columns(3)

        f1.metric("Entradas", f"R$ {entradas:,.2f}")
        f2.metric("Saídas", f"R$ {saidas:,.2f}")
        f3.metric("Saldo", f"R$ {saldo:,.2f}")

        resumo = financeiro.groupby("tipo")["valor"].sum().reset_index()

        fig2 = px.bar(
            resumo,
            x="tipo",
            y="valor",
            text_auto=True,
            color="tipo"
        )

        st.plotly_chart(fig2, use_container_width=True)

    else:
        st.info("Sem movimentações financeiras")
