import streamlit as st
from database.db import query, execute, recalcular_custo_produto


def show_receitas():

    st.title("📚 Receitas (BOM)")

    produtos = query("SELECT * FROM produtos")

    produtos["tipo"] = produtos["tipo"].str.lower()

    finais = produtos[produtos["tipo"] == "produto final"]
    materias = produtos[produtos["tipo"] == "matéria prima"]

    with st.form("receita", clear_on_submit=True):

        pf_nome = st.selectbox("Produto Final", finais["nome"])
        mp_nome = st.selectbox("Matéria Prima", materias["nome"])
        qtd = st.number_input("Quantidade", min_value=0.01)

        if st.form_submit_button("Adicionar"):

            pf_id = finais[finais["nome"] == pf_nome].iloc[0]["id"]
            mp_id = materias[materias["nome"] == mp_nome].iloc[0]["id"]

            execute("""
                INSERT INTO receitas(produto_final, materia_prima, quantidade)
                VALUES(?,?,?)
            """, (pf_id, mp_id, qtd))

            # ✅ recalcula custo automaticamente
            recalcular_custo_produto(pf_id)

            st.success("✅ Receita adicionada")

    st.divider()

    receitas = query("""
        SELECT r.id, p1.nome produto_final, p2.nome materia_prima, r.quantidade
        FROM receitas r
        JOIN produtos p1 ON r.produto_final = p1.id
        JOIN produtos p2 ON r.materia_prima = p2.id
    """)

    st.dataframe(receitas, use_container_width=True)
