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

    qtd = st.number_input(
        "Quantidade",
        min_value=1.0,
        value=1.0
    )

    cliente = st.text_input("Cliente")

    forma_pagamento = st.selectbox(
        "Forma de Pagamento",
        [
            "Dinheiro",
            "PIX",
            "Cartão Débito",
            "Cartão Crédito",
            "Boleto"
        ]
    )

    status_pagamento = st.selectbox(
        "Status do Pagamento",
        [
            "Pago",
            "Pendente"
        ]
    )

    if st.button("Vender"):

        if qtd > float(info["estoque"]):
            st.error("Estoque insuficiente")
            return

        total = qtd * float(info["venda"])
        lucro = total - (qtd * float(info["custo"]))

        execute(
            """
            UPDATE produtos
            SET estoque = estoque - ?
            WHERE id = ?
            """,
            (qtd, int(info["id"]))
        )

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
        """,
        (
            produto_nome,
            qtd,
            total,
            lucro,
            cliente,
            forma_pagamento,
            status_pagamento
        ))

 if status_pagamento == "Pago":
execute("""
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
    status_pagamento
))

        st.success("✅ Venda realizada com sucesso!")
        st.rerun()

    st.divider()

    st.subheader("📋 Histórico de Vendas")

    vendas = query("""
        SELECT
            id,
            data,
            produto,
            quantidade,
            total,
            lucro,
            cliente,
            forma_pagamento,
            status_pagamento,
            status
        FROM vendas
        ORDER BY id DESC
    """)

    if vendas.empty:

        st.info("Nenhuma venda registrada.")

    else:

        st.dataframe(
            vendas,
            use_container_width=True
        )

        st.divider()

        st.subheader("↩️ Estornar Venda")

        vendas_ativas = vendas[
            vendas["status"] == "Ativa"
        ]

        if vendas_ativas.empty:

            st.info(
                "Nenhuma venda disponível para estorno."
            )

        else:

            venda_id = st.selectbox(
                "Selecione a venda",
                vendas_ativas["id"].tolist()
            )

            if st.button("Estornar Venda"):

                venda = vendas_ativas[
                    vendas_ativas["id"] == venda_id
                ].iloc[0]

                produto = query(
                    """
                    SELECT *
                    FROM produtos
                    WHERE nome = ?
                    """,
                    (venda["produto"],)
                )

                if produto.empty:

                    st.error(
                        "Produto não encontrado."
                    )

                else:

                    produto_id = int(
                        produto.iloc[0]["id"]
                    )

                    quantidade = float(
                        venda["quantidade"]
                    )

                    execute(
                        """
                        UPDATE produtos
                        SET estoque = estoque + ?
                        WHERE id = ?
                        """,
                        (
                            quantidade,
                            produto_id
                        )
                    )

                    execute(
                        """
                        UPDATE vendas
                        SET status = 'Estornada'
                        WHERE id = ?
                        """,
                        (venda_id,)
                    )

                    if venda["status_pagamento"] == "Pago":

                        execute("""
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
                        ))

                    st.success(
                        "✅ Venda estornada com sucesso."
                    )

                    st.rerun()
