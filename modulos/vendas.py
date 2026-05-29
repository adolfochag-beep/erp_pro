import streamlit as st
import pandas as pd

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

    produto = st.selectbox("Produto", produtos["nome"])
    info = produtos[produtos["nome"] == produto].iloc[0]

    qtd = st.number_input("Quantidade", min_value=1.0, step=1.0)

    cliente = st.text_input("Cliente / Destinatário")

    forma_pagamento = st.selectbox(
        "Forma de pagamento",
        ["PIX", "Cartão", "Dinheiro", "Boleto", "Transferência"]
    )

    status_pagamento = st.selectbox(
        "Status do pagamento",
        ["Pago", "Pendente"]
    )

    total = qtd * info["venda"]

    st.info(f"Total: R$ {total:,.2f}")

    if st.button("✅ Finalizar Venda"):

        if qtd > info["estoque"]:
            st.error("Estoque insuficiente")
            return

        # =========================
        # AJUSTA ESTOQUE
        # =========================

        novo_estoque = info["estoque"] - qtd
        lucro = total - (qtd * info["custo"])

        execute("""
            UPDATE produtos
            SET estoque=?
            WHERE id=?
        """, (novo_estoque, info["id"]))

        # =========================
        # REGISTRA VENDA
        # =========================

        execute("""
            INSERT INTO vendas(
                produto,
                quantidade,
                total,
                lucro,
                cliente,
                forma_pagamento,
                status_pagamento
            )
            VALUES(?,?,?,?,?,?,?)
        """, (
            produto,
            qtd,
            total,
            lucro,
            cliente,
            forma_pagamento,
            status_pagamento
        ))

        # =========================
        # ALIMENTA FINANCEIRO
        # =========================

        execute("""
            INSERT INTO financeiro(
                tipo,
                descricao,
                valor,
                status
            )
            VALUES(?,?,?,?)
        """, (
            "Entrada",
            f"Venda - {produto} ({cliente})",
            total,
            status_pagamento
        ))

        st.success("✅ Venda registrada e financeiro atualizado")
        st.rerun()

    # =========================
    # HISTÓRICO
    # =========================

    st.divider()
    st.subheader("📋 Histórico de Vendas")

    vendas = query("""
        SELECT
            produto,
            quantidade,
            total,
            cliente,
            forma_pagamento,
            status_pagamento,
            data
        FROM vendas
        ORDER BY data DESC
    """)

    if vendas.empty:
        st.info("Nenhuma venda registrada")
        return

    st.dataframe(vendas, use_container_width=True)
