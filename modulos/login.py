import streamlit as st
import bcrypt
import pandas as pd

from database.db import users_conn

def show_login():

    st.markdown(
        """
        <div style='text-align:center;padding-top:80px;'>

        <h1>🚀 ERP PRO MAX</h1>

        <p>Sistema de Gestão Empresarial</p>

        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1,1,1])

    with col2:

        usuario = st.text_input("Usuário")

        senha = st.text_input(
            "Senha",
            type="password"
        )

        if st.button("Entrar"):

            c = users_conn()

            user = pd.read_sql_query(
                """
                SELECT * FROM usuarios
                WHERE usuario = ?
                """,
                c,
                params=(usuario,)
            )

            c.close()

            if user.empty:

                st.error("Usuário inválido")

                return

            senha_hash = user.iloc[0]["senha"]

            if bcrypt.checkpw(
                senha.encode(),
                senha_hash.encode()
            ):

                st.session_state["logado"] = True

                st.session_state["usuario"] = usuario

                st.rerun()

            else:

                st.error("Senha incorreta")