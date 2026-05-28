import streamlit as st
import pandas as pd
import sqlite3
import bcrypt
import plotly.express as px
from datetime import datetime
import shutil

DB_NAME = "erp_v3.db"

# =========================================================
# CONEXÃO
# =========================================================
def conn():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

# =========================================================
# HELPERS
# =========================================================
@st.cache_data(ttl=60)
def query(sql, params=()):
    c = conn()
    try:
        return pd.read_sql_query(sql, c, params=params)
    finally:
        c.close()

def execute(sql, params=()):
    c = conn()
    cur = c.cursor()
    cur.execute(sql, params)
    c.commit()
    c.close()
    st.cache_data.clear()

def moeda(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def tabela(df):
    if df.empty:
        st.info("Sem dados disponíveis")
    else:
        st.dataframe(df, use_container_width=True, height=400)

def gerar_backup():
    nome = datetime.now().strftime('%Y%m%d_%H%M%S')
    caminho = f'backup_{nome}.db'
    shutil.copy(DB_NAME, caminho)

    with open(caminho, "rb") as f:
        st.download_button("📥 Baixar Backup", f, file_name=caminho)

# =========================================================
# LOGIN
# =========================================================
if 'logado' not in st.session_state:
    st.session_state.logado = False

if not st.session_state.logado:

    c1, c2, c3 = st.columns([1,1.2,1])

    with c2:
        st.title("🔐 ERP Pro Max")

        with st.form("login"):

            usuario = st.text_input("Usuário")
            senha = st.text_input("Senha", type="password")

            if st.form_submit_button("Entrar"):

                users = query(
                    "SELECT * FROM usuarios WHERE usuario=?",
                    (usuario,)
                )

                if not users.empty:
                    senha_hash = users.iloc[0]['senha']

                    if bcrypt.checkpw(senha.encode(), senha_hash.encode()):
                        st.session_state.logado = True
                        st.session_state.usuario = usuario
                        st.rerun()

                st.error("Usuário ou senha inválidos")

    st.stop()

# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:

    st.markdown("## 🍞 ERP Pro Max")
    st.write(f"👤 {st.session_state.usuario}")

    menu = st.radio(
        "Menu",
        [
            "📊 Dashboard",
            "📦 Produtos",
            "🧪 Receita Técnica",
            "🏭 Produção",
            "🛒 Vendas",
            "⚠️ Lista Compras",
            "💰 Financeiro",
            "🔐 Alterar Senha",
            "❓ Ajuda",
            "💾 Backup"
        ]
    )

    if st.button("🚪 Sair", use_container_width=True):
        st.session_state.logado = False
        st.rerun()

# =========================================================
# DASHBOARD (MELHORADO)
# =========================================================
if "Dashboard" in menu:

    st.title("📊 Dashboard")

    vendas = query("SELECT * FROM vendas")
    produtos = query("SELECT * FROM produtos")

    faturamento = vendas['total'].sum() if not vendas.empty else 0
    lucro = vendas['lucro'].sum() if not vendas.empty else 0

    estoque_baixo = query("""
        SELECT * FROM produtos
        WHERE estoque <= estoque_min
    """)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Faturamento", moeda(faturamento))
    c2.metric("Lucro", moeda(lucro))
    c3.metric("Produtos", len(produtos))
    c4.metric("Estoque Crítico", len(estoque_baixo))

    st.markdown("### ⚠️ Produtos com Estoque Crítico")

    if not estoque_baixo.empty:

        def highlight(row):
            if row["estoque"] == 0:
                return ['background-color: red; color: white'] * len(row)
            return ['background-color: #fff3cd'] * len(row)

        st.dataframe(
            estoque_baixo.style.apply(highlight, axis=1),
            use_container_width=True
        )

    if not vendas.empty:

        graf = vendas.groupby('data')['total'].sum().reset_index()

        fig = px.bar(graf, x='data', y='total')
        st.plotly_chart(fig, use_container_width=True)

# =========================================================
# PRODUTOS (MELHORADO)
# =========================================================
elif "Produtos" in menu:

    st.title("📦 Produtos")

    aba1, aba2 = st.tabs(["Cadastrar", "Listagem"])

    with aba1:
        with st.form("produto"):

            nome = st.text_input("Nome")
            tipo = st.selectbox("Tipo", ["Produto Final", "Matéria Prima"])
            unidade = st.selectbox("Unidade", ["UN", "KG", "L"])
            estoque = st.number_input("Estoque", min_value=0.0)
            estoque_min = st.number_input("Estoque Mínimo", min_value=0.0)
            custo = st.number_input("Custo", min_value=0.0)
            venda = st.number_input("Preço Venda", min_value=0.0)

            if st.form_submit_button("Salvar"):

                if not nome:
                    st.warning("Informe o nome")
                    st.stop()

                execute("""
                INSERT INTO produtos(nome,tipo,unidade,estoque,estoque_min,custo,venda)
                VALUES(?,?,?,?,?,?,?)
                """, (nome, tipo, unidade, estoque, estoque_min, custo, venda))

                st.success("Produto cadastrado")

    with aba2:
        produtos = query("SELECT * FROM produtos")
        tabela(produtos)

# =========================================================
# FINANCEIRO (MELHORADO)
# =========================================================
elif "Financeiro" in menu:

    st.title("💰 Financeiro")

    with st.form("financeiro"):

        tipo = st.selectbox("Tipo", ["Receita", "Despesa"])
        descricao = st.text_input("Descrição")
        valor = st.number_input("Valor", min_value=0.0)
        status = st.selectbox("Status", ["Pendente", "Pago"])

        if st.form_submit_button("Salvar"):

            execute("""
            INSERT INTO financeiro(tipo,descricao,valor,status)
            VALUES(?,?,?,?)
            """, (tipo, descricao, valor, status))

            st.success("Lançamento salvo")

    fin = query("SELECT * FROM financeiro")

    if not fin.empty:
        fin["valor"] = fin["valor"].apply(moeda)

    tabela(fin)

# =========================================================
# BACKUP (MELHORADO)
# =========================================================
elif "Backup" in menu:

    st.title("💾 Backup")

    if st.button("Gerar Backup"):
        gerar_backup()
