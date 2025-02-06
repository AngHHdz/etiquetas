import streamlit as st
import pandas as pd
import fitz  # pymupdf
import os

st.title("Superponer datos de Excel en un PDF")

# Subir archivos
pdf_file = st.file_uploader("Sube el archivo PDF", type=["pdf"])
excel_file = st.file_uploader("Sube el archivo Excel", type=["xlsx"])

if pdf_file and excel_file:
    # Guardar archivos temporalmente
    pdf_path = os.path.join("temp.pdf")
    excel_path = os.path.join("temp.xlsx")

    with open(pdf_path, "wb") as f:
        f.write(pdf_file.read())

    with open(excel_path, "wb") as f:
        f.write(excel_file.read())

    # Cargar el archivo Excel
    df = pd.read_excel(excel_path, usecols=["VIN", "POSICION"])

    # Cargar el PDF
    pdf_doc = fitz.open(pdf_path)

    # Procesar cada página del PDF
    for page_num in range(len(pdf_doc)):
        page = pdf_doc[page_num]
        text = page.get_text("text")  # Extraer texto de la página

        # Buscar coincidencias en el PDF
        for _, row in df.iterrows():
            palabra_clave = str(row["VIN"])
            texto_a_insertar = str(row["POSICION"])

            if palabra_clave in text:
                rect = page.search_for(palabra_clave)
                if rect:
                    x, y, _, _ = rect[0]  # Primera coincidencia
                    page.insert_text((x - 100, y - 10), texto_a_insertar, fontsize=10, color=(0, 0, 0, 0.188))

    # Guardar el PDF modificado
    output_pdf = "documento_modificado.pdf"
    pdf_doc.save(output_pdf)
    pdf_doc.close()

    # Descargar el nuevo PDF
    with open(output_pdf, "rb") as f:
        st.download_button("Descargar PDF Modificado", f, file_name="documento_modificado.pdf")
