import streamlit as st
from database.db import query, execute


def show_produtos():

    st.subheader("📦 Produtos")

    # =========================
    # CADASTRO
    # =========================

    with st.form("produto", clear_on_submit=True):

        nome = st.text_input("Nome").strip()

        tipo = st.selectbox(
            "Tipo",
            ["Produto Final", "Matéria Prima"]
        )

        unidade = st.selectbox(
            "Unidade",
            ["UN", "KG", "L"]
        )

        estoque = st.number_input(
            "Estoque",
            min_value=0.0,
            value=0.0
        )

        estoque_min = st.number_input(
            "Estoque Mínimo",
            min_value=0.0,
            value=0.0
        )

        custo = 0.0

        if tipo == "Matéria Prima":
            custo = st.number_input(
                "Custo",
                min_value=0.0,
                value=0.0
            )

        venda = st.number_input(
            "Preço Venda",
            min_value=0.0,
            value=0.0
        )

        salvar = st.form_submit_button("Salvar")

        if salvar:

            if not nome:
                st.error("Informe o nome do produto.")
                st.stop()

            produtos_existentes = query(
                "SELECT * FROM produtos"
            )

            if not produtos_existentes.empty:

                existe = produtos_existentes[
                    produtos_existentes["nome"]
                    .astype(str)
                    .str.upper()
                    == nome.upper()
                ]

                if not existe.empty:
                    st.error(
                        "Já existe um produto com esse nome."
                    )
                    st.stop()

            execute("""
                INSERT INTO produtos(
                    nome,
                    tipo,
                    unidade,
                    estoque,
                    estoque_min,
                    custo,
                    venda
                )
                VALUES(?,?,?,?,?,?,?)
            """,
            (
                nome,
                tipo,
                unidade,
                estoque,
                estoque_min,
                custo,
                venda
            ))

            st.success("✅ Produto cadastrado")
            st.rerun()

    st.divider()

    # =========================
    # LISTAGEM
    # =========================

    produtos = query("""
        SELECT *
        FROM produtos
        ORDER BY nome
    """)

    if produtos.empty:
        st.info("Nenhum produto cadastrado.")
        return

    # =========================
    # ALERTA ESTOQUE
    # =========================

    produtos["Status"] = produtos.apply(
        lambda x:
        "⚠️ Baixo"
        if float(x["estoque"]) <= float(x["estoque_min"])
        else "✅ OK",
        axis=1
    )

    st.subheader("📋 Produtos")

    edited_df = st.data_editor(
        produtos,
        use_container_width=True,
        height=450,
        disabled=["id", "Status"]
    )

    # =========================
    # SALVAR ALTERAÇÕES
    # =========================

    if st.button("💾 Salvar Alterações"):

        for _, row in edited_df.iterrows():

            execute("""
                UPDATE produtos
                SET
                    nome=?,
                    tipo=?,
                    unidade=?,
                    estoque=?,
                    estoque_min=?,
                    custo=?,
                    venda=?
                WHERE id=?
            """,
            (
                row["nome"],
                row["tipo"],
                row["unidade"],
                row["estoque"],
                row["estoque_min"],
                row["custo"],
                row["venda"],
                row["id"]
            ))

        st.success("✅ Alterações salvas")
        st.rerun()

    st.divider()

    # =========================
    # EXCLUSÃO
    # =========================

    st.subheader("🗑️ Excluir Produto")

    produto_del = st.selectbox(
        "Selecione o produto",
        produtos["nome"].tolist()
    )

    if st.button("Excluir Produto"):

        prod = produtos[
            produtos["nome"] == produto_del
        ]

        if prod.empty:
            st.error("Produto não encontrado.")
            st.stop()

        prod_id = int(prod.iloc[0]["id"])

        receitas = query("""
            SELECT *
            FROM receitas
            WHERE produto_final = ?
               OR materia_prima = ?
        """, (prod_id, prod_id))

        if not receitas.empty:
            st.error(
                "Produto utilizado em receitas. Não pode ser excluído."
            )
            st.stop()

        execute(
            "DELETE FROM produtos WHERE id=?",
            (prod_id,)
        )

        st.success("✅ Produto excluído")
        st.rerun()
