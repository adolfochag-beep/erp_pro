import streamlit as st


def show_config():

    st.title("⚙️ Configurações")

    st.subheader("Perfil")

    st.info("Área de configurações do ERP")

    st.text_input("Nome da empresa")

    st.text_input("Email")

    st.text_input("Telefone")

    st.button("Salvar alterações")
