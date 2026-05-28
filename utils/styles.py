import streamlit as st


def load_css():

    st.markdown("""
    <style>

    /* FUNDO */
    .stApp {
        background-color: #f4f6f9;
    }

    /* SIDEBAR */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e5e5e5;
    }

    /* TÍTULOS */
    h1, h2, h3 {
        color: #1f2937;
    }

    /* BOTÕES */
    .stButton>button {
        background-color: #2563eb;
        color: white;
        border-radius: 10px;
        border: none;
        padding: 10px;
        font-weight: 500;
    }

    .stButton>button:hover {
        background-color: #1d4ed8;
    }

    /* MÉTRICAS */
    div[data-testid="metric-container"] {
        background-color: white;
        border: 1px solid #e5e7eb;
        padding: 15px;
        border-radius: 15px;
    }

    /* INPUT */
    input {
        border-radius: 8px !important;
    }

    /* TABELA */
    .stDataFrame {
        border: 1px solid #e5e7eb;
        border-radius: 10px;
    }

    </style>
    """, unsafe_allow_html=True)
