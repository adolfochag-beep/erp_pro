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

        if st.form_submit_button("Adicionar Receita"):

            pf_id = int(
                finais.loc[finais["nome"] == pf_nome, "id"].iloc[0]
            )

            mp_id = int(
                materias.loc[materias["nome"] == mp_nome, "id"].iloc[0]
            )

            # Evita duplicidade
            existe = query("""
                SELECT 1
                FROM receitas
                WHERE produto_final = ?
                  AND materia_prima = ?
            """, (pf_id, mp_id))

            if not existe.empty:
                st.warning("Essa matéria-prima já existe nessa receita.")
                return

            execute("""
                INSERT INTO receitas (
                    produto_final,
                    materia_prima,
                    quantidade
                )
                VALUES (?, ?, ?)
            """, (pf_id, mp_id, qtd))

            recalcular_custo_produto(pf_id)

            st.success("✅ Receita adicionada com sucesso")

    st.divider()

    # =========================
    # LISTAGEM (ROBUSTA)
    # =========================
    receitas = query("""
        SELECT
            r.id,
            COALESCE(pf.nome, 'Produto não encontrado') AS produto_final,
            COALESCE(mp.nome, 'Matéria-prima não encontrada') AS materia_prima,
            r.quantidade
        FROM receitas r
        LEFT JOIN produtos pf
            ON CAST(r.produto_final AS INTEGER) = pf.id
        LEFT JOIN produtos mp
            ON CAST(r.materia_prima AS INTEGER) = mp.id
        ORDER BY r.id DESC
    """)

    if receitas.empty:
        st.info("Nenhuma receita cadastrada")
        return

    receitas_exibir = receitas.rename(columns={
        "id": "ID",
        "produto_final": "Produto Final",
        "materia_prima": "Matéria Prima",
        "quantidade": "Quantidade"
    })

    st.dataframe(
        receitas_exibir,
        use_container_width=True,
        height=400,
        hide_index=True
    )
