import streamlit as st
from database.db import query, execute


def show_produtos():

    st.subheader("📦 Produtos")

    # ✅ FORA DO FORM → atualiza em tempo real
    tipo = st.selectbox(
        "Tipo",
        ["Produto Final", "Matéria Prima"]
    )

    # =========================
    # FORMULÁRIO
    # =========================

    with st.form("produto", clear_on_submit=True):

        nome = st.text_input("Nome").strip()

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

        # ✅ AGORA FUNCIONA EM TEMPO REAL
        if tipo == "Matéria Prima":
            custo = st.number_input(
                "Custo",
                min_value=0.0,
                value=0.0
            )
        else:
            custo = st.number_input(
                "Custo (automático)",
                value=0.0,
                disabled=True
            )
            st.info("Custo calculado automaticamente pela receita.")

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

            produtos_existentes = query("SELECT * FROM produtos")

            if not produtos_existentes.empty:

                existe = produtos_existentes[
                    produtos_existentes["nome"]
                    .astype(str)
                    .str.upper()
                    == nome.upper()
                ]

                if not existe.empty:
                    st.error("Já existe um produto com esse nome.")
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

    # =========================
    # LISTAGEM
    # =========================

    st.divider()

    produtos = query("SELECT * FROM produtos ORDER BY nome")

    if produtos.empty:
        st.info("Nenhum produto cadastrado.")
        return

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
