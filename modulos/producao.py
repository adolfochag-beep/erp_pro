import streamlit as st
from database.db import query, execute


def show_producao():

    st.subheader("🏭 Produção com Receita Automática")

    # =========================
    # PRODUZIR
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
        "Quantidade a produzir",
        min_value=1.0,
        step=1.0
    )

    if st.button("✅ Produzir"):

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

        # Verifica estoque
        for _, r in receitas.iterrows():
            necessario = r["quantidade"] * qtd
            if r["estoque"] < necessario:
                st.error(f"Estoque insuficiente de {r['materia_nome']}")
                return

        # Desconta matéria‑prima
        custo_total = 0
        for _, r in receitas.iterrows():
            necessario = r["quantidade"] * qtd
            execute("""
                UPDATE produtos
                SET estoque = estoque - ?
                WHERE id = ?
            """, (necessario, r["materia_id"]))
            custo_total += r["custo"] * necessario

        # Atualiza produto final
        execute("""
            UPDATE produtos
            SET estoque = estoque + ?
            WHERE id = ?
        """, (qtd, produto_id))

        # Registra produção
        execute("""
            INSERT INTO producoes(
                produto_final,
                quantidade,
                custo,
                status
            )
            VALUES (?,?,?,?)
        """, (produto_id, qtd, custo_total, "Ativa"))

        st.success("✅ Produção realizada com sucesso!")

    # =========================
    # HISTÓRICO
    # =========================
    st.divider()
    st.subheader("📋 Histórico de Produções")

    producoes = query("""
        SELECT
            pr.id,
            p.nome AS produto_final,
            pr.quantidade,
            pr.custo,
            pr.status,
            pr.data
        FROM producoes pr
        LEFT JOIN produtos p
            ON pr.produto_final = p.id
        ORDER BY pr.data DESC
    """)

    if producoes.empty:
        st.info("Nenhuma produção registrada")
        return

    st.dataframe(
        producoes,
        use_container_width=True,
        height=300,
        hide_index=True
    )

    # =========================
    # CANCELAR PRODUÇÃO
    # =========================
    st.divider()
    st.subheader("❌ Cancelar Produção")

    producoes_ativas = producoes[
        producoes["status"] == "Ativa"
    ]

    if producoes_ativas.empty:
        st.info("Nenhuma produção ativa para cancelar")
        return

    prod_id = st.selectbox(
        "Selecione a produção",
        producoes_ativas["id"]
    )

    if st.button("❌ Cancelar Produção"):

        prod = producoes_ativas[
            producoes_ativas["id"] == prod_id
        ].iloc[0]

        # Devolve produto final
        execute("""
            UPDATE produtos
            SET estoque = estoque - ?
            WHERE nome = ?
        """, (prod["quantidade"], prod["produto_final"]))

        # Devolve matéria‑prima
        receitas = query("""
            SELECT
                r.quantidade,
                p.id AS materia_id
            FROM receitas r
            JOIN produtos p
                ON r.materia_prima = p.id
            WHERE r.produto_final = (
                SELECT produto_final FROM producoes WHERE id = ?
            )
        """, (prod_id,))

        for _, r in receitas.iterrows():
            execute("""
                UPDATE produtos
                SET estoque = estoque + ?
                WHERE id = ?
            """, (r["quantidade"] * prod["quantidade"], r["materia_id"]))

        # Marca como cancelada
        execute("""
            UPDATE producoes
            SET status = 'Cancelada'
            WHERE id = ?
        """, (prod_id,))

        st.success("✅ Produção cancelada com sucesso")
        st.rerun()
