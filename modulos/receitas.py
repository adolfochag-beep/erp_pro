import streamlit as st
import pandas as pd
from database.db import query, execute


def show_receitas():

    st.title("📚 Receitas (Produto → Matéria Prima)")

    # =========================
    # DADOS
    # =========================

    produtos = query("SELECT * FROM produtos")

    if produtos.empty:
        st.warning("Cadastre produtos primeiro")
        return

    # ✅ normaliza (evita erro de texto)
    produtos["tipo"] = produtos["tipo"].str.lower().str.strip()

    produtos_finais = produtos[produtos["tipo"] == "produto final"]
    materias_primas = produtos[produtos["tipo"] == "matéria prima"]

    if produtos_finais.empty or materias_primas.empty:
        st.warning("Precisa ter Produto Final e Matéria Prima cadastrados")
        return

    # =========================
    # FORMULÁRIO
    # =========================

    with st.form("receita", clear_on_submit=True):

        produto_final_nome = st.selectbox(
            "Produto Final",
            produtos_finais["nome"]
        )

        materia_prima_nome = st.selectbox(
            "Matéria Prima",
            materias_primas["nome"]
        )

        qtd = st.number_input(
            "Quantidade por unidade",
            min_value=0.01,
            step=0.01
        )

        salvar = st.form_submit_button("Adicionar Receita")

        if salvar:

            # ✅ seguro (não quebra mais)
            pf = produtos_finais[
                produtos_finais["nome"] == produto_final_nome
            ]

            mp = materias_primas[
                materias_primas["nome"] == materia_prima_nome
            ]

            if pf.empty or mp.empty:
                st.error("Erro ao localizar produtos")
                return

            pf_id = int(pf.iloc[0]["id"])
            mp_id = int(mp.iloc[0]["id"])

            # ✅ evita duplicidade
            existe = query("""
                SELECT * FROM receitas
                WHERE produto_final=? AND materia_prima=?
            """, (pf_id, mp_id))

            if not existe.empty:
                st.warning("Essa receita já existe")
            else:
                execute("""
                INSERT INTO receitas(produto_final, materia_prima, quantidade)
                VALUES(?,?,?)
                """, (pf_id, mp_id, qtd))

                st.success("✅ Receita adicionada")

    st.divider()

    # =========================
    # LISTAGEM
    # =========================

    receitas = query("""
        SELECT 
            r.id,
            p1.nome as produto_final,
            p2.nome as materia_prima,
            r.quantidade
        FROM receitas r
        LEFT JOIN produtos p1 ON r.produto_final = p1.id
        LEFT JOIN produtos p2 ON r.materia_prima = p2.id
    """)

    if receitas.empty:
        st.info("Nenhuma receita cadastrada")
        return

    st.subheader("📋 Estrutura das Receitas")

    # =========================
    # TABELA EDITÁVEL
    # =========================

    editado = st.data_editor(
        receitas,
        use_container_width=True,
        height=400
    )

    # =========================
    # SALVAR ALTERAÇÕES
    # =========================

    if st.button("💾 Salvar alterações"):

        for _, row in editado.iterrows():

            # protege erro se nome mudar
            pf = query(
                "SELECT id FROM produtos WHERE nome=?",
                (row["produto_final"],)
            )

            mp = query(
                "SELECT id FROM produtos WHERE nome=?",
                (row["materia_prima"],)
            )

            if pf.empty or mp.empty:
                continue

            execute("""
            UPDATE receitas
            SET produto_final=?, materia_prima=?, quantidade=?
            WHERE id=?
            """, (
                int(pf.iloc[0]["id"]),
                int(mp.iloc[0]["id"]),
                row["quantidade"],
                row["id"]
            ))

        st.success("✅ Alterações salvas")
        st.rerun()

    # =========================
    # EXCLUSÃO
    # =========================

    with st.expander("🗑️ Excluir receita"):

        id_excluir = st.selectbox(
            "Selecione a receita",
            receitas["id"]
        )

        if st.button("Excluir receita"):

            execute(
                "DELETE FROM receitas WHERE id=?",
                (id_excluir,)
            )

            st.success("✅ Receita excluída")
            st.rerun()
