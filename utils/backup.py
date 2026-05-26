import streamlit as st
import pandas as pd
import sqlite3
import bcrypt
import plotly.express as px
from datetime import datetime
import shutil

# =========================================================
# CONFIG
# =========================================================
st.set_page_config(
    page_title="ERP Pro Max V3",
    layout="wide",
    page_icon="🍞"
)

DB_NAME = "erp_v3.db"

# =========================================================
# CSS
# =========================================================
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Roboto', sans-serif;
}

[data-testid="stSidebar"]{
    background-color:#FFFFFF;
}

.stButton>button{
    border-radius:30px;
    background-color:#1A73E8;
    color:white;
    border:none;
}

div[data-testid="metric-container"]{
    border:1px solid #EAEAEA;
    padding:20px;
    border-radius:20px;
    background:white;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# DB
# =========================================================
def conn():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

# =========================================================
# INIT DB
# =========================================================
def init_db():

    c = conn()
    cur = c.cursor()

    # USERS
    cur.execute("""
    CREATE TABLE IF NOT EXISTS usuarios(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT UNIQUE,
        senha TEXT,
        cargo TEXT
    )
    """)

    # PRODUCTS
    cur.execute("""
    CREATE TABLE IF NOT EXISTS produtos(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        tipo TEXT,
        unidade TEXT,
        estoque REAL,
        estoque_min REAL,
        custo REAL,
        venda REAL,
        ativo INTEGER DEFAULT 1
    )
    """)

    # RECIPES
    cur.execute("""
    CREATE TABLE IF NOT EXISTS receitas(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        produto_final INTEGER,
        materia_prima INTEGER,
        quantidade REAL
    )
    """)

    # PRODUCTIONS
    cur.execute("""
    CREATE TABLE IF NOT EXISTS producoes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        produto_final INTEGER,
        quantidade REAL,
        custo REAL,
        data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # SALES
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

    # FINANCE
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

    # ADMIN
    cur.execute("SELECT * FROM usuarios WHERE usuario='admin'")

    if not cur.fetchone():

        senha = bcrypt.hashpw(
            "123456".encode(),
            bcrypt.gensalt()
        ).decode()

        cur.execute("""
        INSERT INTO usuarios(usuario, senha, cargo)
        VALUES(?,?,?)
        """, (
            "admin",
            senha,
            "ADM"
        ))

    c.commit()
    c.close()

init_db()

# =========================================================
# HELPERS
# =========================================================
@st.cache_data(ttl=30)
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

def gerar_backup():

    nome = datetime.now().strftime('%Y%m%d_%H%M%S')

    shutil.copy(
        DB_NAME,
        f'backup_{nome}.db'
    )

# =========================================================
# PRODUÇÃO
# =========================================================
def produzir(produto_id, quantidade):

    c = conn()
    cur = c.cursor()

    receita = cur.execute("""
    SELECT materia_prima, quantidade
    FROM receitas
    WHERE produto_final=?
    """, (produto_id,)).fetchall()

    custo_total = 0

    for mp_id, qtd_receita in receita:

        produto_mp = cur.execute("""
        SELECT estoque, custo
        FROM produtos
        WHERE id=?
        """, (mp_id,)).fetchone()

        estoque_atual = produto_mp[0]
        custo_mp = produto_mp[1]

        baixa = qtd_receita * quantidade

        if baixa > estoque_atual:

            c.close()
            return False

        novo_estoque = estoque_atual - baixa

        cur.execute("""
        UPDATE produtos
        SET estoque=?
        WHERE id=?
        """, (
            novo_estoque,
            mp_id
        ))

        custo_total += baixa * custo_mp

    produto = cur.execute("""
    SELECT estoque
    FROM produtos
    WHERE id=?
    """, (produto_id,)).fetchone()

    estoque_pf = produto[0]

    cur.execute("""
    UPDATE produtos
    SET estoque=?
    WHERE id=?
    """, (
        estoque_pf + quantidade,
        produto_id
    ))

    cur.execute("""
    INSERT INTO producoes(
        produto_final,
        quantidade,
        custo
    )
    VALUES(?,?,?)
    """, (
        produto_id,
        quantidade,
        custo_total
    ))

    c.commit()
    c.close()

    return True

# =========================================================
# LOGIN
# =========================================================
if 'logado' not in st.session_state:
    st.session_state.logado = False

if not st.session_state.logado:

    c1, c2, c3 = st.columns([1,1.2,1])

    with c2:

        st.markdown(
            "<h2 style='text-align:center;'>🔐 ERP Pro Max</h2>",
            unsafe_allow_html=True
        )

        with st.form("login"):

            usuario = st.text_input("Usuário")
            senha = st.text_input("Senha", type="password")

            entrar = st.form_submit_button("Entrar")

            if entrar:

                users = query(
                    "SELECT * FROM usuarios WHERE usuario=?",
                    (usuario,)
                )

                if not users.empty:

                    senha_hash = users.iloc[0]['senha']

                    ok = bcrypt.checkpw(
                        senha.encode(),
                        senha_hash.encode()
                    )

                    if ok:

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

    if st.button("Sair"):

        st.session_state.logado = False
        st.rerun()

# =========================================================
# DASHBOARD
# =========================================================
if "Dashboard" in menu:

    st.title("📊 Dashboard")

    vendas = query("SELECT * FROM vendas")
    produtos = query("SELECT * FROM produtos")

    faturamento = vendas['total'].sum() if not vendas.empty else 0
    lucro = vendas['lucro'].sum() if not vendas.empty else 0

    estoque_baixo = query("""
    SELECT *
    FROM produtos
    WHERE estoque <= estoque_min
    """)

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Faturamento", moeda(faturamento))
    c2.metric("Lucro", moeda(lucro))
    c3.metric("Produtos", len(produtos))
    c4.metric("Estoque Crítico", len(estoque_baixo))

    st.error("⚠️ ALERTA AUTOMÁTICO DE ESTOQUE BAIXO")

    if not estoque_baixo.empty:

        st.dataframe(
            estoque_baixo,
            use_container_width=True
        )

    if not vendas.empty:

        graf = vendas.groupby('data')['total'].sum().reset_index()

        graf['data'] = pd.to_datetime(
            graf['data']
        ).dt.strftime('%d/%m/%Y')

        fig = px.bar(
            graf,
            x='data',
            y='total',
            title='Vendas por Data'
        )

        fig.update_layout(
            xaxis_title='Data',
            yaxis_title='Valor'
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

# =========================================================
# PRODUTOS
# =========================================================
elif "Produtos" in menu:

    st.title("📦 Produtos")

    aba1, aba2 = st.tabs([
        "Cadastrar",
        "Listagem"
    ])

    with aba1:

        with st.form("produto"):

            nome = st.text_input("Nome")

            tipo = st.selectbox(
                "Tipo",
                [
                    "Produto Final",
                    "Matéria Prima"
                ]
            )

            unidade = st.selectbox(
                "Unidade",
                [
                    "UN",
                    "KG",
                    "L"
                ]
            )

            estoque = st.number_input(
                "Estoque",
                min_value=0.0,
                step=0.1,
                format="%.2f"
            )

            estoque_min = st.number_input(
                "Estoque Mínimo",
                min_value=0.0,
                step=0.1,
                format="%.2f"
            )

            custo = st.number_input(
                "Custo",
                min_value=0.0,
                step=0.01,
                format="%.2f"
            )

            venda = st.number_input(
                "Preço Venda",
                min_value=0.0,
                step=0.01,
                format="%.2f"
            )

            salvar = st.form_submit_button("Salvar")

            if salvar:

                execute("""
                INSERT INTO produtos(
                    nome,
                    tipo,
                    unidade,
                    estoque,
                    estoque_min,
                    custo,
                    venda
                )
                VALUES(?,?,?,?,?,?,?)
                """, (
                    nome,
                    tipo,
                    unidade,
                    estoque,
                    estoque_min,
                    custo,
                    venda
                ))

                st.success("Produto cadastrado")

    with aba2:

        produtos = query(
            "SELECT * FROM produtos"
        )

        st.dataframe(
            produtos,
            use_container_width=True
        )

# =========================================================
# RECEITA TÉCNICA
# =========================================================
elif "Receita Técnica" in menu:

    st.title("🧪 Receita Técnica")

    pf = query("""
    SELECT *
    FROM produtos
    WHERE tipo='Produto Final'
    """)

    mp = query("""
    SELECT *
    FROM produtos
    WHERE tipo='Matéria Prima'
    """)

    if pf.empty or mp.empty:

        st.warning(
            "Cadastre produtos finais e matérias primas"
        )

        st.stop()

    produto_final = st.selectbox(
        "Produto Final",
        pf['nome']
    )

    materia_prima = st.selectbox(
        "Matéria Prima",
        mp['nome']
    )

    quantidade = st.number_input(
        "Quantidade Utilizada",
        min_value=0.01,
        step=0.01,
        format="%.2f"
    )

    if st.button("Adicionar Receita"):

        pf_id = pf[
            pf['nome'] == produto_final
        ].iloc[0]['id']

        mp_id = mp[
            mp['nome'] == materia_prima
        ].iloc[0]['id']

        execute("""
        INSERT INTO receitas(
            produto_final,
            materia_prima,
            quantidade
        )
        VALUES(?,?,?)
        """, (
            pf_id,
            mp_id,
            quantidade
        ))

        st.success("Receita adicionada")

# =========================================================
# PRODUÇÃO
# =========================================================
elif "Produção" in menu:

    st.title("🏭 Produção")

    pf = query("""
    SELECT *
    FROM produtos
    WHERE tipo='Produto Final'
    """)

    if pf.empty:

        st.warning("Nenhum produto final")

        st.stop()

    produto = st.selectbox(
        "Produto",
        pf['nome']
    )

    quantidade = st.number_input(
        "Quantidade Produzir",
        min_value=1.0,
        step=1.0
    )

    if st.button("Produzir"):

        produto_id = pf[
            pf['nome'] == produto
        ].iloc[0]['id']

        ok = produzir(
            produto_id,
            quantidade
        )

        if ok:

            st.success(
                "Produção realizada"
            )

        else:

            st.error(
                "Matéria-prima insuficiente"
            )

# =========================================================
# VENDAS
# =========================================================
elif "Vendas" in menu:

    st.title("🛒 Vendas")

    produtos = query("""
    SELECT *
    FROM produtos
    WHERE tipo='Produto Final'
    """)

    produto = st.selectbox(
        "Produto",
        produtos['nome']
    )

    info = produtos[
        produtos['nome'] == produto
    ].iloc[0]

    if info['unidade'] == 'UN':

        quantidade = st.number_input(
            "Quantidade",
            min_value=1,
            step=1
        )

    else:

        quantidade = st.number_input(
            "Quantidade",
            min_value=0.1,
            step=0.1,
            format="%.2f"
        )

    total = quantidade * info['venda']

    st.success(
        f"Total: {moeda(total)}"
    )

    if st.button("Finalizar Venda"):

        if info['estoque'] <= 0:

            st.error(
                "Produto sem estoque"
            )

            st.stop()

        if quantidade > info['estoque']:

            st.error(
                f"Estoque insuficiente. Disponível: {info['estoque']}"
            )

            st.stop()

        novo = info['estoque'] - quantidade

        lucro = total - (
            quantidade * info['custo']
        )

        execute("""
        UPDATE produtos
        SET estoque=?
        WHERE id=?
        """, (
            novo,
            info['id']
        ))

        execute("""
        INSERT INTO vendas(
            produto,
            quantidade,
            total,
            lucro
        )
        VALUES(?,?,?,?)
        """, (
            produto,
            quantidade,
            total,
            lucro
        ))

        st.success(
            "Venda realizada"
        )

# =========================================================
# LISTA COMPRAS
# =========================================================
elif "Lista Compras" in menu:

    st.title("⚠️ Lista de Compras")

    lista = query("""
    SELECT *
    FROM produtos
    WHERE estoque <= estoque_min
    ORDER BY estoque ASC
    """)

    if lista.empty:

        st.success(
            "Nenhum item crítico"
        )

    else:

        lista['Comprar'] = (
            lista['estoque_min'] -
            lista['estoque']
        )

        lista['Status'] = (
            'COMPRAR URGENTE'
        )

        st.warning(
            "Itens adicionados automaticamente"
        )

        st.dataframe(
            lista,
            use_container_width=True
        )

# =========================================================
# FINANCEIRO
# =========================================================
elif "Financeiro" in menu:

    st.title("💰 Financeiro")

    with st.form("financeiro"):

        tipo = st.selectbox(
            "Tipo",
            [
                "Receita",
                "Despesa"
            ]
        )

        descricao = st.text_input(
            "Descrição"
        )

        valor = st.number_input(
            "Valor",
            min_value=0.0,
            step=0.01,
            format="%.2f"
        )

        status = st.selectbox(
            "Status",
            [
                "Pendente",
                "Pago"
            ]
        )

        salvar = st.form_submit_button(
            "Salvar"
        )

        if salvar:

            execute("""
            INSERT INTO financeiro(
                tipo,
                descricao,
                valor,
                status
            )
            VALUES(?,?,?,?)
            """, (
                tipo,
                descricao,
                valor,
                status
            ))

            st.success(
                "Lançamento salvo"
            )

    fin = query(
        "SELECT * FROM financeiro"
    )

    st.dataframe(
        fin,
        use_container_width=True
    )

# =========================================================
# ALTERAR SENHA
# =========================================================
elif "Alterar Senha" in menu:

    st.title("🔐 Alterar Senha")

    with st.form("senha"):

        atual = st.text_input(
            "Senha Atual",
            type="password"
        )

        nova = st.text_input(
            "Nova Senha",
            type="password"
        )

        confirmar = st.text_input(
            "Confirmar Senha",
            type="password"
        )

        salvar = st.form_submit_button(
            "Alterar"
        )

        if salvar:

            dados = query(
                """
                SELECT *
                FROM usuarios
                WHERE usuario=?
                """,
                (
                    st.session_state.usuario,
                )
            )

            senha_hash = dados.iloc[0]['senha']

            ok = bcrypt.checkpw(
                atual.encode(),
                senha_hash.encode()
            )

            if not ok:

                st.error(
                    "Senha atual incorreta"
                )

                st.stop()

            if nova != confirmar:

                st.error(
                    "Senhas não conferem"
                )

                st.stop()

            nova_hash = bcrypt.hashpw(
                nova.encode(),
                bcrypt.gensalt()
            ).decode()

            execute("""
            UPDATE usuarios
            SET senha=?
            WHERE usuario=?
            """, (
                nova_hash,
                st.session_state.usuario
            ))

            st.success(
                "Senha alterada"
            )

# =========================================================
# AJUDA
# =========================================================
elif "Ajuda" in menu:

    st.title("❓ Central de Ajuda")

    st.markdown("""
    ### Como usar

    1. Cadastre matérias primas
    2. Cadastre produtos finais
    3. Configure receitas técnicas
    4. Faça produção
    5. Venda produtos
    6. Acompanhe dashboard

    ### Login padrão

    Usuário: admin
    Senha: 123456
    """)

# =========================================================
# BACKUP
# =========================================================
elif "Backup" in menu:

    st.title("💾 Backup")

    if st.button("Gerar Backup"):

        gerar_backup()

        st.success(
            "Backup gerado"
        )