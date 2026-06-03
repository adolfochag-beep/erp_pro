import streamlit as st
from database.db import query, execute


def show_vendas():

    st.subheader("🛒 Vendas")

    produtos = query("SELECT * FROM produtos")

    if produtos.empty:
        st.warning("Nenhum produto cadastrado.")
        return

    produtos["tipo"] = (
        produtos["tipo"]
        .astype(str)
        .str.lower()
        .str.strip()
    )

    produtos = produtos[
        produtos["tipo"] == "produto final"
    ]

    if produtos.empty:
        st.warning("Nenhum produto final cadastrado.")
        return

    produto_nome = st.selectbox(
        "Produto",
        produtos["nome"].tolist()
    )

    info = produtos[
        produtos["nome"] == produto_nome
    ].iloc[0]

    produto_id = int(info["id"])  # ✅ NOVO

    qtd = st.number_input(
        "Quantidade",
        min_value=1,
        value=1
    )

    cliente = st.text_input("Cliente")

    forma_pagamento = st.selectbox(
        "Forma de Pagamento",
        ["Dinheiro", "PIX", "Cartão Débito", "Cartão Crédito", "Boleto"]
    )

    status_pagamento = st.selectbox(
        "Status do Pagamento",
        ["Pago", "Pendente"]
    )

    total = qtd * float(info["venda"])
    lucro = total - (qtd * float(info["custo"]))

    if st.button("Vender"):

        if qtd > float(info["estoque"]):
            st.error("Estoque insuficiente")
            return

        try:
            # ✅ Atualiza estoque
            execute(
                """
                UPDATE produtos
                SET estoque = estoque - ?
                WHERE id = ?
                """,
                (qtd, produto_id)
            )

            # ✅ VENDA COM ID
            execute(
                """
                INSERT INTO vendas(
                    produto_id,
                    produto,
                    quantidade,
                    total,
                    lucro,
                    cliente,
                    forma_pagamento,
                    status_pagamento,
                    status
                )
                VALUES(?,?,?,?,?,?,?,?,?)
                """,
                (
                    produto_id,
                    produto_nome,
                    qtd,
                    total,
                    lucro,
                    cliente,
                    forma_pagamento,
                    status_pagamento,
                    "Ativa"
                )
            )

            # ✅ Financeiro
            if status_pagamento == "Pago":
                execute(
                    """
                    INSERT INTO financeiro(
                        tipo,
                        descricao,
                        valor,
                        status
                    )
                    VALUES(?,?,?,?)
                    """,
                    (
                        "Entrada",
                        f"Venda - {produto_nome} ({forma_pagamento})",
                        total,
                        "OK"
                    )
                )

            st.success("✅ Venda realizada com sucesso!")
            st.rerun()

        except Exception as e:
            st.error(f"Erro ao vender: {e}")

    # =========================
    # HISTÓRICO
    # =========================

    st.divider()
    st.subheader("📋 Histórico de Vendas")

    vendas = query("SELECT * FROM vendas ORDER BY id DESC")

    if vendas.empty:
        st.info("Nenhuma venda registrada.")
        return

    st.dataframe(vendas, use_container_width=True)

    # =========================
    # ESTORNO (CORRIGIDO)
    # =========================

    st.divider()
    st.subheader("↩️ Estornar Venda")

    vendas_ativas = vendas[vendas["status"] == "Ativa"]

    if vendas_ativas.empty:
        st.info("Nenhuma venda disponível para estorno.")
        return

    venda_id = st.selectbox(
        "Selecione a venda",
        vendas_ativas["id"].tolist()
    )

    if st.button("Estornar Venda", key="estorno"):

        venda = vendas_ativas[
            vendas_ativas["id"] == venda_id
        ].iloc[0]

        produto_id = int(venda["produto_id"])  # ✅ AGORA CORRETO

        quantidade = float(venda["quantidade"])

        try:
            # ✅ devolve estoque
            execute(
                """
                UPDATE produtos
                SET estoque = estoque + ?
                WHERE id = ?
                """,
                (quantidade, produto_id)
            )

            # ✅ marca estornada
            execute(
                """
                UPDATE vendas
                SET status = 'Estornada'
                WHERE id = ?
                """,
                (venda_id,)
            )

            # ✅ financeiro
            if venda["status_pagamento"] == "Pago":

                execute(
                    """
                    INSERT INTO financeiro(
                        tipo,
                        descricao,
                        valor,
                        status
                    )
                    VALUES(?,?,?,?)
                    """,
                    (
                        "Saída",
                        f"Estorno Venda #{venda_id}",
                        float(venda["total"]),
                        "OK"
                    )
                )

            st.success("✅ Venda estornada com sucesso.")
            st.rerun()

        except Exception as e:
            st.error(f"Erro ao estornar: {e}")
