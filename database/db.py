import sqlite3
import pandas as pd
import streamlit as st
import bcrypt

DB = "erp.db"

def conn():
    return sqlite3.connect(DB, check_same_thread=False)

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

def init_db():
    c = conn()
    cur = c.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS usuarios(
        id INTEGER PRIMARY KEY,
        usuario TEXT,
        senha TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS produtos(
        id INTEGER PRIMARY KEY,
        nome TEXT,
        tipo TEXT,
        estoque REAL,
        estoque_min REAL,
        custo REAL,
        venda REAL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS receitas(
        id INTEGER PRIMARY KEY,
        produto_final INTEGER,
        materia_prima INTEGER,
        quantidade REAL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS vendas(
        id INTEGER PRIMARY KEY,
        produto TEXT,
        total REAL,
        lucro REAL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS financeiro(
        id INTEGER PRIMARY KEY,
        tipo TEXT,
        descricao TEXT,
        valor REAL
    )
    """)

    c.commit()
    c.close()

def init_users():
    c = conn()
    cur = c.cursor()

    cur.execute("SELECT * FROM usuarios WHERE usuario='admin'")
    if not cur.fetchone():

        senha = bcrypt.hashpw("123456".encode(), bcrypt.gensalt()).decode()

        cur.execute(
            "INSERT INTO usuarios(usuario, senha) VALUES(?,?)",
            ("admin", senha)
        )

    c.commit()
    c.close()
