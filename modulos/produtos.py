import streamlit as st
import pandas as pd
from database.db import query, execute


def show_produtos():

    st.title("📦 Produtos")

    # =========================
    # FORMULÁRIO
    # =========================

    with st.form("produto", clear_on_submit=True):  # ✅ limpa automático

        nome = st.text_input("Nome")

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
            step=0.1
        )

        estoque_min = st.number_input(
            "Estoque Mínimo",
            min_value=0.0,
            step=0.1
        )

        custo = st.number_input(
            "Custo",
            min_value=0.0
        )

        venda = st.number_input(
            "Preço Venda",
            min_value=0.0
        )

        salvar = st.form_submit_button("Salvar")

        if salvar:

            if not nome:
                st.warning("Informe o nome do produto")
                st.stop()

            # ✅ NÃO REPETIR PRODUTO
            existe = query(
                "SELECT * FROM produtos WHERE LOWER(nome) = LOWER(?)",
                (nome,)
            )

            if not existe.empty:
                st.warning("Produto já cadastrado")
            else:

                execute("""
                INSERT INTO produtos(nome, tipo, unidade, estoque, estoque_min, custo, venda)
                VALUES(?,?,?,?,?,?,?)
                """, (
                    nome,
                    tipo,
                    unidade,
                    estoque,
                    estoque_min,
                    custo,
                    venda
                ))

                st.success("✅ Produto salvo com sucesso")

    st.divider()

    # =========================
    # LISTAGEM (EDITÁVEL)
    # =========================

    produtos = query("SELECT * FROM produtos")

    if not produtos.empty:

        st.subheader("📋 Cadastro de Produtos")

        # ✅ edição direto na tabela
        edited_df = st.data_editor(
            produtos,
            use_container_width=True,
            num_rows="dynamic",
            height=400
        )

        # =========================
        # BOTÃO SALVAR EDIÇÕES
        # =========================

        if st.button("💾 Salvar alterações"):

            for _, row in edited_df.iterrows():

                execute("""
                UPDATE produtos
                SET nome=?, tipo=?, unidade=?, estoque=?, estoque_min=?, custo=?, venda=?
                WHERE id=?
                """, (
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

    else:
        st.info("Nenhum produto cadastrado")
