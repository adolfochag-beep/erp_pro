import streamlit as st
from database.db import query, execute

def show_producao():

    st.subheader("🏭 Produção")

    # Busca todos os produtos
    produtos = query("SELECT * FROM produtos")

    if produtos.empty:
        st.warning("Nenhum produto cadastrado.")
        return

    # Normaliza igual ao módulo de receitas
    produtos["tipo"] = (
        produtos["tipo"]
        .astype(str)
        .str.lower()
        .str.normalize("NFKD")
        .str.encode("ascii", errors="ignore")
        .str.decode("utf-8")
    )

    # Filtra produtos finais
    produtos_finais = produtos[
        produtos["tipo"] == "produto final"
    ]

    if produtos_finais.empty:
        st.warning("Nenhum Produto Final cadastrado.")
        return

    produto_nome = st.selectbox(
        "Produto",
        produtos_finais["nome"].tolist()
    )

    produto_filtrado = produtos_finais[
        produtos_finais["nome"] == produto_nome
    ]

    if produto_filtrado.empty:
        st.error("Produto não encontrado.")
        return

    produto = produto_filtrado.iloc[0]

    qtd = st.number_input(
        "Quantidade",
        min_value=1.0,
        value=1.0,
        step=1.0
    )

    if st.button("Produzir"):

        produto_id = int(produto["id"])

        receitas = query("""
            SELECT
                r.quantidade,
                p.id AS mp_id,
                p.nome AS mp_nome,
                p.estoque,
                p.custo
            FROM receitas r
            INNER JOIN produtos p
                ON r.materia_prima = p.id
            WHERE r.produto_final = ?
        """, (produto_id,))

        # Diagnóstico temporário
        st.write("Produto ID:", produto_id)
        st.write("Receitas encontradas:", len(receitas))

        if receitas.empty:
            st.error(
                f"Nenhuma receita encontrada para o produto '{produto_nome}'."
            )
            return

        # Valida estoque das matérias-primas
        for _, r in receitas.iterrows():

            necessario = float(r["quantidade"]) * qtd

            if float(r["estoque"]) < necessario:
                st.error(
                    f"Estoque insuficiente de {r['mp_nome']} "
                    f"(necessário: {necessario}, disponível: {r['estoque']})"
                )
                return

        custo_total = 0

        # Consome matérias-primas
        for _, r in receitas.iterrows():

            consumo = float(r["quantidade"]) * qtd

            execute(
                """
                UPDATE produtos
                SET estoque = estoque - ?
                WHERE id = ?
                """,
                (consumo, int(r["mp_id"]))
            )

            custo_total += (
                float(r["custo"]) * consumo
            )

        # Adiciona produto final ao estoque
        execute(
            """
            UPDATE produtos
            SET estoque = estoque + ?
            WHERE id = ?
            """,
            (qtd, produto_id)
        )

        # Registra produção
        execute("""
            INSERT INTO producoes(
                produto_final,
                quantidade,
                custo,
                status
            )
            VALUES (?, ?, ?, ?)
        """, (
            produto_id,
            qtd,
            custo_total,
            "Ativa"
        ))

        st.success("✅ Produção registrada com sucesso!")

        st.rerun()

    st.divider()

    st.subheader("📋 Histórico de Produção")

    producoes = query("""
        SELECT
            pr.id,
            p.nome AS produto,
            pr.quantidade,
            pr.custo,
            pr.status,
            pr.data
        FROM producoes pr
        LEFT JOIN produtos p
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
