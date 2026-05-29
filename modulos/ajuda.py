import streamlit as st


def show_ajuda():

    st.title("📚 Central de Ajuda ERP PRO MAX")

    st.info("Manual completo de utilizacao do sistema")

    st.markdown("""
    ### 🚀 Navegacao rapida

    1. Cadastre produtos  
    2. Crie receitas (BOM)  
    3. Produza itens  
    4. Realize vendas  
    5. Controle financeiro  
    """)

    abas = st.tabs([
        "📦 Produtos",
        "🧪 Receitas (BOM)",
        "🏭 Producao",
        "🛒 Vendas",
        "💰 Financeiro",
        "💾 Backup",
        "⚠️ Erros Comuns",
        "✅ Boas Praticas"
    ])

    # =========================
    # PRODUTOS
    # =========================
    with abas[0]:

        st.header("📦 Cadastro de Produtos")

        st.markdown("""
        ### Tipos de produto

        - **Materia Prima** → recebe custo manual  
        - **Produto Final** → custo calculado automaticamente pela Receita

        ### Exemplos
        Farinha → Materia Prima  
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

        st.warning("⚠️ Nao misture unidades (ex: KG com UN)")

        st.divider()

        st.subheader("💰 Custos")

        st.markdown("""
        ✅ **Materia-prima**: custo digitado manualmente  
        ✅ **Produto final**: custo calculado automaticamente pela Receita

        > **Custo do produto final** =  
        > Soma das materias-primas × quantidades definidas na Receita
        """)

    # =========================
    # RECEITAS
    # =========================
    with abas[1]:

        st.header("🧪 Receitas (BOM)")

        st.markdown("""
        Receita (BOM - Bill of Materials) define como um produto e produzido.

        Ela informa:
        - Qual produto final sera produzido
        - Quais materias-primas serao consumidas
        - Em qual quantidade
        """)

        st.subheader("📌 Exemplo")

        st.markdown("""
        Produto Final: Bolo

        Materias-primas:
        - 0.20 kg Farinha
        - 0.10 kg Acucar
        - 3 UN Ovos
        """)

        st.info(
            "✅ Sempre que a Receita e criada, alterada ou excluida, "
            "o custo do produto final e recalculado automaticamente."
        )

    # =========================
    # PRODUCAO
    # =========================
    with abas[2]:

        st.header("🏭 Producao")

        st.markdown("""
        A producao transforma materia-prima em produto final com base na Receita.
        """)

        st.markdown("""
        Quando voce produz:
        ✔ baixa materia-prima  
        ✔ aumenta estoque do produto final  
        ✔ utiliza o custo calculado pela Receita  
        """)

        st.warning("⚠️ Se faltar materia-prima, a producao nao deve ser realizada")

    # =========================
    # VENDAS
    # =========================
    with abas[3]:

        st.header("🛒 Vendas")

        st.markdown("""
        O modulo de vendas:
        ✔ baixa estoque  
        ✔ calcula lucro com custo real  
        ✔ gera lancamento automatico no financeiro  
        ✔ registra cliente e forma de pagamento  
        """)

        st.markdown("""
        ### Pagamento
        - **Pago** → entrada imediata no financeiro  
        - **Pendente** → conta a receber  
        """)

    # =========================
    # FINANCEIRO
    # =========================
    with abas[4]:

        st.header("💰 Financeiro")

        st.markdown("""
        Controle completo de entradas e saidas.
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
        Backup cria uma copia de seguranca do banco de dados.
        """)

        st.warning("""
        Gere backup:
        - diariamente  
        - antes de alteracoes importantes  
        - antes de atualizar o sistema  
        """)

    # =========================
    # ERROS COMUNS
    # =========================
    with abas[6]:

        st.header("⚠️ Erros Comuns")

        st.markdown("""
        ❌ Produto final com custo zero  
        ✔ Verifique se existe Receita cadastrada

        ❌ Estoque negativo  
        ✔ Falta controle de producao ou venda

        ❌ Receita nao recalcula custo  
        ✔ Verifique se materia-prima possui custo

        ❌ Venda nao aparece no financeiro  
        ✔ Verifique o status do pagamento
        """)

    # =========================
    # BOAS PRATICAS
    # =========================
    with abas[7]:

        st.header("✅ Boas Praticas")

        st.markdown("""
        ✔ Cadastre primeiro materias-primas  
        ✔ Informe custo real das materias-primas  
        ✔ Sempre crie Receita antes de produzir  
        ✔ Nao altere custo manualmente do produto final  
        ✔ Faca backup diario  
        ✔ Analise lucro com frequencia  

        ### 💡 Uso profissional
        - Receita e a base do custo  
        - Producao e o consumo  
        - Venda usa custo real  
        """)

        st.success("✅ Seguindo isso, seu ERP funciona como sistema profissional")

