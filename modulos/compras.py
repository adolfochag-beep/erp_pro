import streamlit as st
import pandas as pd
from database.db import query

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def gerar_pdf(df):

    file_name = "lista_compras.pdf"

    c = canvas.Canvas(file_name, pagesize=letter)
    width, height = letter

    y = height - 40

    # Título
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, y, "Lista de Compras")

    y -= 20

    c.setFont("Helvetica", 10)

    # Cabeçalho
    c.drawString(40, y, "Produto")
    c.drawString(200, y, "Qtd")
    c.drawString(260, y, "Un")
    c.drawString(320, y, "Custo")

    y -= 15

    # Dados
    for _, row in df.iterrows():

        if y < 40:
            c.showPage()
            y = height - 40

        c.drawString(40, y, str(row["nome"]))
        c.drawString(200, y, str(round(row["comprar"], 2)))
        c.drawString(260, y, str(row["unidade"]))
        c.drawString(320, y, f"R$ {row['custo']:.2f}")

        y -= 15

    c.save()

    return file_name


def show_compras():

    st.title("⚠️ Lista de Compras")

    # ✅ CORRIGIDO: só matéria-prima
    sql = """
        SELECT
            nome,
            tipo,
            unidade,
            estoque,
            estoque_min,
            custo,
            (estoque_min - estoque) AS comprar
        FROM produtos
        WHERE estoque <= estoque_min
        AND LOWER(tipo) LIKE '%materia%'
    """

    df = query(sql)

    if df is None or df.empty:
        st.success("✅ Estoque OK. Nenhum item precisa de reposição.")
        return

    df["comprar"] = df["comprar"].clip(lower=0)

    st.warning("Itens que precisam de reposição")

    def destaque(row):
        if row["estoque"] == 0:
            return ["background-color: #fee2e2"] * len(row)
        return ["background-color: #fff7ed"] * len(row)

    st.dataframe(
        df.style.apply(destaque, axis=1),
        use_container_width=True,
        height=400
    )

    st.divider()

    # =========================
    # GERAR PDF
    # =========================

    if st.button("📄 Gerar PDF da Lista"):

        file_path = gerar_pdf(df)

        with open(file_path, "rb") as f:
            st.download_button(
                label="📥 Baixar PDF",
                data=f,
                file_name=file_path,
                mime="application/pdf"
            )
