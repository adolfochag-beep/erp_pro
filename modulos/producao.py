import streamlit as st
from database.db import query, execute


def show_producao():

    st.title("🏭 Produção com Receita Automática")

    # =========================
    # PRODUTOS FINAIS
    # =========================
    produtos = query("""
        SELECT *
        FROM produtos
        WHERE tipo = 'Produto Final'
    """)

    if produtos.empty:
        st.warning("Nenhum produto final cadastrado")
        return

    produto_nome = st.selectbox(
        "Produto a produzir",
        produtos["nome"].tolist()
    )

    produto = produtos[
        produtos["nome"] == produto_nome
    ].iloc[0]

    produto_id = int(produto["id"])

    qtd = st.number_input(
        "Quantidade",
        min_value=1.0,
        step=1.0
    )

    if st.button("Produzir"):

        # =========================
        # BUSCA RECEITA PELO ID
        # =========================
        receitas = query("""
            SELECT
                r.quantidade,
                p.id AS materia_id,
                p.nome AS materia_nome,
                p.estoque,
                p.custo
            FROM receitas r
            JOIN produtos p
                ON r.materia_prima = p.id
            WHERE r.produto_final = ?
        """, (produto_id,))

        if receitas.empty:
            st.error("Produto não possui receita cadastrada")
            return

        # =========================
        # VERIFICA ESTOQUE
        # =========================
        for _, r in receitas.iterrows():

            necessario = r["quantidade"] * qtd

            if r["estoque"] < necessario:
                st.error(
                    f"Estoque insuficiente de {r['materia_nome']}"
                )
                return

        # =========================
        # DESCONTA MATÉRIA-PRIMA
        # =========================
        custo_total = 0

        for _, r in receitas.iterrows():

            necessario = r["quantidade"] * qtd
            novo_estoque = r["estoque"] - necessario

            execute("""
                UPDATE produtos
                SET estoque = ?
                WHERE id = ?
            """, (novo_estoque, r["materia_id"]))

            custo_total += r["custo"] * necessario

        # =========================
        # ATUALIZA PRODUTO FINAL
        # =========================
        novo_final = produto["estoque"] + qtd

        execute("""
            UPDATE produtos
            SET estoque = ?
            WHERE id = ?
        """, (novo_final, produto_id))

        # =========================
        # REGISTRA PRODUÇÃO
        # =========================
        execute("""
            INSERT INTO producoes(
                produto_final,
                quantidade,
                custo
            )
            VALUES (?,?,?)
        """, (produto_id, qtd, custo_total))

        st.success("✅ Produção realizada com sucesso!")
