import streamlit as st
from database.db import query, execute

def show_vendas():

    st.subheader("🛒 Vendas")

    produtos = query("SELECT * FROM produtos WHERE tipo='Produto Final'")

    # valida produtos
    if produtos.empty:
        st.warning("Nenhum produto final cadastrado.")
        return

    produto_nome = st.selectbox(
        "Produto",
        produtos["nome"].tolist()
    )

    produto_filtrado = produtos[
        produtos["nome"] == produto_nome
    ]

    # valida filtro
    if produto_filtrado.empty:
        st.error("Produto não encontrado.")
        return

    info = produto_filtrado.iloc[0]

    qtd = st.number_input(
        "Quantidade",
        min_value=1.0,
        value=1.0
    )

    if st.button("Vender"):

        if qtd > info["estoque"]:
            st.error("Estoque insuficiente")
            return

        total = qtd * info["venda"]
        lucro = total - (qtd * info["custo"])

        # baixa estoque
        execute(
            "UPDATE produtos SET estoque = estoque - ? WHERE id=?",
            (qtd, info["id"])
        )

        # registra venda
        execute("""
            INSERT INTO vendas(
                produto,
                quantidade,
                total,
                lucro
            )
            VALUES(?,?,?,?)
        """, (
            produto_nome,
            qtd,
            total,
            lucro
        ))

        st.success("✅ Venda realizada")

    st.divider()

    vendas = query("""
        SELECT *
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
