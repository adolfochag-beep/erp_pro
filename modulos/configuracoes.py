import streamlit as st
import bcrypt
import shutil
import os

from database.db import (
    query,
    execute,
    get_user_db
)


def show_config():

    st.title("⚙️ Configurações")

    aba1, aba2 = st.tabs([
        "🔐 Segurança",
        "🧾 Sistema"
    ])

    # =========================
    # SEGURANÇA
    # =========================

    with aba1:

        st.subheader("🔑 Alterar Senha")

        usuario = st.session_state.get("usuario")

        with st.form("trocar_senha"):

            senha_atual = st.text_input(
                "Senha atual",
                type="password"
            )

            nova_senha = st.text_input(
                "Nova senha",
                type="password"
            )

            confirmar = st.text_input(
                "Confirmar nova senha",
                type="password"
            )

            salvar = st.form_submit_button(
                "Salvar"
            )

            if salvar:

                dados = query(
                    """
                    SELECT *
                    FROM usuarios
                    WHERE usuario=?
                    """,
                    (usuario,)
                )

                if dados.empty:
                    st.error(
                        "Usuário não encontrado."
                    )
                    return

                senha_hash = dados.iloc[0]["senha"]

                if not bcrypt.checkpw(
                    senha_atual.encode(),
                    senha_hash.encode()
                ):
                    st.error(
                        "Senha atual incorreta."
                    )
                    return

                if nova_senha != confirmar:
                    st.warning(
                        "As senhas não coincidem."
                    )
                    return

                if len(nova_senha) < 4:
                    st.warning(
                        "A senha deve ter pelo menos 4 caracteres."
                    )
                    return

                nova_hash = bcrypt.hashpw(
                    nova_senha.encode(),
                    bcrypt.gensalt()
                ).decode()

                execute(
                    """
                    UPDATE usuarios
                    SET senha=?
                    WHERE usuario=?
                    """,
                    (
                        nova_hash,
                        usuario
                    )
                )

                st.success(
                    "✅ Senha atualizada com sucesso."
                )

    # =========================
    # SISTEMA
    # =========================

    with aba2:

        st.subheader("📌 Informações do Sistema")

        st.info("""
ERP PRO MAX

✔ Controle de Estoque
✔ Produção
✔ Receitas (BOM)
✔ Vendas
✔ Financeiro
✔ Compras
✔ Multiusuário
        """)

        st.divider()

        st.subheader("💾 Backup")

        banco_usuario = get_user_db()

        st.caption(
            f"Banco atual: {os.path.basename(banco_usuario)}"
        )

        if st.button("Gerar Backup"):

            if not os.path.exists(banco_usuario):

                st.error(
                    "Banco de dados não encontrado."
                )

                return

            from datetime import datetime

            nome_backup = (
                f"backup_"
                f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
            )

            shutil.copy(
                banco_usuario,
                nome_backup
            )

            st.success(
                "✅ Backup gerado com sucesso."
            )

            with open(
                nome_backup,
                "rb"
            ) as f:

                st.download_button(
                    label="📥 Baixar Backup",
                    data=f,
                    file_name=nome_backup,
                    mime="application/octet-stream"
                )
