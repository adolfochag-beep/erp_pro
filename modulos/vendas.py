import streamlit as st
from database.db import query, execute

def show_vendas():

    st.subheader("🛒 Vendas")

    produtos = query("SELECT * FROM produtos WHERE tipo='Produto Final'")
    produto = st.selectbox("Produto", produtos["nome"])
    info = produtos[produtos["nome"] == produto].iloc[0]
    qtd = st.number_input("Quantidade", min_value=1.0)

    if st.button("Vender"):
        if qtd > info["estoque"]:
            st.error("Estoque insuficiente")
            return

        total = qtd * info["venda"]
        lucro = total - qtd * info["custo"]

        execute("UPDATE produtos SET estoque = estoque - ? WHERE id=?",
                (qtd, info["id"]))

        execute("""
            INSERT INTO vendas(produto, quantidade, total, lucro)
            VALUES(?,?,?,?)
        """, (produto, qtd, total, lucro))

        st.success("✅ Venda realizada")

    st.divider()
    st.dataframe(query("SELECT * FROM vendas"), use_container_width=True)
