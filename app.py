import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

# 1. ESTILO VISUAL PRO
st.set_page_config(page_title="LISA Charts Center", layout="wide")

st.markdown("""
<style>
    .main {background-color: #0b0b0b; color: white;}
    .stMetric {background-color: #161b22; border-left: 5px solid #ff007f; padding: 20px; border-radius: 10px;}
    .css-12w0qpk {color: #ff007f;}
    h1 {text-align: center; color: #ff007f; font-family: 'Arial';}
</style>
""", unsafe_allow_html=True)

st.title("🤳 LISA Worldwide Charts Dashboard")

# 2. SELECTOR DE PAÍS
paises = {
    "Global 🌍": "global",
    "Tailandia 🇹🇭": "th",
    "Honduras 🇭🇳": "hn",
    "Brasil 🇧🇷": "br",
    "Estados Unidos 🇺🇸": "us",
    "Corea del Sur 🇰🇷": "kr",
    "México 🇲🇽": "mx"
}
seleccion = st.selectbox("Selecciona mercado para analizar:", list(paises.keys()))
codigo = paises[seleccion]

# 3. FUNCIÓN PARA SCRAPING DE TOP 200 (Más estable que CSV)
def get_live_charts(country_code):
    url = f"https://kworb.net/spotify/country/{country_code}_daily.html"
    try:
        res = requests.get(url)
        # Kworb es la fuente más estable para trackers de fans
        tables = pd.read_html(res.text)
        df = tables[0]
        return df
    except:
        return None

df = get_live_charts(codigo)

if df is not None:
    # Identificar columnas (Kworb usa nombres distintos)
    # Buscamos a LISA
    lisa_mask = df.astype(str).apply(lambda x: x.str.contains('LISA', case=False)).any(axis=1)
    lisa_data = df[lisa_mask].copy()

    if not lisa_data.empty:
        # Métricas principales
        m1, m2 = st.columns(2)
        
        # Intentamos sacar la posición (columna 0 generalmente)
        pos = lisa_data.iloc[0, 0]
        streams = lisa_data.iloc[0, 6] if len(lisa_data.columns) > 6 else "N/A"
        
        with m1:
            st.metric("Mejor Posición", f"#{pos}")
        with m2:
            st.metric("Streams Diarios (Aprox)", f"{streams}")

        st.write("---")
        st.subheader(f"📊 Desempeño en {seleccion}")
        
        # Limpiamos la tabla para que se vea como B-CD
        # Seleccionamos: Posición, Artista - Canción, Streams
        # Dependiendo del país, las columnas varían, así que mostramos la fila limpia
        st.dataframe(lisa_data, use_container_width=True)
        
        st.success(f"LISA está actualmente en el Top 200 de {seleccion}")
        st.balloons()
    else:
        st.warning(f"LISA no se encuentra en el Top 200 de {seleccion} hoy.")
        st.info("Sugerencia: Revisa el chart de Tailandia 🇹🇭 para ver sus mejores números.")

else:
    st.error("No se pudo conectar con el servidor de Charts.")
    st.info("Esto pasa cuando Spotify o Kworb están actualizando datos. Intenta en 5 minutos.")

st.caption("Los datos se sincronizan con los charts diarios globales.")
