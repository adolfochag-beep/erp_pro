import streamlit as st
import pandas as pd
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

        estoque = st.number_input("Estoque", min_value=0.0, value=0.0)

        estoque_min = st.number_input("Estoque Mínimo", min_value=0.0, value=0.0)

        # ✅ CUSTO DINÂMICO
        if tipo == "Matéria Prima":
            custo = st.number_input("Custo", min_value=0.0, value=0.0)
        else:
            custo = st.number_input(
                "Custo (automático)",
                value=0.0,
                disabled=True
            )
            st.info("Custo calculado automaticamente pela receita.")

        venda = st.number_input("Preço Venda", min_value=0.0, value=0.0)

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

    # ✅ TRATAMENTO
    produtos["estoque"] = pd.to_numeric(produtos["estoque"], errors="coerce")
    produtos["estoque_min"] = pd.to_numeric(produtos["estoque_min"], errors="coerce")
    produtos["custo"] = pd.to_numeric(produtos["custo"], errors="coerce")
    produtos["venda"] = pd.to_numeric(produtos["venda"], errors="coerce")

    # ✅ STATUS DE ESTOQUE
    produtos["Status"] = produtos.apply(
        lambda x: "⚠️ Baixo"
        if x["estoque"] <= x["estoque_min"]
        else "✅ OK",
        axis=1
    )

    # ✅ RENOMEAR COLUNAS (visual melhor)
    produtos = produtos.rename(columns={
        "nome": "Produto",
        "tipo": "Tipo",
        "unidade": "Unidade",
        "estoque": "Estoque",
        "estoque_min": "Estoque Mín",
        "custo": "Custo (R$)",
        "venda": "Venda (R$)"
    })

    st.subheader("📋 Produtos")

    # ✅ FUNÇÃO DE ESTILO
    def destacar_linha(row):

        if row["Status"] == "⚠️ Baixo":
            return ["background-color: #fee2e2"] * len(row)
        else:
            return [""] * len(row)

    # ✅ TABELA MELHORADA
    st.dataframe(
        produtos.style
        .apply(destacar_linha, axis=1)
        .format({
            "Custo (R$)": "R$ {:,.2f}",
            "Venda (R$)": "R$ {:,.2f}"
        }),
        use_container_width=True,
        height=450
    )

    # =========================
    # EDIÇÃO
    # =========================

    st.subheader("✏️ Editar Produtos")

    edited_df = st.data_editor(
        produtos,
        use_container_width=True,
        height=300,
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
                row["Produto"],
                row["Tipo"],
                row["Unidade"],
                row["Estoque"],
                row["Estoque Mín"],
                row["Custo (R$)"],
                row["Venda (R$)"],
                row["id"]
            ))

        st.success("✅ Alterações salvas")
        st.rerun()
