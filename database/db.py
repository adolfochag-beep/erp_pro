import sqlite3
import pandas as pd
import streamlit as st
import bcrypt

DB_NAME = "erp_v3.db"

# =========================================================
# CONEXÃO SEGURA
# =========================================================
def conn():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

# =========================================================
# QUERY (COM PROTEÇÃO)
# =========================================================
@st.cache_data(ttl=60)
def query(sql, params=()):

    try:
        c = conn()
        df = pd.read_sql_query(sql, c, params=params)
        c.close()
        return df

    except Exception as e:
        # 👇 evita quebrar app
        st.error("Erro ao consultar banco")
        return pd.DataFrame()

# =========================================================
# EXECUTE
# =========================================================
def execute(sql, params=()):

    try:
        c = conn()
        cur = c.cursor()
        cur.execute(sql, params)
        c.commit()
        c.close()

        st.cache_data.clear()

    except Exception as e:
        st.error("Erro ao executar operação")


# =========================================================
# CRIAR TABELAS
# =========================================================
def init_db():

    c = conn()
    cur = c.cursor()

    # ✅ USUÁRIOS
    cur.execute("""
    CREATE TABLE IF NOT EXISTS usuarios(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT UNIQUE,
        senha TEXT,
        cargo TEXT
    )
    """)

    # ✅ PRODUTOS
    cur.execute("""
    CREATE TABLE IF NOT EXISTS produtos(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        tipo TEXT,
        unidade TEXT,
        estoque REAL,
        estoque_min REAL,
        custo REAL,
        venda REAL
    )
    """)

    # ✅ RECEITAS
    cur.execute("""
    CREATE TABLE IF NOT EXISTS receitas(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        produto_final INTEGER,
        materia_prima INTEGER,
        quantidade REAL
    )
    """)

    # ✅ PRODUÇÃO
    cur.execute("""
    CREATE TABLE IF NOT EXISTS producoes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        produto_final INTEGER,
        quantidade REAL,
        custo REAL,
        data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # ✅ VENDAS
    cur.execute("""
    CREATE TABLE IF NOT EXISTS vendas(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        produto TEXT,
        quantidade REAL,
        total REAL,
        lucro REAL,
        data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # ✅ FINANCEIRO
    cur.execute("""
    CREATE TABLE IF NOT EXISTS financeiro(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo TEXT,
        descricao TEXT,
        valor REAL,
        status TEXT,
        data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    c.commit()
    c.close()


# =========================================================
# GARANTIR ADMIN
# =========================================================
def init_users():

    c = conn()
    cur = c.cursor()

    cur.execute("SELECT * FROM usuarios WHERE usuario='admin'")
    user = cur.fetchone()

    if not user:
        senha = bcrypt.hashpw(
            "123456".encode(),
            bcrypt.gensalt()
        ).decode()

        cur.execute("""
        INSERT INTO usuarios(usuario, senha, cargo)
        VALUES(?,?,?)
        """, ("admin", senha, "ADMIN"))

    c.commit()
    c.close()
``
