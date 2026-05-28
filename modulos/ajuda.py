import streamlit as st


def show_ajuda():

    st.title("📚 Central de Ajuda ERP PRO MAX")

    st.info("Manual completo de utilização do sistema")

    # =========================
    # NAVEGAÇÃO RÁPIDA
    # =========================

    st.markdown("""
    ### 🚀 Navegação rápida

    1. Cadastre produtos  
    2. Crie receitas  
    3. Produza itens  
    4. Realize vendas  
    5. Controle financeiro  
    """)

    abas = st.tabs([
        "📦 Produtos",
        "🧪 Receitas",
        "🏭 Produção",
        "🛒 Vendas",
        "💰 Financeiro",
        "💾 Backup",
        "⚠️ Erros Comuns",
        "✅ Boas Práticas"
    ])

    # =========================
    # PRODUTOS
    # =========================

    with abas[0]:

        st.header("📦 Cadastro de Produtos")

        st.markdown("""
        ### Tipos de produto
        - Matéria Prima
        - Produto Final

        ### Exemplos
        Farinha → Matéria Prima  
        Bolo → Produto Final
        """)

        st.divider()

        st.subheader("📏 Quantidade")

        st.markdown("""
        O sistema trabalha conforme a unidade cadastrada.

        #### KG
        - 0.01 = 10g
        - 0.1 = 100g
        - 1 = 1kg

        #### UN
        - 1 = 1 unidade
        - 10 = 10 unidades

        #### Litro
        - 0.5 = meio litro
        """)

        st.warning("⚠️ Sempre usar a mesma unidade para evitar erro de estoque")

        st.divider()

        st.subheader("💰 Custos")

        st.markdown("""
        - Custo = valor pago
        - Venda = preço vendido

        ✔ Lucro é calculado automaticamente
        """)

    # =========================
    # RECEITAS
    # =========================

    with abas[1]:

        st.header("🧪 Receitas")

        st.markdown("""
        Define quanto de matéria-prima será consumida.

        ✔ Ligação entre produto final e insumos
        """)

        st.info("""
        Produção automática:
        ✔ soma produto final  
        ✔ reduz matéria-prima  
        """)

    # =========================
    # PRODUÇÃO
    # =========================

    with abas[2]:

        st.header("🏭 Produção")

        st.markdown("""
        Transforma matéria-prima em produto final.
        """)

        st.warning("""
        ⚠️ Não produza sem estoque suficiente!
        """)

    # =========================
    # VENDAS
    # =========================

    with abas[3]:

        st.header("🛒 Vendas")

        st.markdown("""
        ✔ baixa estoque  
        ✔ calcula lucro  
        ✔ gera financeiro  
        """)

    # =========================
    # FINANCEIRO
    # =========================

    with abas[4]:

        st.header("💰 Financeiro")

        st.markdown("""
        Controle completo de caixa.
        """)

        st.success("""
        O sistema calcula automaticamente:
        ✔ saldo  
        ✔ lucro  
        ✔ despesas  
        """)

    # =========================
    # BACKUP
    # =========================

    with abas[5]:

        st.header("💾 Backup")

        st.markdown("""
        Cria cópia de segurança da base de dados.
        """)

        st.warning("""
        Gere backup:
        - diariamente  
        - antes de alterações  
        """)

    # =========================
    # ERROS COMUNS
    # =========================

    with abas[6]:

        st.header("⚠️ Erros Comuns")

        st.markdown("""
        ❌ Produto não aparece na receita  
        ✔ Verifique o tipo (Produto Final / Matéria Prima)

        ❌ Estoque negativo  
        ✔ Falta controle de produção ou venda

        ❌ Não consegue logar  
        ✔ Verifique usuário e senha

        ❌ Dados somem  
        ✔ Necessidade de backup

        ❌ Receita não funciona  
        ✔ Produto não vinculado corretamente
        """)

    # =========================
    # BOAS PRÁTICAS
    # =========================

    with abas[7]:

        st.header("✅ Boas Práticas")

        st.markdown("""
        ✔ Use nomes padronizados (ex: Farinha KG)  
        ✔ Não misture unidades (KG com UN)  
        ✔ Cadastre custo real  
        ✔ Faça backup diário  
        ✔ Evite duplicar produtos  
        ✔ Valide estoque antes da produção  

        ### 💡 Uso profissional

        - Use o sistema diariamente  
        - Faça conferência semanal  
        - Controle entradas e saídas  
        - Analise lucro constantemente  
        """)

        st.success("✅ Seguindo isso, seu ERP funciona como sistema profissional")

