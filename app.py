import streamlit as st
from streamlit_option_menu import option_menu

from modulos.login import show_login, limpar_sessao

from database.db import (
    init_db,
    init_users
)

from utils.styles import load_css

from modulos.dashboard import show_dashboard
from modulos.produtos import show_produtos
from modulos.receitas import show_receitas
from modulos.producao import show_producao
from modulos.vendas import show_vendas
from modulos.financeiro import show_financeiro
from modulos.compras import show_compras
from modulos.ajuda import show_ajuda
from modulos.configuracoes import show_config


# =========================
# CONFIGURAÇÃO DA PÁGINA
# =========================

st.set_page_config(
    page_title="ERP PRO MAX",
    layout="wide",
    page_icon="📊",
    initial_sidebar_state="expanded"
)

# =========================
# INICIALIZAÇÃO
# =========================

init_db()
init_users()
load_css()

# =========================
# LOGIN (ÚNICO LUGAR)
# =========================

if "logado" not in st.session_state:
    st.session_state["logado"] = False

show_login()

if not st.session_state["logado"]:
    st.stop()

# =========================
# HEADER
# =========================

col_logo, col_user = st.columns([8, 2])

with col_logo:
    st.markdown("## 🚀 ERP PRO MAX")

with col_user:
    st.markdown(f"👤 **{st.session_state['usuario']}**")

st.divider()

# =========================
# MENU PRINCIPAL
# =========================

menu = option_menu(
    None,
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
    orientation="horizontal",
    styles={
        "container": {
            "padding": "5px",
            "background-color": "#f8f9fa",
            "border-radius": "10px"
        },
        "icon": {
            "font-size": "16px",
            "color": "#0d6efd"
        },
        "nav-link": {
            "font-size": "14px",
            "text-align": "center",
        },
        "nav-link-selected": {
            "background-color": "#0d6efd",
            "color": "white",
        },
    }
)

st.markdown("<br>", unsafe_allow_html=True)

# =========================
# SIDEBAR
# =========================

with st.sidebar:

    st.markdown("### ⚙️ Painel")

    st.info(f"Logado como:\n**{st.session_state['usuario']}**")

    st.divider()

    if st.button("🚪 Sair", use_container_width=True):
        st.session_state["logado"] = False
        limpar_sessao()   # ✅ CORRETO
        st.rerun()

# =========================
# ROTAS
# =========================

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
