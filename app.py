import streamlit as st

from streamlit_option_menu import option_menu

from database.db import (
    init_db,
    init_users
)
from utils.styles import load_css

from modulos.login import show_login

from modulos.dashboard import show_dashboard
from modulos.produtos import show_produtos
from modulos.receitas import show_receitas
from modulos.producao import show_producao
from modulos.vendas import show_vendas
from modulos.financeiro import show_financeiro
from modulos.compras import show_compras
from modulos.ajuda import show_ajuda
from modulos.configuracoes import show_config

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="ERP PRO MAX",
    layout="wide",
    page_icon="📊"
)

# CARREGA CSS
load_css()

# INICIA BANCO
init_db()

# CONTROLE LOGIN
load_css()

init_users()
if "logado" not in st.session_state:

    st.session_state["logado"] = False

# LOGIN
if not st.session_state["logado"]:

    show_login()

    st.stop()

# CRIA BANCO DO USUÁRIO
init_db()

# SIDEBAR
with st.sidebar:

    st.markdown("## 🚀 ERP PRO MAX")

    st.caption(
        f"Usuário: {st.session_state['usuario']}"
    )

    menu = option_menu(
        "",
        [
            "Dashboard",
            "Produtos",
            "Receitas",
            "Produção",
            "Vendas",
            "Financeiro",
            "Compras",
            "Configurações",
            "Ajuda"
        ],
        icons=[
            "speedometer2",
            "box-seam",
            "journal-text",
            "gear-wide-connected",
            "cart-fill",
            "cash-stack",
            "truck",
            "gear",
            "question-circle"
        ],
        default_index=0
    )

    st.divider()

    if st.button("Sair"):

        st.session_state["logado"] = False

        st.rerun()

# ROTAS DOS MÓDULOS

if menu == "Dashboard":

    show_dashboard()

elif menu == "Produtos":

    show_produtos()

elif menu == "Receitas":

    show_receitas()

elif menu == "Produção":

    show_producao()

elif menu == "Vendas":

    show_vendas()

elif menu == "Financeiro":

    show_financeiro()

elif menu == "Compras":

    show_compras()

elif menu == "Configurações":

    show_config()

elif menu == "Ajuda":

    show_ajuda()