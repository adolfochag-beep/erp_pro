import streamlit as st

def show_ajuda():

    st.title("❓ Central de Ajuda")

    st.markdown("""
    ## Como usar o sistema

    ### 📦 Produtos
    Cadastre:
    - matéria-prima
    - produtos finais

    ---

    ### 📚 Receitas
    Vincule:
    - produto final
    - ingredientes

    ---

    ### 🏭 Produção
    Produza itens automaticamente:
    - desconta matéria-prima
    - adiciona produto final

    ---

    ### 🛒 Vendas
    Registra vendas e baixa estoque.

    ---

    ### ⚠️ Compras
    Mostra itens abaixo do estoque mínimo.

    ---
    """)