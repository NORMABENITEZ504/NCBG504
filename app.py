import streamlit as st
import pandas as pd
import requests
from io import StringIO
from datetime import datetime, timedelta

# 1. ESTILO VISUAL "LISA STATS PRO"
st.set_page_config(page_title="LISA Spotify Tracker", layout="wide")

st.markdown("""
<style>
    .main {background-color: #0b0b0b; color: white;}
    .stMetric {background-color: #161b22; border-top: 4px solid #ff007f; padding: 20px; border-radius: 10px;}
    h1 {color: #ff007f; text-align: center; font-family: 'Arial Black';}
    .status-up {color: #00ff00; font-weight: bold;}
    .status-down {color: #ff0000; font-weight: bold;}
</style>
""", unsafe_allow_html=True)

st.title("🤳 LISA Worldwide Daily Tracker")

# 2. CONFIGURACIÓN DE FECHAS Y PAÍSES
paises = {"Global 🌍": "global", "Tailandia 🇹🇭": "th", "Honduras 🇭🇳": "hn", "Brasil 🇧🇷": "br", "USA 🇺🇸": "us"}
seleccion = st.selectbox("Selecciona Mercado:", list(paises.keys()))
codigo = paises[seleccion]

@st.cache_data(ttl=3600)
def get_chart_by_date(region, date_obj):
    date_str = date_obj.strftime('%Y-%m-%d')
    # Intentamos la URL por fecha exacta
    url = f"https://charts-csv.s3.us-east-1.amazonaws.com/regional/{region}/daily/{date_str}/resources/chart.csv"
    
    # Si la URL de arriba falla (porque Spotify cambia carpetas), usamos la de respaldo 'latest'
    url_backup = f"https://charts-csv.s3.us-east-1.amazonaws.com/regional/{region}/daily/latest/regional-{region}-daily-latest.csv"
    
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        res = requests.get(url_backup, headers=headers)
        if res.status_code == 200:
            df = pd.read_csv(StringIO(res.text))
            df.columns = [c.lower() for c in df.columns]
            return df
        return None
    except:
        return None

# 3. CARGAR HOY Y AYER
hoy_date = datetime.now() - timedelta(days=1) # Spotify siempre va un día atrás
ayer_date = hoy_date - timedelta(days=1)

df_hoy = get_chart_by_date(codigo, hoy_date)

if df_hoy is not None:
    # Identificar columnas
    artist_col = 'artist_names' if 'artist_names' in df_hoy.columns else 'artist'
    track_col = 'track_name' if 'track_name' in df_hoy.columns else 'track'
    
    # Filtrar LISA
    lisa_hoy = df_hoy[df_hoy[artist_col].str.contains('LISA', case=False, na=False)].copy()

    if not lisa_hoy.empty:
        st.subheader(f"📊 Reporte de Posiciones en {seleccion}")
        
        for _, row in lisa_hoy.iterrows():
            with st.container():
                col1, col2, col3 = st.columns([2,1,1])
                with col1:
                    st.write(f"### {row[track_col]}")
                    st.write(f"👤 {row[artist_col]}")
                with col2:
                    st.metric("Posición Actual", f"#{int(row['rank'])}")
                with col3:
                    st.metric("Streams Diarios", f"{int(row['streams']):,}")
                st.write("---")
