import streamlit as st
import pandas as pd
import requests
from io import StringIO
from datetime import datetime

# 1. ESTILO VISUAL "DARK FANBASE"
st.set_page_config(page_title="LISA Spotify Dashboard", layout="wide")

st.markdown("""
<style>
    .main {background-color: #0b0b0b; color: white;}
    .stMetric {background-color: #161b22; border: 1px solid #ff007f; padding: 20px; border-radius: 15px;}
    div[data-testid="stExpander"] {background-color: #161b22; border: none;}
    .css-1offfwp e16nr0p33 {color: #ff007f;}
</style>
""", unsafe_allow_html=True)

st.title("🤳 LISA Worldwide Charts Dashboard")
st.write("Seguimiento diario de posiciones en el Top 200")

# 2. SELECTOR DE MERCADO
col_sel1, col_sel2 = st.columns([2, 1])
with col_sel1:
    paises = {
        "Global 🌍": "global",
        "Tailandia 🇹🇭": "th",
        "Honduras 🇭🇳": "hn",
        "Brasil 🇧🇷": "br",
        "Estados Unidos 🇺🇸": "us",
        "Corea del Sur 🇰🇷": "kr",
        "México 🇲🇽": "mx"
    }
    seleccion = st.selectbox("Selecciona el mercado para analizar:", list(paises.keys()))
    codigo = paises[seleccion]

# 3. FUNCIÓN PARA CARGAR EL TOP 200 REAL
@st.cache_data(ttl=3600) # Guarda los datos por 1 hora para que cargue rápido
def get_top_200(country_code):
    url = f"https://charts-csv.s3.us-east-1.amazonaws.com/regional/{country_code}/daily/latest/regional-{country_code}-daily-latest.csv"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            return pd.read_csv(StringIO(res.text))
        return None
    except:
        return None

df = get_top_200(codigo)

if df is not None:
    # Limpieza de nombres de columnas
    df.columns = [c.lower().strip() for c in df.columns]
    artist_col = 'artist_names' if 'artist_names' in df.columns else 'artist'
    track_col = 'track_name' if 'track_name' in df.columns else 'track'
    
    # FILTRAR A LISA
    lisa_data = df[df[artist_col].str.contains("LISA", case=False, na=False)].copy()

    # 4. MÉTRICAS ESTILO "DETAILS"
    st.write("---")
    m1, m2, m3 = st.columns(3)
    
    if not lisa_data.empty:
        top_pos = int(lisa_data['rank'].min())
        total_streams = lisa_data['streams'].sum()
        
        m1.metric("Mejor Posición Hoy", f"#{top_pos}")
        m2.metric("Total Streams (LISA)", f"{total_streams:,}")
        m3.metric("Mercado Seleccionado", seleccion)

        st.write("### 📈 Desempeño de Canciones")
        
        # TABLA ESTILIZADA
        # Preparamos los datos para que se vean como en la web que pasaste
        lisa_data['Puesto'] = lisa_data['rank'].apply(lambda x: f"#{int(x)}")
        lisa_data['Streams Diarios'] = lisa_data['streams'].apply(lambda x: f"{int(x):,}")
        
        final_table = lisa_data[[track_col, 'Puesto', 'Streams Diarios']]
        final_table.columns = ['Canción', 'Posición Actual', 'Streams']
        
        st.table(final_table)
        
        # Gráfica de barras para ver cuál es la que más suena
        st.bar_chart(lisa_data.set_index(track_col)['streams'])
        
    else:
        st.warning(f"LISA no se encuentra en el Top 200 de {seleccion} en este momento.")
        st.info("¡Sigue haciendo stream para que entre en el próximo corte!")

else:
    st.error("No se pudo obtener la data de Spotify Charts.")
    st.info("Intenta refrescar la página en unos minutos; a veces los servidores de Amazon S3 se saturan.")

st.write("---")
st.caption("Actualizado automáticamente con los últimos CSV oficiales de Spotify Charts.")
