import streamlit as st
from database.db import query, execute, recalcular_custo_produto


def show_receitas():

    st.title("📚 Receitas (BOM)")

    produtos = query("SELECT * FROM produtos")

    if produtos.empty:
        st.warning("Cadastre produtos primeiro")
        return

    # normaliza tipo
    produtos["tipo"] = (
        produtos["tipo"]
        .str.lower()
        .str.normalize("NFKD")
        .str.encode("ascii", errors="ignore")
        .str.decode("utf-8")
    )

    finais = produtos[produtos["tipo"] == "produto final"]
    materias = produtos[produtos["tipo"] == "materia prima"]

    if finais.empty or materias.empty:
        st.warning("Necessario cadastrar Produto Final e Materia Prima")
        return

    # =========================
    # FORMULÁRIO
    # =========================
    with st.form("receita", clear_on_submit=True):

        pf_nome = st.selectbox("Produto Final", finais["nome"])
        mp_nome = st.selectbox("Materia Prima", materias["nome"])

        qtd = st.number_input(
            "Quantidade por unidade",
            min_value=0.01,
            step=0.01
        )

        if st.form_submit_button("Adicionar Receita"):

            pf_id = finais[finais["nome"] == pf_nome].iloc[0]["id"]
            mp_id = materias[materias["nome"] == mp_nome].iloc[0]["id"]

            execute("""
                INSERT INTO receitas(produto_final, materia_prima, quantidade)
                VALUES(?,?,?)
            """, (pf_id, mp_id, qtd))

            recalcular_custo_produto(pf_id)

            st.success("✅ Receita adicionada")

    st.divider()

    # =========================
    # LISTAGEM
    # =========================
    receitas = query("""
        SELECT
            r.id,
            p1.nome AS produto_final,
            p2.nome AS materia_prima,
            r.quantidade
        FROM receitas r
        LEFT JOIN produtos p1 ON r.produto_final = p1.id
        LEFT JOIN produtos p2 ON r.materia_prima = p2.id
        ORDER BY r.id DESC
    """)

    if receitas.empty:
        st.info("Nenhuma receita cadastrada")
        return

    st.dataframe(receitas, use_container_width=True, height=400)
