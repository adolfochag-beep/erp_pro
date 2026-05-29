import streamlit as st
import pandas as pd

from utils.pdf import gerar_pdf_vendas
from database.db import query, execute


def show_vendas():

    st.title("🛒 Vendas")

    # =========================
    # NOVA VENDA
    # =========================

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

    info = produtos[produtos["nome"] == produto].iloc[0]

    qtd = st.number_input(
        "Quantidade",
        min_value=1.0,
        step=1.0
    )

    total = qtd * info["venda"]

    st.info(f"Total: R$ {total:,.2f}")

    if st.button("✅ Finalizar Venda"):

        if qtd > info["estoque"]:
            st.error("Estoque insuficiente")
            return

        novo_estoque = info["estoque"] - qtd
        lucro = total - (qtd * info["custo"])

        execute("""
            UPDATE produtos
            SET estoque=?
            WHERE id=?
        """, (novo_estoque, info["id"]))

        execute("""
            INSERT INTO vendas(produto, quantidade, total, lucro)
            VALUES(?,?,?,?)
        """, (produto, qtd, total, lucro))

        st.success("Venda registrada")
        st.rerun()

    # =========================
    # HISTÓRICO DE VENDAS
    # =========================

    st.divider()
    st.subheader("📋 Histórico de Vendas")

    vendas = query("""
        SELECT rowid as id, *
        FROM vendas
        ORDER BY rowid DESC
    """)

    if vendas.empty:
        st.info("Nenhuma venda registrada")
        return

    st.dataframe(vendas, use_container_width=True)

    # =========================
    # EDITAR VENDA
    # =========================

    st.divider()
    st.subheader("✏️ Editar Venda")

    venda_id = st.selectbox(
        "Selecione a venda",
        vendas["id"]
    )

    venda = vendas[vendas["id"] == venda_id].iloc[0]

    prod_edit = st.selectbox(
        "Produto",
        produtos["nome"],
        index=list(produtos["nome"]).index(venda["produto"])
    )

    qtd_nova = st.number_input(
        "Nova quantidade",
        min_value=1.0,
        value=float(venda["quantidade"]),
        step=1.0
    )

    info_prod = produtos[produtos["nome"] == prod_edit].iloc[0]

    total_novo = qtd_nova * info_prod["venda"]
    lucro_novo = total_novo - (qtd_nova * info_prod["custo"])

    st.info(f"Novo total: R$ {total_novo:,.2f}")

    if st.button("💾 Salvar Alteração"):

        # 1️⃣ DEVOLVE ESTOQUE ANTIGO
        execute("""
            UPDATE produtos
            SET estoque = estoque + ?
            WHERE nome=?
        """, (venda["quantidade"], venda["produto"]))

        # 2️⃣ VERIFICA ESTOQUE NOVO
        estoque_atual = query(
            "SELECT estoque FROM produtos WHERE nome=?",
            (prod_edit,)
        ).iloc[0]["estoque"]

        if qtd_nova > estoque_atual:
            st.error("Estoque insuficiente para alteração")
            return

        # 3️⃣ BAIXA NOVO ESTOQUE
        execute("""
            UPDATE produtos
            SET estoque = estoque - ?
            WHERE nome=?
        """, (qtd_nova, prod_edit))

        # 4️⃣ ATUALIZA VENDA
        execute("""
            UPDATE vendas
            SET produto=?, quantidade=?, total=?, lucro=?
            WHERE rowid=?
        """, (
            prod_edit,
            qtd_nova,
            total_novo,
            lucro_novo,
            venda_id
        ))

        st.success("✅ Venda atualizada")
        st.rerun()

    # =========================
    # PDF
    # =========================

    st.divider()

    if st.button("📄 Gerar PDF"):
        gerar_pdf_vendas(vendas)

        with open("relatorio_vendas.pdf", "rb") as file:
            st.download_button(
                label="⬇️ Baixar PDF",
                data=file,
                file_name="relatorio_vendas.pdf",
                mime="application/pdf"
            )
``
