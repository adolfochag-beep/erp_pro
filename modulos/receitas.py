import streamlit as st
from database.db import query, execute, recalcular_custo_produto

def show_receitas():

    st.subheader("📚 Receitas (BOM)")

    produtos = query("SELECT * FROM produtos")

    produtos["tipo"] = (
        produtos["tipo"]
        .str.lower()
        .str.normalize("NFKD")
        .str.encode("ascii", errors="ignore")
        .str.decode("utf-8")
    )

    finais = produtos[produtos["tipo"] == "produto final"]
    materias = produtos[produtos["tipo"] == "materia prima"]

    with st.form("receita", clear_on_submit=True):

        pf = st.selectbox("Produto Final", finais["nome"])
        mp = st.selectbox("Matéria Prima", materias["nome"])
        qtd = st.number_input("Quantidade", min_value=0.01)

        if st.form_submit_button("Adicionar"):
            pf_id = int(finais[finais["nome"] == pf]["id"].iloc[0])
            mp_id = int(materias[materias["nome"] == mp]["id"].iloc[0])

            execute("""
                INSERT INTO receitas(produto_final, materia_prima, quantidade)
                VALUES(?,?,?)
            """, (pf_id, mp_id, qtd))

            recalcular_custo_produto(pf_id)
            st.success("✅ Receita cadastrada")

    st.divider()
    st.dataframe(query("""
        SELECT r.id, pf.nome produto_final, mp.nome materia_prima, r.quantidade
        FROM receitas r
        LEFT JOIN produtos pf ON r.produto_final = pf.id
        LEFT JOIN produtos mp ON r.materia_prima = mp.id
    """), use_container_width=True)
