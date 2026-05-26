import streamlit as st
from database.db import query, execute

def show_receitas():

    st.title("📚 Receitas (Produto → Matéria-prima)")

    produtos = query("SELECT * FROM produtos")

    produto_final = st.selectbox("Produto Final", produtos["nome"])

    materia_prima = st.selectbox("Matéria Prima", produtos["nome"])

    qtd = st.number_input("Quantidade por unidade", min_value=0.0, step=0.1)

    if st.button("Adicionar Receita"):

        execute("""
        INSERT INTO receitas(produto_final, materia_prima, quantidade)
        VALUES(?,?,?)
        """, (produto_final, materia_prima, qtd))

        st.success("Receita adicionada")

    st.divider()

    st.dataframe(query("SELECT * FROM receitas"), use_container_width=True)