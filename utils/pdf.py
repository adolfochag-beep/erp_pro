from fpdf import FPDF
import pandas as pd


def gerar_pdf_vendas(df):

    pdf = FPDF()

    pdf.add_page()

    pdf.set_font("Arial", size=12)

    pdf.cell(
        200,
        10,
        txt="RELATÓRIO DE VENDAS",
        ln=True,
        align="C"
    )

    pdf.ln(10)

    for index, row in df.iterrows():

        linha = (
            f"Produto: {row['produto']} | "
            f"Qtd: {row['quantidade']} | "
            f"Total: R$ {row['total']}"
        )

        pdf.multi_cell(
            0,
            10,
            linha
        )

    pdf.output("relatorio_vendas.pdf")