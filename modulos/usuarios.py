import streamlit as st
import pandas as pd
import sqlite3
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
# FUNÇÃO PRINCIPAL DO MÓDULO
# =========================================================
def show_usuarios():

    st.title("👥 Gestão Geral")

    aba1, aba2, aba3, aba4 = st.tabs([
        "📊 Dashboard",
        "📦 Produtos",
        "💰 Financeiro",
        "💾 Backup"
    ])

    # =========================
    # DASHBOARD
    # =========================
    with aba1:

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

        if not estoque_baixo.empty:
            st.dataframe(estoque_baixo, use_container_width=True)

    # =========================
    # PRODUTOS
    # =========================
    with aba2:

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
                    return

                execute("""
                INSERT INTO produtos(nome,tipo,unidade,estoque,estoque_min,custo,venda)
                VALUES(?,?,?,?,?,?,?)
                """, (nome, tipo, unidade, estoque, estoque_min, custo, venda))

                st.success("Produto cadastrado")

        tabela(query("SELECT * FROM produtos"))

    # =========================
    # FINANCEIRO
    # =========================
    with aba3:

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

        tabela(query("SELECT * FROM financeiro"))

    # =========================
    # BACKUP
    # =========================
    with aba4:

        if st.button("Gerar Backup"):
            gerar_backup()
