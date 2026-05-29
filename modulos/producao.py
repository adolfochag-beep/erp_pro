import streamlit as st
from database.db import query, execute

def show_producao():

    st.subheader("🏭 Produção")

    produtos = query("SELECT * FROM produtos WHERE tipo='Produto Final'")
    produto_nome = st.selectbox("Produto", produtos["nome"])
    produto = produtos[produtos["nome"] == produto_nome].iloc[0]
    qtd = st.number_input("Quantidade", min_value=1.0)

    if st.button("Produzir"):

        receitas = query("""
            SELECT r.quantidade, p.id mp_id, p.nome mp_nome, p.estoque, p.custo
            FROM receitas r
            JOIN produtos p ON r.materia_prima = p.id
            WHERE r.produto_final = ?
        """, (produto["id"],))

        for _, r in receitas.iterrows():
            if r["estoque"] < r["quantidade"] * qtd:
                st.error(f"Estoque insuficiente de {r['mp_nome']}")
                return

        custo = 0
        for _, r in receitas.iterrows():
            execute("UPDATE produtos SET estoque = estoque - ? WHERE id = ?",
                    (r["quantidade"] * qtd, r["mp_id"]))
            custo += r["custo"] * r["quantidade"] * qtd

        execute("UPDATE produtos SET estoque = estoque + ? WHERE id = ?",
                (qtd, produto["id"]))

        execute("""
            INSERT INTO producoes(produto_final, quantidade, custo, status)
            VALUES(?,?,?,?)
        """, (produto["id"], qtd, custo, "Ativa"))

        st.success("✅ Produção registrada")

    st.divider()
    st.subheader("📋 Histórico")

    producoes = query("""
        SELECT pr.id, p.nome produto, pr.quantidade, pr.custo, pr.status, pr.data
        FROM producoes pr
        JOIN produtos p ON pr.produto_final = p.id
    """)

    st.dataframe(producoes, use_container_width=True)
