import streamlit as st
import pandas as pd
import requests
from io import StringIO
import base64

# 1. CONFIGURACIÓN DE PÁGINA Y ESTILO CON FONDO PERSONALIZADO
st.set_page_config(page_title="LISA Worldwide Stats", layout="wide")

# Función para codificar la imagen de fondo local (image_9.png)
@st.cache_data
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Intentamos cargar la imagen image_9.png como fondo
try:
    # Asegúrate de que el archivo image_9.png esté en la misma carpeta que app.py en GitHub
    bin_str = get_base64_of_bin_file('image_9.png')
    
    st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{bin_str}");
        background-size: cover;
        background-attachment: fixed;
    }}
    /* Capa oscura para legibilidad */
    .stApp::before {{
        content: "";
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        background-color: rgba(0, 0, 0, 0.7); /* Oscurece el fondo un 70% */
        z-index: -1;
    }}
    /* Colores para resaltar sobre la imagen */
    h1 {{color: #ff007f !important; text-shadow: 2px 2px #000; text-align: center;}}
    h3, p, label, .stSelectbox {{color: white !important; font-weight: bold; text-shadow: 1px 1px #000;}}
    .stMetric {{background-color: rgba(22, 27, 34, 0.8); border-top: 3px solid #ff007f; padding: 20px; border-radius: 10px;}}
    </style>
    """, unsafe_allow_html=True)
except FileNotFoundError:
    # Si no encuentra la imagen, usa fondo oscuro
    st.warning("⚠️ No se encontró el archivo 'image_9.png'. Asegúrate de subirlo a tu repositorio de GitHub.")
    st.markdown("""<style>.stApp {background-color: #0b0b0b; color: white;}</style>""", unsafe_allow_html=True)

st.title("🤳 LISA Worldwide Charts Tracker")

# 2. SELECTOR DE PAÍS
paises = {
    "Global 🌍": "global",
    "Tailandia 🇹🇭": "th",
    "Honduras 🇭🇳": "hn",
    "Brasil 🇧🇷": "br",
    "Estados Unidos 🇺🇸": "us"
}
seleccion = st.selectbox("Mercado para analizar:", list(paises.keys()))
codigo = paises[seleccion]

# 3. FUNCIÓN DE DESCARGA (Anti-bloqueo de streams)
def get_data(region):
    url = f"https://charts-csv.s3.us-east-1.amazonaws.com/regional/{region}/daily/latest/regional-{region}-daily-latest.csv"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            lines = response.text.splitlines()
            start_line = 0
            for i, line in enumerate(lines[:10]):
                if 'rank' in line.lower() or 'position' in line.lower():
                    start_line = i
                    break
            df = pd.read_csv(StringIO("\n".join(lines[start_line:])))
            df.columns = [c.lower().strip() for c in df.columns]
            return df
        return None
    except:
        return None

df = get_data(codigo)

if df is not None:
    # Buscador de columnas
    artist_col = next((c for c in df.columns if 'artist' in c), None)
    track_col = next((c for c in df.columns if 'track' in c or 'title' in c), None)
    stream_col = next((c for c in df.columns if 'stream' in c or 'count' in c), None)
    
    # Filtramos a LISA
    lisa_hoy = df[df[artist_col].astype(str).str.contains('LISA', case=False, na=False)].copy()

    if not lisa_hoy.empty:
        st.subheader(f"📊 Reporte de Streams en {seleccion}")
        
        for _, row in lisa_hoy.iterrows():
            with st.container():
                c1, c2, c3 = st.columns([2,1,1])
                with c1:
                    st.write(f"### {row[track_col]}")
                    st.write(f"Artista: {row[artist_col]}")
                with c2:
                    st.metric("Posición", f"#{int(row['rank'])}")
                with c3:
                    if stream_col:
                        st.metric("Streams", f"{int(row[stream_col]):,}")
                st.write("---")
        st.balloons()
    else:
        st.warning(f"LISA no aparece en el Top 200 de {seleccion} hoy.")
else:
    st.error("No se pudo conectar con el servidor de Spotify.")
