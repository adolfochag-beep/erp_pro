import streamlit as st

def load_css():

    st.markdown("""

    <style>

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        visibility: hidden;
    }

    .stApp {
        background-color: #f3f4f6;
        color: #111827;
    }

    section[data-testid="stSidebar"] {

        background-color: #ffffff;

        border-right: 1px solid #d1d5db;
    }

    .block-container {

        padding-top: 1rem;
    }

    div[data-testid="metric-container"] {

        background-color: white;

        border: 1px solid #e5e7eb;

        padding: 20px;

        border-radius: 16px;

        box-shadow:
        0 2px 8px rgba(0,0,0,0.05);
    }

    .stButton > button {

        background-color: #2563eb;

        color: white;

        border: none;

        border-radius: 10px;

        height: 42px;

        font-weight: 600;
    }

    .stButton > button:hover {

        background-color: #1d4ed8;

        color: white;
    }

    .stTextInput input,
    .stNumberInput input {

        background-color: white !important;

        color: black !important;

        border-radius: 10px !important;

        border: 1px solid #d1d5db !important;
    }

    div[data-baseweb="select"] > div {

        background-color: white !important;

        color: black !important;

        border-radius: 10px !important;

        border: 1px solid #d1d5db !important;
    }

    h1,h2,h3,h4 {

        color: #111827;
    }

    p,label,span {

        color: #374151 !important;
    }

    </style>

    """, unsafe_allow_html=True)