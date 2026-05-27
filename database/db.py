import sqlite3
import pandas as pd
import os
import streamlit as st
import bcrypt

# =========================
# BASE
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
# BANCO USUÁRIOS
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
# BANCO ERP USUÁRIO
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

def query(sql, params=()):

    c = conn()

    try:

        return pd.read_sql_query(
            sql,
            c,
            params=params
        )

    finally:

        c.close()

# =========================
# EXECUTE
# =========================

def execute(sql, params=()):

    c = conn()

    cur = c.cursor()

    cur.execute(sql, params)

    c.commit()

    c.close()

# =========================
# INIT USERS
# =========================

def init_users():

    c = users_conn()

    cur = c.cursor()

    # TABELA
    cur.execute("""
    CREATE TABLE IF NOT EXISTS usuarios(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT UNIQUE,
        senha TEXT,
        trocar_senha INTEGER DEFAULT 1
    )
    """)

    # GARANTE COLUNA NOVA
    try:

        cur.execute("""
        ALTER TABLE usuarios
        ADD COLUMN trocar_senha INTEGER DEFAULT 1
        """)

    except:

        pass

    # VERIFICA ADMIN
    cur.execute("""
    SELECT *
    FROM usuarios
    WHERE usuario = ?
    """, ("admin",))

    admin = cur.fetchone()

    # CRIA ADMIN
    if not admin:

        senha = bcrypt.hashpw(
            "admin123".encode(),
            bcrypt.gensalt()
        ).decode()

        cur.execute("""
        INSERT INTO usuarios(
            usuario,
            senha,
            trocar_senha
        )
        VALUES(?,?,?)
        """, (
            "admin",
            senha,
            1
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

    # PRODUÇÕES
    cur.execute("""
    CREATE TABLE IF NOT EXISTS producoes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        produto TEXT,
        quantidade REAL,
        custo REAL,
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
