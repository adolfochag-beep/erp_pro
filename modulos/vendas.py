import streamlit as st
from database.db import query, execute

def show_vendas():

    st.title("🛒 Vendas")

    produtos = query("SELECT * FROM produtos WHERE tipo='Produto Final'")

    if produtos.empty:
        st.warning("Sem produtos cadastrados")
        return

    produto = st.selectbox("Produto", produtos["nome"])

    info = produtos[produtos["nome"] == produto].iloc[0]

    qtd = st.number_input("Quantidade", min_value=1.0, step=1.0)

    total = qtd * info["venda"]

    st.info(f"Total: R$ {total:,.2f}")

    if st.button("Finalizar Venda"):

        if qtd > info["estoque"]:
            st.error("Estoque insuficiente")
            return

        novo_estoque = info["estoque"] - qtd

        lucro = total - (qtd * info["custo"])

        execute("UPDATE produtos SET estoque=? WHERE id=?", (novo_estoque, info["id"]))

        execute("""
        INSERT INTO vendas(produto, quantidade, total, lucro)
        VALUES(?,?,?,?)
        """, (produto, qtd, total, lucro))

        st.success("Venda registrada")