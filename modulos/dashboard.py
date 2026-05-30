import streamlit as st
import pandas as pd
import plotly.express as px

from database.db import query

def show_dashboard():

```
st.title("📊 Dashboard Executivo")

vendas = query("SELECT * FROM vendas")
produtos = query("SELECT * FROM produtos")
financeiro = query("SELECT * FROM financeiro")
receitas = query("SELECT * FROM receitas")
producoes = query("SELECT * FROM producoes")

# =========================
# TRATAMENTO
# =========================

if not vendas.empty:

    vendas["total"] = pd.to_numeric(
        vendas["total"],
        errors="coerce"
    )

    vendas["lucro"] = pd.to_numeric(
        vendas["lucro"],
        errors="coerce"
    )

    vendas["quantidade"] = pd.to_numeric(
        vendas["quantidade"],
        errors="coerce"
    )

    vendas["data"] = pd.to_datetime(
        vendas["data"],
        errors="coerce"
    )

    if "status" in vendas.columns:
        vendas = vendas[
            vendas["status"] != "Estornada"
        ]

if not produtos.empty:

    produtos["estoque"] = pd.to_numeric(
        produtos["estoque"],
        errors="coerce"
    )

    produtos["estoque_min"] = pd.to_numeric(
        produtos["estoque_min"],
        errors="coerce"
    )

    produtos["custo"] = pd.to_numeric(
        produtos["custo"],
        errors="coerce"
    )

if not financeiro.empty:

    financeiro["valor"] = pd.to_numeric(
        financeiro["valor"],
        errors="coerce"
    )

# =========================
# INDICADORES
# =========================

faturamento = (
    vendas["total"].sum()
    if not vendas.empty else 0
)

lucro = (
    vendas["lucro"].sum()
    if not vendas.empty else 0
)

total_produtos = (
    len(produtos)
    if not produtos.empty else 0
)

estoque_baixo = len(
    produtos[
        produtos["estoque"]
        <= produtos["estoque_min"]
    ]
) if not produtos.empty else 0

percentual_critico = (
    (estoque_baixo / total_produtos) * 100
    if total_produtos > 0 else 0
)

entradas = (
    financeiro[
        financeiro["tipo"] == "Entrada"
    ]["valor"].sum()
    if not financeiro.empty else 0
)

saidas = (
    financeiro[
        financeiro["tipo"] == "Saída"
    ]["valor"].sum()
    if not financeiro.empty else 0
)

saldo = entradas - saidas

valor_estoque = (
    (
        produtos["estoque"]
        * produtos["custo"]
    ).sum()
    if not produtos.empty else 0
)

margem = (
    (lucro / faturamento) * 100
    if faturamento > 0 else 0
)

# =========================
# CARDS PRINCIPAIS
# =========================

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
    "💵 Caixa",
    f"R$ {saldo:,.2f}"
)

c4.metric(
    "📦 Valor Estoque",
    f"R$ {valor_estoque:,.2f}"
)

c5, c6, c7, c8 = st.columns(4)

c5.metric(
    "📦 Produtos",
    total_produtos
)

c6.metric(
    "⚠️ Estoque Crítico",
    estoque_baixo,
    f"{percentual_critico:.1f}%"
)

c7.metric(
    "📈 Margem",
    f"{margem:.1f}%"
)

itens_comprar = estoque_baixo

c8.metric(
    "🛒 Comprar",
    itens_comprar
)

# =========================
# VENDAS POR PRODUTO
# =========================

st.divider()

st.subheader("📈 Vendas por Produto")

if not vendas.empty:

    grafico = (
        vendas.groupby("produto")["total"]
        .sum()
        .reset_index()
        .sort_values(
            by="total",
            ascending=False
        )
    )

    fig = px.bar(
        grafico,
        x="produto",
        y="total",
        text_auto=True,
        color="produto"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

else:

    st.info("Sem vendas registradas")

# =========================
# FORMAS DE PAGAMENTO
# =========================

st.divider()

st.subheader("💳 Vendas por Forma de Pagamento")

if (
    not vendas.empty
    and "forma_pagamento" in vendas.columns
):

    forma = (
        vendas.groupby("forma_pagamento")["total"]
        .sum()
        .reset_index()
    )

    fig_fp = px.pie(
        forma,
        names="forma_pagamento",
        values="total"
    )

    st.plotly_chart(
        fig_fp,
        use_container_width=True
    )

# =========================
# TOP PRODUTOS
# =========================

st.divider()

st.subheader("🏆 Produtos Mais Vendidos")

if not vendas.empty:

    top = (
        vendas.groupby("produto")["quantidade"]
        .sum()
        .reset_index()
        .sort_values(
            by="quantidade",
            ascending=False
        )
        .head(10)
    )

    st.dataframe(
        top,
        use_container_width=True
    )

# =========================
# ÚLTIMAS VENDAS
# =========================

st.divider()

st.subheader("🛒 Últimas Vendas")

if not vendas.empty:

    ultimas = vendas.sort_values(
        by="data",
        ascending=False
    ).head(10)

    st.dataframe(
        ultimas[
            [
                "data",
                "produto",
                "quantidade",
                "total",
                "cliente"
            ]
        ],
        use_container_width=True
    )

# =========================
# ESTOQUE CRÍTICO
# =========================

st.divider()

st.subheader("⚠️ Estoque Crítico")

if not produtos.empty:

    criticos = produtos[
        produtos["estoque"]
        <= produtos["estoque_min"]
    ]

    if criticos.empty:

        st.success(
            "✅ Nenhum produto crítico"
        )

    else:

        st.dataframe(
            criticos[
                [
                    "nome",
                    "estoque",
                    "estoque_min"
                ]
            ],
            use_container_width=True
        )

# =========================
# PRODUTOS SEM RECEITA
# =========================

st.divider()

st.subheader(
    "📚 Produtos sem Receita"
)

if (
    not produtos.empty
    and not receitas.empty
):

    finais = produtos[
        produtos["tipo"]
        == "Produto Final"
    ]

    usados = receitas[
        "produto_final"
    ].unique()

    sem_receita = finais[
        ~finais["id"].isin(usados)
    ]

    if sem_receita.empty:

        st.success(
            "✅ Todos possuem receita"
        )

    else:

        st.dataframe(
            sem_receita[
                ["nome"]
            ],
            use_container_width=True
        )

# =========================
# PRODUÇÕES
# =========================

st.divider()

st.subheader("🏭 Produções")

if not producoes.empty:

    st.metric(
        "Total Produções",
        len(producoes)
    )

    st.dataframe(
        producoes.tail(10),
        use_container_width=True
    )

# =========================
# FINANCEIRO
# =========================

st.divider()

st.subheader("💰 Resumo Financeiro")

f1, f2, f3 = st.columns(3)

f1.metric(
    "Entradas",
    f"R$ {entradas:,.2f}"
)

f2.metric(
    "Saídas",
    f"R$ {saidas:,.2f}"
)

f3.metric(
    "Saldo",
    f"R$ {saldo:,.2f}"
)

if not financeiro.empty:

    resumo = (
        financeiro.groupby("tipo")["valor"]
        .sum()
        .reset_index()
    )

    fig2 = px.bar(
        resumo,
        x="tipo",
        y="valor",
        text_auto=True,
        color="tipo"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

