import streamlit as st
import base64

# Función para codificar la imagen
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Reemplaza 'fondo.jpg' por el nombre exacto de tu archivo en GitHub
try:
    bin_str = get_base64('fondo.jpg') 
    
    st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{bin_str}");
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
    }}
    
    /* CAPA OSCURA: Esto es importante para que las letras se lean bien */
    .stApp::before {{
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.6); /* 0.6 es el nivel de oscuridad */
        z-index: -1;
    }}
    </style>
    """, unsafe_allow_html=True)
except FileNotFoundError:
    st.error("No se encontró la imagen. Verifica el nombre del archivo en GitHub.")
