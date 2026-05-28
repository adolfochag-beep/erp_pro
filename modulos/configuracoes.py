import streamlit as st
import bcrypt
from database.db import query, execute


def show_config():

    st.title("⚙️ Configurações")

    st.subheader("🔐 Alterar Senha")

    usuario = st.session_state.get("usuario")

    with st.form("trocar_senha"):

        senha_atual = st.text_input("Senha atual", type="password")
        nova_senha = st.text_input("Nova senha", type="password")
        confirmar = st.text_input("Confirmar nova senha", type="password")

        salvar = st.form_submit_button("Salvar")

        if salvar:

            dados = query(
                "SELECT * FROM usuarios WHERE usuario=?",
                (usuario,)
            )

            if dados.empty:
                st.error("Usuário não encontrado")
                return

            senha_hash = dados.iloc[0]["senha"]

            # valida senha atual
            if not bcrypt.checkpw(
                senha_atual.encode(), senha_hash.encode()
            ):
                st.error("Senha atual incorreta")
                return

            # valida nova senha
            if nova_senha != confirmar:
                st.warning("Senhas não coincidem")
                return

            # grava nova senha
            nova_hash = bcrypt.hashpw(
                nova_senha.encode(),
                bcrypt.gensalt()
            ).decode()

            execute(
                "UPDATE usuarios SET senha=? WHERE usuario=?",
                (nova_hash, usuario)
            )

            st.success("✅ Senha alterada com sucesso")
