import streamlit as st
from database.db import query, execute, recalcular_custo_produto


def show_receitas():

    st.title("📚 Receitas (BOM)")

    produtos = query("SELECT * FROM produtos")

    if produtos.empty:
        st.warning("Cadastre produtos primeiro")
        return

    # =========================
    # NORMALIZA TIPO
    # =========================
    produtos["tipo"] = (
        produtos["tipo"]
        .astype(str)
        .str.lower()
        .str.normalize("NFKD")
        .str.encode("ascii", errors="ignore")
        .str.decode("utf-8")
    )

    finais = produtos[produtos["tipo"] == "produto final"]
    materias = produtos[produtos["tipo"] == "materia prima"]

    if finais.empty or materias.empty:
        st.warning("Necessário cadastrar Produto Final e Matéria Prima")
        return

    # =========================
    # FORMULÁRIO
    # =========================
    with st.form("receita", clear_on_submit=True):

        pf_nome = st.selectbox(
            "Produto Final",
            finais["nome"].tolist()
        )

        mp_nome = st.selectbox(
            "Matéria Prima",
            materias["nome"].tolist()
        )

        qtd = st.number_input(
            "Quantidade por unidade",
            min_value=0.01,
            step=0.01,
            format="%.2f"
        )

        submitted = st.form_submit_button("Adicionar Receita")

        if submitted:

            pf_id = finais.loc[
                finais["nome"] == pf_nome, "id"
            ].values[0]

            mp_id = materias.loc[
                materias["nome"] == mp_nome, "id"
            ].values[0]

            # Evita duplicidade
            existe = query("""
                SELECT *
                FROM receitas
                WHERE produto_final = ?
                AND materia_prima = ?
            """, (pf_id, mp_id))

            if not existe.empty:
                st.warning("Essa matéria-prima já foi adicionada nessa receita.")
                return

            execute("""
                INSERT INTO receitas (
                    produto_final,
                    materia_prima,
                    quantidade
                )
                VALUES (?, ?, ?)
            """, (pf_id, mp_id, qtd))

            # Recalcula custo automaticamente
            recalcular_custo_produto(pf_id)

            st.success("✅ Receita adicionada com sucesso")

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
        LEFT JOIN produtos p1
            ON r.produto_final = p1.id
        LEFT JOIN produtos p2
            ON r.materia_prima = p2.id
        ORDER BY r.id DESC
    """)

    if receitas.empty:
        st.info("Nenhuma receita cadastrada")
        return

    # =========================
    # RENOMEIA COLUNAS
    # =========================
    receitas_exibir = receitas.rename(columns={
        "id": "ID",
        "produto_final": "Produto Final",
        "materia_prima": "Matéria Prima",
        "quantidade": "Quantidade"
    })

    # =========================
    # TABELA
    # =========================
    st.dataframe(
        receitas_exibir,
        use_container_width=True,
        height=400,
        hide_index=True
    )
