import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 1. ESTILO "FANBASE PRO"
st.set_page_config(page_title="LISA Worldwide Stats", layout="wide")

st.markdown("""
<style>
    .main {background-color: #0b0b0b; color: white;}
    .stMetric {background-color: #161b22; border-left: 5px solid #ff007f; padding: 20px; border-radius: 10px;}
    h1 {color: #ff007f; text-align: center; font-family: 'Arial Black';}
</style>
""", unsafe_allow_html=True)

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

# 3. FUNCIÓN DE DESCARGA CON SEGURIDAD
def get_data(region):
    # Intentamos la URL más estable de Spotify Charts
    url = f"https://charts-csv.s3.us-east-1.amazonaws.com/regional/{region}/daily/latest/regional-{region}-daily-latest.csv"
    
    # Engañamos al servidor para que piense que somos un navegador normal
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            # Saltamos la primera línea si Spotify mete un encabezado extra
            raw_text = response.text
            if "Pitched" in raw_text or "Spotify" in raw_text[:50]:
                df = pd.read_csv(StringIO(raw_text), skiprows=1)
            else:
                df = pd.read_csv(StringIO(raw_text))
            
            df.columns = [c.lower().strip() for c in df.columns]
            return df
        return None
    except:
        return None

df = get_data(codigo)

if df is not None:
    # Identificamos las columnas de Artista y Streams
    artist_col = 'artist_names' if 'artist_names' in df.columns else 'artist'
    track_col = 'track_name' if 'track_name' in df.columns else 'track'
    stream_col = 'streams' # Esta es la que te faltaba
    
    # Filtramos a LISA
    lisa_hoy = df[df[artist_col].str.contains('LISA', case=False, na=False)].copy()

    if not lisa_hoy.empty:
        st.subheader(f"📊 Top 200 de {seleccion}")
        
        for _, row in lisa_hoy.iterrows():
            with st.container():
                c1, c2, c3 = st.columns([2,1,1])
                with c1:
                    st.write(f"### {row[track_col]}")
                    st.write(f"👤 {row[artist_col]}")
                with c2:
                    st.metric("Posición Actual", f"#{int(row['rank'])}")
                with c3:
                    # AQUÍ APARECERÁN TUS STREAMS
                    try:
                        st.metric("Streams Diarios", f"{int(row[stream_col]):,}")
                    except:
                        st.metric("Streams Diarios", "Cargando...")
                st.write("---")
        
        st.success
