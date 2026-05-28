import streamlit as st
from streamlit_option_menu import option_menu

from modulos.login import show_login, limpar_sessao

from database.db import init_db, init_users
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

# CONFIG
st.set_page_config(
    page_title="ERP PRO MAX",
    layout="wide",
    page_icon="📊"
)

# INIT DB
init_db()
init_users()
load_css()

# LOGIN
if "logado" not in st.session_state:
    st.session_state["logado"] = False

if not st.session_state["logado"]:

    show_login()

    st.stop()
# HEADER
col1, col2 = st.columns([8, 2])
col1.markdown("## 🚀 ERP PRO MAX")
col2.markdown(f"👤 {st.session_state.get('usuario','')}")

st.divider()

# SIDEBAR
with st.sidebar:

    st.markdown("""
    <h2 style='text-align:center;color:#FFFFFF;'>
    🚀 ERP PRO MAX
    </h2>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.success(
        f"👤 {st.session_state.get('usuario','')}"
    )

    menu = option_menu(
        menu_title="MENU",
        options=[
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
            "box",
            "book",
            "gear",
            "cart",
            "cash",
            "truck",
            "sliders",
            "question-circle"
        ],
        menu_icon="cast",
        default_index=0,

        styles={

            "container": {
                "padding": "5!important",
                "background-color": "#111827",
            },

            "icon": {
                "color": "#60A5FA",
                "font-size": "18px"
            },

            "nav-link": {
                "font-size": "15px",
                "text-align": "left",
                "margin":"3px",
                "--hover-color": "#1F2937",
                "border-radius": "10px",
            },

            "nav-link-selected": {
                "background-color": "#2563EB",
                "font-weight": "bold",
            },
        }
    )

    st.markdown("---")

    if st.button(
        "🚪 Sair",
        use_container_width=True
    ):

        st.session_state["logado"] = False

        limpar_sessao()

        st.rerun()

# ROTAS
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
