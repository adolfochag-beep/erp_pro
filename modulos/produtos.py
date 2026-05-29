import streamlit as st
from database.db import query, execute


def show_produtos():

    st.title("📦 Produtos")

    with st.form("produto", clear_on_submit=True):

        nome = st.text_input("Nome")

        tipo = st.selectbox(
            "Tipo",
            ["Produto Final", "Matéria Prima"]
        )

        unidade = st.selectbox(
            "Unidade",
            ["UN", "KG", "L"]
        )

        estoque = st.number_input("Estoque", min_value=0.0)
        estoque_min = st.number_input("Estoque Mínimo", min_value=0.0)

        # ✅ custo só para matéria-prima
        custo = 0.0
        if tipo == "Matéria Prima":
            custo = st.number_input("Custo", min_value=0.0)

        venda = st.number_input("Preço Venda", min_value=0.0)

        if st.form_submit_button("Salvar"):

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

            st.success("✅ Produto cadastrado")

    st.divider()

    produtos = query("SELECT * FROM produtos")

    st.data_editor(
        produtos,
        use_container_width=True,
        height=400
    )
