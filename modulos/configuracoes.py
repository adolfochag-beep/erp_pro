import streamlit as st
import bcrypt

from database.db import execute

def show_config():

    st.title("⚙️ Configurações")

    nova = st.text_input(
        "Nova senha",
        type="password"
    )

    if st.button("Alterar senha"):

        senha_hash = bcrypt.hashpw(
            nova.encode(),
            bcrypt.gensalt()
        ).decode()

        execute("""
        UPDATE usuarios
        SET senha = ?
        WHERE usuario = ?
        """, (
            senha_hash,
            st.session_state["usuario"]
        ))

        st.success("Senha alterada")