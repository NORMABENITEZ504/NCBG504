import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 1. ESTILO VISUAL "B-CD STYLE" (Fondo oscuro y rosa)
st.set_page_config(page_title="LISA Worldwide Charts", layout="wide")

st.markdown("""
<style>
    .main {background-color: #0b0b0b; color: white;}
    .stMetric {background-color: #161b22; border-left: 5px solid #ff007f; padding: 20px; border-radius: 10px;}
    h1 {text-align: center; color: #ff007f; font-weight: bold;}
    .stSelectbox label {color: #ff007f !important;}
</style>
""", unsafe_allow_html=True)

st.title("🤳 LISA Worldwide Charts Dashboard")

# 2. SELECTOR DE MERCADO
paises = {
    "Global 🌍": "global",
    "Tailandia 🇹🇭": "th",
    "Honduras 🇭🇳": "hn",
    "Brasil 🇧🇷": "br",
    "Estados Unidos 🇺🇸": "us",
    "Corea del Sur 🇰🇷": "kr",
    "México 🇲🇽": "mx"
}
seleccion = st.selectbox("Selecciona un país para ver el Top 200:", list(paises.keys()))
codigo = paises[seleccion]

# 3. OBTENER EL TOP 200 REAL (CSV OFICIAL)
def get_data(region):
    # Usamos el enlace directo al CSV diario de Spotify
    url = f"https://charts-csv.s3.us-east-1.amazonaws.com/regional/{region}/daily/latest/regional-{region}-daily-latest.csv"
    try:
        res = requests.get(url)
        if res.status_code == 200:
            return pd.read_csv(StringIO(res.text))
        return None
    except:
        return None

df = get_data(codigo)

if df is not None:
    # Ajustamos columnas según el país
    df.columns = [c.lower() for c in df.columns]
    artist_col = 'artist_names' if 'artist_names' in df.columns else 'artist'
    track_col = 'track_name' if 'track_name' in df.columns else 'track'
    
    # BUSCAMOS A LISA
    lisa_hits = df[df[artist_col].str.contains('LISA', case=False, na=False)].copy()

    if not lisa_hits.empty:
        # MÉTRICAS ESTILO B-CD
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("Mejor Posición", f"#{int(lisa_hits['rank'].min())}")
        with m2:
            st.metric("Total Streams", f"{int(lisa_hits['streams'].sum()):,}")
        with m3:
            st.metric("Canciones en Chart", len(lisa_hits))

        st.write("---")
        st.subheader(f"📊 Desempeño en {seleccion}")
        
        # TABLA LIMPIA
        tabla_final = lisa_hits[['rank', track_col, 'streams']]
        tabla_final.columns = ['Puesto', 'Canción', 'Streams Diarios']
        st.table(tabla_final)
        
        st.balloons()
    else:
        st.warning(f"LISA no está en el Top 200 de {seleccion} hoy.")
else:
    st.error("Spotify aún no ha actualizado los datos de hoy. Intenta en un momento.")

st.caption("Datos sincronizados con los reportes diarios de Spotify Charts.")
