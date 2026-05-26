import streamlit as st
from database.db import query, execute

def show_producao():

    st.title("🏭 Produção com Receita Automática")

    produtos = query("""
    SELECT * FROM produtos
    WHERE tipo='Produto Final'
    """)

    if produtos.empty:
        st.warning("Nenhum produto final cadastrado")
        return

    produto = st.selectbox("Produto a produzir", produtos["nome"])

    qtd = st.number_input("Quantidade", min_value=1.0, step=1.0)

    if st.button("Produzir"):

        # busca receita do produto
        receitas = query("""
        SELECT * FROM receitas
        WHERE produto_final = ?
        """, (produto,))

        if receitas.empty:
            st.error("Produto não possui receita cadastrada")
            return

        # VERIFICA E DESCONTA MATÉRIA PRIMA
        for _, r in receitas.iterrows():

            materia = query("""
            SELECT * FROM produtos
            WHERE nome = ?
            """, (r["materia_prima"],)).iloc[0]

            necessario = r["quantidade"] * qtd

            if materia["estoque"] < necessario:

                st.error(f"Estoque insuficiente de {materia['nome']}")
                return

        # agora desconta tudo
        custo_total = 0

        for _, r in receitas.iterrows():

            materia = query("""
            SELECT * FROM produtos
            WHERE nome = ?
            """, (r["materia_prima"],)).iloc[0]

            necessario = r["quantidade"] * qtd

            novo_estoque = materia["estoque"] - necessario

            execute("""
            UPDATE produtos
            SET estoque = ?
            WHERE id = ?
            """, (novo_estoque, materia["id"]))

            custo_total += materia["custo"] * necessario

        # adiciona produto final
        produto_final = produtos[produtos["nome"] == produto].iloc[0]

        novo_final = produto_final["estoque"] + qtd

        execute("""
        UPDATE produtos
        SET estoque = ?
        WHERE id = ?
        """, (novo_final, produto_final["id"]))

        # registra produção
        execute("""
        INSERT INTO producoes(produto, quantidade, custo)
        VALUES(?,?,?)
        """, (produto, qtd, custo_total))

        st.success("Produção realizada com sucesso!")