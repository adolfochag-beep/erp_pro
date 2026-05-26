import streamlit as st
from database.db import query, execute

def show_produtos():

    st.title("📦 Produtos")

    with st.form("produto"):

        nome = st.text_input("Nome")

        tipo = st.selectbox("Tipo", ["Produto Final", "Matéria Prima"])

        unidade = st.selectbox("Unidade", ["UN", "KG", "L"])

        estoque = st.number_input("Estoque", min_value=0.0, step=0.1)

        estoque_min = st.number_input("Estoque Mínimo", min_value=0.0, step=0.1)

        custo = st.number_input("Custo", min_value=0.0)

        venda = st.number_input("Preço Venda", min_value=0.0)

        if st.form_submit_button("Salvar"):

            execute("""
            INSERT INTO produtos(nome, tipo, unidade, estoque, estoque_min, custo, venda)
            VALUES(?,?,?,?,?,?,?)
            """, (nome, tipo, unidade, estoque, estoque_min, custo, venda))

            st.success("Produto salvo")

    st.divider()

    st.dataframe(query("SELECT * FROM produtos"), use_container_width=True)