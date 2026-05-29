import streamlit as st
from database.db import query, execute, recalcular_custo_produto


def show_receitas():

    st.subheader("📚 Receitas (BOM)")

    produtos = query("SELECT * FROM produtos")

    if produtos.empty:
        st.warning("Cadastre produtos primeiro.")
        return

    produtos["tipo"] = (
        produtos["tipo"]
        .astype(str)
        .str.lower()
        .str.normalize("NFKD")
        .str.encode("ascii", errors="ignore")
        .str.decode("utf-8")
        .str.strip()
    )

    finais = produtos[
        produtos["tipo"] == "produto final"
    ]

    materias = produtos[
        produtos["tipo"] == "materia prima"
    ]

    if finais.empty:
        st.warning(
            "Nenhum Produto Final cadastrado."
        )
        return

    if materias.empty:
        st.warning(
            "Nenhuma Matéria Prima cadastrada."
        )
        return

    # =========================
    # CADASTRO
    # =========================

    with st.form("receita", clear_on_submit=True):

        pf = st.selectbox(
            "Produto Final",
            finais["nome"].tolist()
        )

        mp = st.selectbox(
            "Matéria Prima",
            materias["nome"].tolist()
        )

        qtd = st.number_input(
            "Quantidade",
            min_value=0.01,
            value=1.0,
            step=0.01
        )

        salvar = st.form_submit_button(
            "Adicionar"
        )

        if salvar:

            pf_id = int(
                finais[
                    finais["nome"] == pf
                ]["id"].iloc[0]
            )

            mp_id = int(
                materias[
                    materias["nome"] == mp
                ]["id"].iloc[0]
            )

            # Impede duplicidade
            existente = query("""
                SELECT *
                FROM receitas
                WHERE produto_final = ?
                AND materia_prima = ?
            """, (pf_id, mp_id))

            if not existente.empty:
                st.error(
                    "Essa matéria-prima já existe nessa receita."
                )
                st.stop()

            execute("""
                INSERT INTO receitas(
                    produto_final,
                    materia_prima,
                    quantidade
                )
                VALUES(?,?,?)
            """,
            (
                pf_id,
                mp_id,
                qtd
            ))

            recalcular_custo_produto(
                pf_id
            )

            st.success(
                "✅ Receita cadastrada"
            )

            st.rerun()

    st.divider()

    # =========================
    # LISTAGEM
    # =========================

    receitas = query("""
        SELECT
            r.id,
            r.produto_final,
            r.materia_prima,
            pf.nome AS produto_final_nome,
            mp.nome AS materia_prima_nome,
            r.quantidade
        FROM receitas r
        LEFT JOIN produtos pf
            ON r.produto_final = pf.id
        LEFT JOIN produtos mp
            ON r.materia_prima = mp.id
        ORDER BY pf.nome
    """)

    if receitas.empty:
        st.info(
            "Nenhuma receita cadastrada."
        )
        return

    st.subheader(
        "📋 Itens das Receitas"
    )

    exibir = receitas[
        [
            "id",
            "produto_final_nome",
            "materia_prima_nome",
            "quantidade"
        ]
    ]

    edited_df = st.data_editor(
        exibir,
        use_container_width=True,
        height=400,
        disabled=[
            "id",
            "produto_final_nome",
            "materia_prima_nome"
        ]
    )

    # =========================
    # SALVAR EDIÇÃO
    # =========================

    if st.button(
        "💾 Salvar Alterações"
    ):

        for _, row in edited_df.iterrows():

            execute("""
                UPDATE receitas
                SET quantidade = ?
                WHERE id = ?
            """,
            (
                row["quantidade"],
                row["id"]
            ))

        produtos_afetados = receitas[
            "produto_final"
        ].unique()

        for prod_id in produtos_afetados:
            recalcular_custo_produto(
                int(prod_id)
            )

        st.success(
            "✅ Alterações salvas"
        )

        st.rerun()

    st.divider()

    # =========================
    # EXCLUSÃO
    # =========================

    st.subheader(
        "🗑️ Excluir Item da Receita"
    )

    item_del = st.selectbox(
        "Selecione",
        receitas["id"].tolist(),
        format_func=lambda x:
            f"ID {x} - "
            f"{receitas[receitas['id']==x]['produto_final_nome'].iloc[0]}"
            f" / "
            f"{receitas[receitas['id']==x]['materia_prima_nome'].iloc[0]}"
    )

    if st.button(
        "Excluir Item"
    ):

        linha = receitas[
            receitas["id"] == item_del
        ]

        if linha.empty:
            st.error(
                "Item não encontrado."
            )
            return

        produto_final_id = int(
            linha.iloc[0]["produto_final"]
        )

        execute(
            """
            DELETE FROM receitas
            WHERE id = ?
            """,
            (item_del,)
        )

        recalcular_custo_produto(
            produto_final_id
        )

        st.success(
            "✅ Item excluído"
        )

        st.rerun()

    st.divider()

    # =========================
    # CUSTOS
    # =========================

    st.subheader(
        "💰 Custos dos Produtos"
    )

    custos = query("""
        SELECT
            nome,
            custo,
            venda
        FROM produtos
        WHERE LOWER(tipo)
        LIKE '%produto%'
        ORDER BY nome
    """)

    if not custos.empty:

        custos["Margem"] = (
            custos["venda"]
            - custos["custo"]
        )

        st.dataframe(
            custos,
            use_container_width=True
                   )
