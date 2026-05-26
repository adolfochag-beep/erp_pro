import streamlit as st
from database.db import query, execute

def show_financeiro():

    st.title("💰 Financeiro")

    with st.form("fin"):

        tipo = st.selectbox("Tipo", ["Entrada", "Saída"])

        desc = st.text_input("Descrição")

        valor = st.number_input("Valor", min_value=0.0)

        if st.form_submit_button("Salvar"):

            execute("""
            INSERT INTO financeiro(tipo, descricao, valor, status)
            VALUES(?,?,?,?)
            """, (tipo, desc, valor, "OK"))

            st.success("Registrado")

    st.dataframe(query("SELECT * FROM financeiro"), use_container_width=True)