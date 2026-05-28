import streamlit as st
import bcrypt
import pandas as pd

from database.db import (
    users_conn,
    init_db
)


def criar_usuario(usuario, senha):

    c = users_conn()

    cur = c.cursor()

    senha_hash = bcrypt.hashpw(
        senha.encode(),
        bcrypt.gensalt()
    ).decode()

    try:

        cur.execute("""
        INSERT INTO usuarios(
            usuario,
            senha,
            trocar_senha
        )
        VALUES(?,?,?)
        """, (
            usuario,
            senha_hash,
            0
        ))

        c.commit()

        c.close()

        return True

    except:

        c.close()

        return False


def show_login():

    st.markdown("""
    <div style='text-align:center;padding-top:40px;'>

    <h1>🚀 ERP PRO MAX</h1>

    <p>Sistema de Gestão Empresarial</p>

    </div>
    """, unsafe_allow_html=True)

    abas = st.tabs([
        "🔐 Login",
        "📝 Criar Conta"
    ])

    # =========================
    # LOGIN
    # =========================

    with abas[0]:

        usuario = st.text_input(
            "Usuário",
            key="login_user"
        )

        senha = st.text_input(
            "Senha",
            type="password",
            key="login_pass"
        )

        if st.button(
            "Entrar"
        ):

            c = users_conn()

            user = pd.read_sql_query(
                """
                SELECT *
                FROM usuarios
                WHERE usuario = ?
                """,
                c,
                params=(usuario,)
            )

            c.close()

            if user.empty:

                st.error(
                    "Usuário inválido"
                )

                return

            senha_hash = user.iloc[0]["senha"]

            if bcrypt.checkpw(
                senha.encode(),
                senha_hash.encode()
            ):

                st.session_state["logado"] = True

                st.session_state["usuario"] = usuario

                # CRIA BANCO AUTOMÁTICO
                init_db()

                st.success(
                    "Login realizado"
                )

                st.rerun()

            else:

                st.error(
                    "Senha incorreta"
                )

    # =========================
    # CADASTRO
    # =========================

    with abas[1]:

        novo_usuario = st.text_input(
            "Novo Usuário"
        )

        nova_senha = st.text_input(
            "Nova Senha",
            type="password"
        )

        confirmar = st.text_input(
            "Confirmar Senha",
            type="password"
        )

        if st.button(
            "Criar Conta"
        ):

            if not novo_usuario:

                st.warning(
                    "Informe usuário"
                )

                return

            if len(nova_senha) < 4:

                st.warning(
                    "Senha muito curta"
                )

                return

            if nova_senha != confirmar:

                st.error(
                    "Senhas diferentes"
                )

                return

            criado = criar_usuario(
                novo_usuario,
                nova_senha
            )

            if criado:

                st.success("""
                Conta criada com sucesso.

                Agora faça login.
                """)

            else:

                st.error("""
                Usuário já existe
                """)
