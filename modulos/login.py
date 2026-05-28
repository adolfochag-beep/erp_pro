import streamlit as st
import os
import bcrypt
from database.db import query

SESSION_FILE = "session_login.txt"

def salvar_sessao(usuario):
    with open(SESSION_FILE, "w") as f:
        f.write(usuario)

def carregar_sessao():
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, "r") as f:
            return f.read()
    return None

def limpar_sessao():
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)

def show_login():

    usuario_salvo = carregar_sessao()

    if usuario_salvo:
        st.session_state["logado"] = True
        st.session_state["usuario"] = usuario_salvo
        return

    st.title("🔐 Login")

    with st.form("login"):
        user = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")

        if st.form_submit_button("Entrar"):

            dados = query("SELECT * FROM usuarios WHERE usuario=?", (user,))

            if not dados.empty:
                senha_hash = dados.iloc[0]["senha"]

                if bcrypt.checkpw(senha.encode(), senha_hash.encode()):
                    st.session_state["logado"] = True
                    st.session_state["usuario"] = user
                    salvar_sessao(user)
                    st.rerun()

            st.error("Login inválido")
