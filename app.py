import streamlit as st
import pandas as pd
import fitz  # pymupdf
import os

# Establecer imagen de fondo
background_image = "url('https://www.reddit.com/media?url=https%3A%2F%2Fi.redd.it%2Ftzzaojwterhd1.png')"  # Reemplaza con la URL de tu imagen
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: {background_image};
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Mostrar GIF centrado arriba
gif_url = "https://i.gifer.com/4UeR.gif"  # Reemplaza con la URL de tu GIF
st.markdown(
    f"""
    <div style="display: flex; justify-content: center;">
        <img src="{gif_url}" width="200">
    </div>
    """,
    unsafe_allow_html=True
)

st.title("- RE-ETIQUETADOR MIGUELITO 🫡")

# Subir archivos
pdf_file = st.file_uploader("CARGA LAS ETIQUETAS", type=["pdf"])
excel_file = st.file_uploader("CARGA LOS VINS CON POSICION", type=["xlsx"])

if pdf_file and excel_file:
    # Guardar archivos temporalmente
    pdf_path = "temp.pdf"
    excel_path = "temp.xlsx"

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

                    # Insertar texto en vertical al lado derecho de la coincidencia
                    page.insert_textbox(
                        fitz.Rect(x + offset_x + 30, y + 40, x + offset_x + 425, y + 450),
                        texto_a_insertar,
                        fontsize=20,
                        color=(0.231, 0.231, 0.216),
                        rotate=-90  # Rotación vertical
                    )

    # Guardar el PDF modificado
    output_pdf = "ETIQUETAS NUEVAS.pdf"
    pdf_doc.save(output_pdf)
    pdf_doc.close()

    # Descargar el nuevo PDF
    with open(output_pdf, "rb") as f:
        st.download_button("Descargar PDF Modificado", f, file_name="ETIQUETAS NUEVAS.pdf")
