import streamlit as st
import pandas as pd
import requests
from io import StringIO
import base64

# 1. CONFIGURACIÓN Y FONDO (image_9.jpg)
st.set_page_config(page_title="LISA Charts Tracker", layout="wide")

@st.cache_data
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        return base64.b64encode(f.read()).decode()

try:
    bin_str = get_base64('image_9.jpg')
    st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{bin_str}");
        background-size: cover;
        background-attachment: fixed;
    }}
    .stApp::before {{
        content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        background-color: rgba(0, 0, 0, 0.75); z-index: -1;
    }}
    h1 {{color: #ff007f !important; text-align: center; font-family: 'Arial Black'; font-size: 45px; margin-bottom: 30px; text-shadow: 3px 3px #000;}}
    .panel {{background-color: rgba(255, 255, 255, 0.05); border: 1px solid #ff007f; padding: 20px; border-radius: 15px; text-align: center;}}
    .stMetric {{background-color: rgba(0,0,0,0.6); border: 1px solid #ff007f; border-radius: 10px; padding: 10px;}}
    a {{text-decoration: none; color: #ff007f; font-weight: bold; font-size: 16px;}}
    a:hover {{color: white;}}
    hr {{border: 0.5px solid #ff007f;}}
    </style>
    """, unsafe_allow_html=True)
except:
    st.markdown("<style>.stApp {background-color: black; color: white;}</style>", unsafe_allow_html=True)

# TÍTULO CENTRADO
st.markdown("<h1>LISA Worldwide Charts Tracker</h1>", unsafe_allow_html=True)

# 2. ESTRUCTURA DE COLUMNAS
col_redes, col_charts, col_streaming = st.columns([1.2, 2, 1.2])

# --- COLUMNA IZQUIERDA: REDES SOCIALES ---
with col_redes:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.subheader("📱 Redes Sociales")
    st.markdown("**LISA**")
    st.markdown("[Instagram](https://www.instagram.com/lalalalisa_m/)")
    st.markdown("[TikTok](https://www.tiktok.com/@lalalalisa_m?_r=1&_t=ZS-95IYpHzXmWg)")
    st.markdown("---")
    st.markdown("**LLOUD**")
    st.markdown("[Website Official](https://lalisaofficial.com)")
    st.markdown("[Instagram](https://www.instagram.com/wearelloud)")
    st.markdown("[Twitter / X](https://twitter.com/wearelloud)")
    st.markdown("[Facebook](https://www.facebook.com/wearelloud)")
    st.markdown("[TikTok](https://www.tiktok.com/@wearelloud)")
    st.markdown('</div>', unsafe_allow_html=True)

# --- COLUMNA DERECHA: STREAMING ---
with col_streaming:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.subheader("🎧 Streaming")
    st.markdown("[Spotify](https://open.spotify.com/intl-es/artist/5L1lO4eRHmJ7a0Q6csE5cT)")
    st.markdown("[Apple Music](https://music.apple.com/hn/artist/lisa/1583908668)")
    st.markdown("[Deezer](https://www.deezer.com/es/artist/145068682)")
    st.markdown("---")
    st.markdown("**YouTube Channels**")
    st.markdown("[LLOUD Official](https://www.youtube.com/channel/UC6-BgjsBa5R3PZQ_kZ8hKPg)")
    st.markdown("[Lilifilm Official](https://www.youtube.com/@lalalalisa_m)")
    st.markdown('</div>', unsafe_allow_html=True)

# --- COLUMNA CENTRAL: CHARTS ---
with col_charts:
    paises = {"Global 🌍": "global", "Tailandia 🇹🇭": "th", "Honduras 🇭🇳": "hn", "Brasil 🇧🇷": "br", "USA 🇺🇸": "us"}
    seleccion = st.selectbox("Selecciona Mercado:", list(paises.keys()))
    codigo = paises[seleccion]

    def get_data(region):
        url = f"https://charts-csv.s3.us-east-1.amazonaws.com/regional/{region}/daily/latest/regional-{region}-daily-latest.csv"
        headers = {"User-Agent": "Mozilla/5.0"}
        try:
            res = requests.get(url, headers=headers)
            if res.status_code == 200:
                lines = res.text.splitlines()
                start = 0
                for i, l in enumerate(lines[:10]):
                    if 'rank' in l.lower(): start = i; break
                df = pd.read_csv(StringIO("\n".join(lines[start:])))
                df.columns = [c.lower().strip() for c in df.columns]
                return df
            return None
        except: return None

    df = get_data(codigo)

    if df is not None:
        artist_col = next((c for c in df.columns if 'artist' in c), None)
        track_col = next((c for c in df.columns if 'track' in c), None)
        stream_col = next((c for c in df.columns if 'stream' in c), None)
        
        lisa_hoy = df[df[artist_col].astype(str).str.contains('LISA', case=False, na=False)].copy()

        if not lisa_hoy.empty:
            st.markdown(f"### Results in {seleccion}")
            for _, row in lisa_hoy.iterrows():
                st.markdown(f"**{row[track_col]}**")
                c1, c2 = st.columns(2)
                c1.metric("Position", f"#{int(row['rank'])}")
                if stream_col:
                    c2.metric("Streams", f"{int(row[stream_col]):,}")
                st.markdown("---")
            st.balloons()
        else:
            st.warning(f"LISA no aparece en el Top 200 de {seleccion} hoy.")
    else:
        st.error("No se pudo conectar con Spotify Charts.")
