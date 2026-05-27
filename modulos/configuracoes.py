import streamlit as st

from backup import gerar_backup


def show_config():

    st.title("⚙️ Configurações")

    st.subheader("🏢 Empresa")

    st.text_input(
        "Nome da Empresa"
    )

    st.text_input(
        "Telefone"
    )

    st.text_input(
        "Email"
    )

    st.divider()

    # =========================
    # BACKUP
    # =========================

    st.subheader("💾 Backup")

    if st.button("Gerar Backup"):

        pasta = gerar_backup()

        st.success(
            f"Backup criado: {pasta}"
        )