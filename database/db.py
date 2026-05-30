import sqlite3
import pandas as pd
import streamlit as st
import os
import bcrypt

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_DIR = os.path.join(BASE_DIR, "databases")
os.makedirs(DATABASE_DIR, exist_ok=True)

USERS_DB = os.path.join(DATABASE_DIR, "usuarios.db")

def users_conn():
    return sqlite3.connect(USERS_DB, check_same_thread=False)

def get_user_db():
    usuario = st.session_state.get("usuario", "default")
    return os.path.join(DATABASE_DIR, f"{usuario}.db")

def conn():
    return sqlite3.connect(get_user_db(), check_same_thread=False)

@st.cache_data(ttl=60)
def query(sql, params=()):
    try:
        c = conn()
        df = pd.read_sql_query(sql, c, params=params)
        c.close()
        return df
    except:
        return pd.DataFrame()

def execute(sql, params=()):
    c = conn()
    cur = c.cursor()
    cur.execute(sql, params)
    c.commit()
    c.close()
    st.cache_data.clear()

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

    cur.execute("SELECT 1 FROM usuarios WHERE usuario='admin'")
    if not cur.fetchone():
        senha = bcrypt.hashpw("123456".encode(), bcrypt.gensalt()).decode()
        cur.execute("INSERT INTO usuarios(usuario, senha) VALUES(?,?)", ("admin", senha))

    c.commit()
    c.close()

def init_db():
    c = conn()
    cur = c.cursor()

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

    cur.execute("""
    CREATE TABLE IF NOT EXISTS receitas(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        produto_final INTEGER,
        materia_prima INTEGER,
        quantidade REAL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS producoes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        produto_final INTEGER,
        quantidade REAL,
        custo REAL,
        status TEXT DEFAULT 'Ativa',
        data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

       cur.execute("""
    CREATE TABLE IF NOT EXISTS vendas(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        produto TEXT,
        quantidade REAL,
        total REAL,
        lucro REAL,
        cliente TEXT,
        forma_pagamento TEXT,
        status_pagamento TEXT,
        data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    try:
        cur.execute(
            "ALTER TABLE vendas ADD COLUMN status TEXT DEFAULT 'Ativa'"
        )
    except Exception:
        pass

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

def recalcular_custo_produto(produto_final_id):
    c = conn()
    cur = c.cursor()

    custo = cur.execute("""
        SELECT SUM(r.quantidade * p.custo)
        FROM receitas r
        JOIN produtos p ON r.materia_prima = p.id
        WHERE r.produto_final = ?
    """, (produto_final_id,)).fetchone()[0] or 0

    cur.execute("UPDATE produtos SET custo=? WHERE id=?", (custo, produto_final_id))
    c.commit()
    c.close()
