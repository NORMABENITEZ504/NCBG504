import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 1. ESTILO "FANBASE PRO"
st.set_page_config(page_title="LISA Worldwide Stats", layout="wide")

st.markdown("""
<style>
    .main {background-color: #0b0b0b; color: white;}
    .stMetric {background-color: #161b22; border-top: 3px solid #ff007f; padding: 20px; border-radius: 10px;}
    h1 {color: #ff007f; text-align: center; font-family: 'Arial Black';}
    .stSelectbox label {color: #ff007f !important;}
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

# 3. FUNCIÓN DE DESCARGA CON BUSCADOR DE COLUMNAS
def get_data(region):
    url = f"https://charts-csv.s3.us-east-1.amazonaws.com/regional/{region}/daily/latest/regional-{region}-daily-latest.csv"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            lines = response.text.splitlines()
            
            # Buscamos la línea donde realmente empiezan los datos (la que tiene 'rank' o 'position')
            start_line = 0
            for i, line in enumerate(lines[:10]):
                if 'rank' in line.lower() or 'position' in line.lower():
                    start_line = i
                    break
            
            # Leemos el CSV desde esa línea
            df = pd.read_csv(StringIO("\n".join(lines[start_line:])))
            df.columns = [c.lower().strip() for c in df.columns]
            return df
        return None
    except:
        return None

df = get_data(codigo)

if df is not None:
    # 4. BUSCADOR DINÁMICO DE COLUMNAS (Para que no fallen los streams)
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
                    st.caption(f"Artista: {row[artist_col]}")
                with c2:
                    st.metric("Posición", f"#{int(row['rank'])}")
                with c3:
                    # Si la columna existe, muestra el número con comas
                    if stream_col:
                        val = row[stream_col]
                        st.metric("Streams", f"{int(val):,}")
                    else:
                        st.metric("Streams", "N/A")
                st.write("---")
        
        st.success("✅ ¡Streams cargados correctamente!")
        st.balloons()
    else:
        st.warning(f"LISA no aparece en el Top 200 de {seleccion} hoy.")
else:
    st.error("No se pudo conectar con el servidor de Spotify.")

st.caption("Los datos reflejan el conteo oficial de Spotify Charts.")
