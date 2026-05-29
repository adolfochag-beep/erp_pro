import streamlit as st


def show_ajuda():

    st.title("📚 Central de Ajuda ERP PRO MAX")

    st.info("Manual completo de utilização do sistema")

    st.markdown("""
    ### 🚀 Navegação rápida

    1. Cadastre produtos  
    2. Crie receitas (BOM)  
    3. Produza itens  
    4. Realize vendas  
    5. Controle financeiro  
    """)

    abas = st.tabs([
        "📦 Produtos",
        "🧪 Receitas (BOM)",
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

        - **Matéria Prima** → recebe custo manual  
        - **Produto Final** → custo calculado automaticamente pela Receita

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
        """)

        st.warning("⚠️ Não misture unidades (ex: KG com UN)")

        st.divider()

        st.subheader("💰 Custos")

        st.markdown("""
        ✅ **Matéria‑prima**: custo digitado manualmente  
        ✅ **Produto final**: custo **calculado automaticamente pela Receita**

        O custo do produto final é:
        > Soma das matérias‑primas × quantidades definidas na Receita
        """)

    # =========================
    # RECEITAS
    # =========================
    with abas[1]:

        st.header("🧪 Receitas (BOM)")

        st.markdown("""
        Receita (BOM – Bill of Materials) define **como um produto é produzido**.

        Ela informa:
        - Qual produto final será produzido
        - Quais matérias‑primas serão consumidas
        - Em qual quantidade
        """)

        st.subheader("📌 Exemplo")

        st.markdown("""
        Produto Final: Bolo  

        Matérias‑primas:
        - 0,20 kg Farinha  
        - 0,10 kg Açúcar  
        - 3 UN Ovos  
        """)

        st.info("""
        ✅ Sempre que a Receita é criada, alterada ou excluída:
        - o custo do produto final é recalculado automaticamente
        """)

    # =========================
    # PRODUÇÃO
    # =========================
    with abas[2]:

        st.header("🏭 Produção")

        st.markdown("""
        A produção transforma matéria‑prima em produto final com base na Receita.
        """)

        st.markdown("""
        Quando você produz:
        ✔ baixa matéria‑prima  
        ✔ aumenta estoque do produto final  
        ✔ utiliza o custo calculado pela Receita  
        """)

        st.warning("⚠️ Se faltar matéria‑prima, a produção não deve ser realizada")

    # =========================
    # VENDAS
    # =========================
    with abas[3]:

        st.header("🛒 Vendas")

        st.markdown("""
        O módulo de vendas:
        ✔ baixa estoque  
        ✔ calcula lucro automaticamente  
        ✔ usa o custo real do produto  
        ✔ registra histórico  
        """)

    # =========================
    # FINANCEIRO
    # =========================
    with abas[4]:

        st.header("💰 Financeiro")

        st.markdown("""
        Controle completo de entradas e saídas.
        """)

        st.success("""
        O sistema apresenta:
        ✔ saldo  
        ✔ lucro real  
        ✔ despesas  
        ✔ fluxo de caixa  
        """)

    # =========================
    # BACKUP
    # =========================
    with abas[5]:

        st.header("💾 Backup")

        st.markdown("""
        Backup cria uma cópia de segurança do banco de dados.
        """)

        st.warning("""
        Gere backup:
        - diariamente  
        - antes de alterações importantes  
        - antes de atualizar o sistema  
        """)

    # =========================
    # ERROS COMUNS
    # =========================
    with abas[6]:

        st.header("⚠️ Erros Comuns")

        st.markdown("""
        ❌ Produto final sem custo  
        ✔ Verifique se existe Receita cadastrada

        ❌ Estoque negativo  
        ✔ Falta controle de produção ou venda

        ❌ Receita não recalcula custo  
        ✔ Verifique se matéria‑prima possui custo

        ❌ Produto não aparece na Receita  
        ✔ Verifique o tipo do produto
        """)

    # =========================
    # BOAS PRÁTICAS
    # =========================
    with abas[7]:

        st.header("✅ Boas Práticas")

        st.markdown("""
        ✔ Cadastre primeiro matérias‑primas  
        ✔ Informe custo real das matérias‑primas  
        ✔ Sempre crie Receita antes de produzir  
        ✔ Não altere custo manualmente do produto final  
        ✔ Faça backup diário  
        ✔ Analise lucro com frequência  

        ### 💡 Uso profissional
        - Receita é a base do custo  
        - Produção é o consumo  
        - Venda usa custo real  
        """)

        st.success("✅ Seguindo isso, seu ERP funciona como sistema profissional")
