import streamlit as st
import os
from database.db import query
import bcrypt

SESSION_FILE = "session_login.txt"


def salvar_sessao(usuario):
    with open(SESSION_FILE, "w") as f:
        f.write(usuario)


def carregar_sessao():
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, "r") as f:
            return f.read().strip()
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

    c1, c2, c3 = st.columns([1, 1.2, 1])

    with c2:
        st.title("🔐 ERP PRO MAX")

        with st.form("login"):

            usuario = st.text_input("Usuário")
            senha = st.text_input("Senha", type="password")

            entrar = st.form_submit_button("Entrar")

            if entrar:

                if not usuario or not senha:
                    st.warning("Informe usuário e senha")
                    return

                dados = query(
                    "SELECT * FROM usuarios WHERE usuario=?",
                    (usuario,)
                )

                if not dados.empty:

                    senha_hash = dados.iloc[0]["senha"]

                    if bcrypt.checkpw(senha.encode(), senha_hash.encode()):

                        st.session_state["logado"] = True
                        st.session_state["usuario"] = usuario

                        salvar_sessao(usuario)

                        st.rerun()

                st.error("Usuário ou senha inválidos")
