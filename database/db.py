import sqlite3
import pandas as pd
import streamlit as st
import os
import bcrypt

# =========================
# PASTA DATABASES
# =========================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DATABASE_DIR = os.path.join(
    BASE_DIR,
    "databases"
)

os.makedirs(
    DATABASE_DIR,
    exist_ok=True
)

# =========================
# BANCO CENTRAL USUÁRIOS
# =========================

USERS_DB = os.path.join(
    DATABASE_DIR,
    "usuarios.db"
)

def users_conn():

    return sqlite3.connect(
        USERS_DB,
        check_same_thread=False
    )

# =========================
# BANCO EMPRESA
# =========================

def get_user_db():

    usuario = st.session_state.get(
        "usuario",
        "default"
    )

    return os.path.join(
        DATABASE_DIR,
        f"{usuario}.db"
    )

def conn():

    return sqlite3.connect(
        get_user_db(),
        check_same_thread=False
    )

# =========================
# QUERY
# =========================

@st.cache_data(ttl=60)
def query(sql, params=()):

    try:

        c = conn()

        df = pd.read_sql_query(
            sql,
            c,
            params=params
        )

        c.close()

        return df

    except:

        return pd.DataFrame()

# =========================
# EXECUTE
# =========================

def execute(sql, params=()):

    c = conn()

    cur = c.cursor()

    cur.execute(
        sql,
        params
    )

    c.commit()

    c.close()

    st.cache_data.clear()

# =========================
# INIT USERS
# =========================

def init_users():

    c = users_conn()

    cur = c.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS usuarios(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT UNIQUE,
        senha TEXT
    )
    """)

    cur.execute("""
    SELECT *
    FROM usuarios
    WHERE usuario=?
    """, ("admin",))

    admin = cur.fetchone()

    if not admin:

        senha = bcrypt.hashpw(
            "123456".encode(),
            bcrypt.gensalt()
        ).decode()

        cur.execute("""
        INSERT INTO usuarios(
            usuario,
            senha
        )
        VALUES(?,?)
        """, (
            "admin",
            senha
        ))

    c.commit()

    c.close()

# =========================
# INIT ERP
# =========================

def init_db():

    c = conn()

    cur = c.cursor()

    # PRODUTOS
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

    # RECEITAS
    cur.execute("""
    CREATE TABLE IF NOT EXISTS receitas(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        produto_final TEXT,
        materia_prima TEXT,
        quantidade REAL
    )
    """)

    # VENDAS
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

    # FINANCEIRO
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
