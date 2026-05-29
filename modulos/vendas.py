import streamlit as st
import pandas as pd

from database.db import query, execute

# ⚠️ mantenha só se o arquivo existir
from utils.pdf import gerar_pdf_vendas


def show_vendas():

    st.title("🛒 Vendas")

    produtos = query("""
        SELECT *
        FROM produtos
        WHERE tipo='Produto Final'
    """)

    if produtos.empty:
        st.warning("Sem produtos cadastrados")
        return

    produto = st.selectbox(
        "Produto",
        produtos["nome"]
    )

    info = produtos[
        produtos["nome"] == produto
    ].iloc[0]

    qtd = st.number_input(
        "Quantidade",
        min_value=1.0,
        step=1.0
    )

    total = qtd * info["venda"]

    st.info(f"Total: R$ {total:,.2f}")

    if st.button("✅ Finalizar Venda"):

        # ✅ CORRETO (sem HTML)
        if qtd > info["estoque"]:
            st.error("Estoque insuficiente")
            return

        novo_estoque = info["estoque"] - qtd

        lucro = total - (qtd * info["custo"])

        execute("""
            UPDATE produtos
            SET estoque=?
            WHERE id=?
        """, (
            novo_estoque,
            info["id"]
        ))

        execute("""
            INSERT INTO vendas(produto, quantidade, total, lucro)
            VALUES(?,?,?,?)
        """, (
            produto,
            qtd,
            total,
            lucro
        ))

        st.success("✅ Venda registrada")
        st.rerun()

    # =========================
    # HISTÓRICO
    # =========================

    st.divider()
    st.subheader("📋 Histórico de Vendas")

    df = query("""
        SELECT *
        FROM vendas
        ORDER BY id DESC
    """)

    if df.empty:
        st.info("Nenhuma venda registrada")
        return

    st.dataframe(df, use_container_width=True)

    # =========================
    # PDF
    # =========================

    if st.button("📄 Gerar PDF"):

        gerar_pdf_vendas(df)

        with open("relatorio_vendas.pdf", "rb") as file:
            st.download_button(
                label="⬇️ Baixar PDF",
                data=file,
                file_name="relatorio_vendas.pdf",
                mime="application/pdf"
            )
