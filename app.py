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
            x, y, w, h = rect[0]  # Tomamos la primera coincidencia

        offset_x = 50  # Desplazamiento a la derecha
        texto_a_insertar = str(row["POSICION"])

        # Insertar texto en vertical al lado derecho de la coincidencia
        page.insert_textbox(
            fitz.Rect(x + offset_x, y, x + offset_x + 20, y + 100),  
            texto_a_insertar,
            fontsize=10,
            color=(1, 0, 0),
            rotate=90  # Rotación vertical
        )


    # Descargar el nuevo PDF
    with open(output_pdf, "rb") as f:
        st.download_button("Descargar PDF Modificado", f, file_name="documento_modificado.pdf")
