import streamlit as st


def show_ajuda():

    st.title("📚 Central de Ajuda ERP PRO MAX")

    st.info(
        "Manual completo de utilização do sistema"
    )

    abas = st.tabs([
        "📦 Produtos",
        "🧪 Receitas",
        "🏭 Produção",
        "🛒 Vendas",
        "💰 Financeiro",
        "💾 Backup"
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

        ### Exemplos:

        #### Unidade = KG

        - 0.01 = 10g
        - 0.02 = 20g
        - 0.1 = 100g
        - 1 = 1kg
        - 2 = 2kg

        #### Unidade = UN

        - 1 = 1 unidade
        - 10 = 10 unidades
        - 200 = 200 unidades

        #### Unidade = Litro

        - 0.5 = meio litro
        - 1 = 1 litro
        """)

        st.warning("""
        ⚠️ Use sempre o mesmo padrão de unidade
        para evitar erros de estoque.
        """)

        st.divider()

        st.subheader("💰 Custos")

        st.markdown("""
        - Custo = valor pago
        - Venda = preço vendido

        O sistema calcula lucro automaticamente.
        """)

    # =========================
    # RECEITAS
    # =========================

    with abas[1]:

        st.header("🧪 Receitas")

        st.markdown("""
        As receitas definem quanto de matéria-prima
        será consumida na produção.
        """)

        st.subheader("📌 Exemplo")

        st.markdown("""
        Produto Final:
        - Bolo Chocolate

        Matérias-primas:
        - 0.2 kg farinha
        - 0.1 kg açúcar
        - 3 ovos
        """)

        st.info("""
        Ao produzir:
        ✔ estoque do produto final aumenta
        ✔ matéria-prima reduz automaticamente
        """)

    # =========================
    # PRODUÇÃO
    # =========================

    with abas[2]:

        st.header("🏭 Produção")

        st.markdown("""
        O módulo produção transforma matéria-prima
        em produto final.
        """)

        st.subheader("🔄 O que acontece")

        st.markdown("""
        Quando uma produção é registrada:

        ✔ baixa matéria-prima  
        ✔ aumenta produto final  
        ✔ registra custo  
        """)

        st.warning("""
        ⚠️ Se faltar matéria-prima,
        a produção não deve ser realizada.
        """)

    # =========================
    # VENDAS
    # =========================

    with abas[3]:

        st.header("🛒 Vendas")

        st.markdown("""
        O módulo vendas:

        ✔ baixa estoque  
        ✔ calcula lucro  
        ✔ registra venda  
        ✔ alimenta financeiro  
        """)

        st.subheader("📌 Exemplo")

        st.markdown("""
        Venda:
        - 2 bolos
        - valor R$ 80

        O ERP:
        - reduz estoque
        - calcula lucro
        - gera entrada financeira
        """)

    # =========================
    # FINANCEIRO
    # =========================

    with abas[4]:

        st.header("💰 Financeiro")

        st.markdown("""
        O financeiro controla entradas e saídas.
        """)

        st.subheader("✅ Entradas")

        st.markdown("""
        - vendas
        - recebimentos
        - depósitos
        """)

        st.subheader("❌ Saídas")

        st.markdown("""
        - aluguel
        - energia
        - fornecedores
        - salários
        - impostos
        """)

        st.info("""
        O financeiro mostra:
        ✔ lucro
        ✔ despesas
        ✔ fluxo de caixa
        ✔ saldo
        """)

    # =========================
    # BACKUP
    # =========================

    with abas[5]:

        st.header("💾 Backup")

        st.markdown("""
        O backup cria uma cópia de segurança
        do sistema.
        """)

        st.subheader("📌 Recomendação")

        st.markdown("""
        Gere backup:
        - diariamente
        - antes de grandes alterações
        - antes de atualizar o sistema
        """)

        st.success("""
        Os backups ficam salvos na pasta:
        backups/
        """)
