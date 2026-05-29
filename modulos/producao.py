import streamlit as st
from database.db import query, execute

def show_producao():

    st.subheader("🏭 Produção")

    produtos = query("SELECT * FROM produtos WHERE tipo='Produto Final'")

    # valida se existem produtos
    if produtos.empty:
        st.warning("Nenhum produto final cadastrado.")
        return

    produto_nome = st.selectbox(
        "Produto",
        produtos["nome"].tolist()
    )

    produto_filtrado = produtos[produtos["nome"] == produto_nome]

    # valida filtro
    if produto_filtrado.empty:
        st.error("Produto não encontrado.")
        return

    produto = produto_filtrado.iloc[0]

    qtd = st.number_input(
        "Quantidade",
        min_value=1.0,
        value=1.0
    )

    if st.button("Produzir"):

        receitas = query("""
            SELECT
                r.quantidade,
                p.id mp_id,
                p.nome mp_nome,
                p.estoque,
                p.custo
            FROM receitas r
            JOIN produtos p
                ON r.materia_prima = p.id
            WHERE r.produto_final = ?
        """, (produto["id"],))

        # valida se possui receita
        if receitas.empty:
            st.error("Esse produto não possui receita cadastrada.")
            return

        # valida estoque
        for _, r in receitas.iterrows():

            necessario = r["quantidade"] * qtd

            if r["estoque"] < necessario:
                st.error(
                    f"Estoque insuficiente de {r['mp_nome']}"
                )
                return

        custo = 0

        # baixa matéria-prima
        for _, r in receitas.iterrows():

            consumo = r["quantidade"] * qtd

            execute(
                "UPDATE produtos SET estoque = estoque - ? WHERE id = ?",
                (consumo, r["mp_id"])
            )

            custo += r["custo"] * consumo

        # adiciona produto final
        execute(
            "UPDATE produtos SET estoque = estoque + ? WHERE id = ?",
            (qtd, produto["id"])
        )

        # registra produção
        execute("""
            INSERT INTO producoes(
                produto_final,
                quantidade,
                custo,
                status
            )
            VALUES(?,?,?,?)
        """, (
            produto["id"],
            qtd,
            custo,
            "Ativa"
        ))

        st.success("✅ Produção registrada")

    st.divider()

    st.subheader("📋 Histórico")

    producoes = query("""
        SELECT
            pr.id,
            p.nome produto,
            pr.quantidade,
            pr.custo,
            pr.status,
            pr.data
        FROM producoes pr
        JOIN produtos p
            ON pr.produto_final = p.id
        ORDER BY pr.id DESC
    """)

    if producoes.empty:
        st.info("Nenhuma produção registrada.")
    else:
        st.dataframe(
            producoes,
            use_container_width=True
        )
