import streamlit as st
import pandas as pd
from database.db import query, execute


def show_financeiro():

    st.title("💰 Financeiro")

    # =========================
    # FORMULÁRIO
    # =========================

    with st.form("fin", clear_on_submit=True):

        tipo = st.selectbox(
            "Tipo",
            ["Entrada", "Saída"]
        )

        desc = st.text_input("Descrição")

        valor = st.number_input(
            "Valor",
            min_value=0.01,
            step=0.01
        )

        salvar = st.form_submit_button("Salvar")

        if salvar:

            if not desc:
                st.warning("Informe a descrição")
                st.stop()

            execute("""
            INSERT INTO financeiro(tipo, descricao, valor, status)
            VALUES(?,?,?,?)
            """, (tipo, desc, valor, "OK"))

            st.success("✅ Registrado")

    st.divider()

    # =========================
    # DADOS
    # =========================

    financeiro = query("SELECT * FROM financeiro")

    if financeiro.empty:
        st.info("Sem registros financeiros")
        return

    # =========================
    # KPIs (VISÃO GERENCIAL)
    # =========================

    entradas = financeiro[financeiro["tipo"] == "Entrada"]["valor"].sum()
    saidas = financeiro[financeiro["tipo"] == "Saída"]["valor"].sum()
    saldo = entradas - saidas

    c1, c2, c3 = st.columns(3)

    c1.metric("Entradas", f"R$ {entradas:,.2f}")
    c2.metric("Saídas", f"R$ {saidas:,.2f}")
    c3.metric("Saldo", f"R$ {saldo:,.2f}")

    st.divider()

    # =========================
    # FILTRO
    # =========================

    filtro_tipo = st.selectbox(
        "Filtrar",
        ["Todos", "Entrada", "Saída"]
    )

    if filtro_tipo != "Todos":
        financeiro = financeiro[
            financeiro["tipo"] == filtro_tipo
        ]

    # =========================
    # TABELA EDITÁVEL
    # =========================

    st.subheader("📋 Movimentações")

    edited_df = st.data_editor(
        financeiro,
        use_container_width=True,
        height=400
    )

    # =========================
    # SALVAR ALTERAÇÕES
    # =========================

    if st.button("💾 Salvar alterações"):

        for _, row in edited_df.iterrows():

            execute("""
            UPDATE financeiro
            SET tipo=?, descricao=?, valor=?, status=?
            WHERE id=?
            """, (
                row["tipo"],
                row["descricao"],
                row["valor"],
                row["status"],
                row["id"]
            ))

        st.success("✅ Alterações salvas")
        st.rerun()

    # =========================
    # EXCLUIR
    # =========================

    with st.expander("🗑️ Excluir lançamento"):

        id_del = st.selectbox(
            "Selecione",
            financeiro["id"]
        )

        if st.button("Excluir"):

            execute(
                "DELETE FROM financeiro WHERE id=?",
                (id_del,)
            )

            st.success("✅ Excluído")
            st.rerun()
