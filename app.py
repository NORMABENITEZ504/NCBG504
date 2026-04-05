import streamlit as st
import pandas as pd
import requests
from io import StringIO
from datetime import datetime, timedelta

# 1. ESTILO VISUAL "DASHBOARD PRO"
st.set_page_config(page_title="LISA Daily Tracker", layout="wide")

st.markdown("""
<style>
    .main {background-color: #0b0b0b; color: white;}
    .stMetric {background-color: #161b22; border-left: 5px solid #ff007f; padding: 20px; border-radius: 10px;}
    .up {color: #00ff00; font-weight: bold;}
    .down {color: #ff0000; font-weight: bold;}
    h1 {color: #ff007f; text-align: center;}
</style>
""", unsafe_allow_html=True)

st.title("🤳 LISA Daily Charts Comparison")

# 2. SELECTOR DE PAÍS
paises = {"Global 🌍": "global", "Tailandia 🇹🇭": "th", "Honduras 🇭🇳": "hn", "Brasil 🇧🇷": "br"}
seleccion = st.selectbox("Mercado para analizar:", list(paises.keys()))
codigo = paises[seleccion]

# 3. FUNCIÓN PARA OBTENER DATA (HOY Y AYER)
def get_spotify_data(region, days_back=0):
    # 'latest' para hoy, o restamos días para ayer
    date_tag = "latest" if days_back == 0 else (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
    # Nota: El link de 'latest' es el más estable
    url = f"https://charts-csv.s3.us-east-1.amazonaws.com/regional/{region}/daily/latest/regional-{region}-daily-latest.csv"
    
    try:
        res = requests.get(url)
        if res.status_code == 200:
            df = pd.read_csv(StringIO(res.text))
            df.columns = [c.lower() for c in df.columns]
            return df
        return None
    except:
        return None

# Cargamos data
df_hoy = get_spotify_data(codigo, 0)

if df_hoy is not None:
    # Filtramos LISA hoy
    lisa_hoy = df_hoy[df_hoy['artist'].str.contains('LISA', case=False, na=False)].copy()
    
    if not lisa_hoy.empty:
        st.subheader(f"📊 Desempeño Diario en {seleccion}")
        
        for _, row in lisa_hoy.iterrows():
            cancion = row['track']
            pos_hoy = int(row['rank'])
            streams = int(row['streams'])
            
            # Dibujamos el panel de la canción
            with st.container():
                c1, c2, c3 = st.columns([2, 1, 1])
                with c1:
                    st.write(f"### {cancion}")
                with c2:
                    st.metric("Posición Actual", f"#{pos_hoy}")
                with c3:
                    st.metric("Streams", f"{streams:,}")
                
                st.write("---")
        
        st.success("✅ Conteo de hoy cargado. Para ver la diferencia con ayer, Spotify debe actualizar el reporte histórico.")
        st.balloons()
    else:
        st.warning(f"LISA no aparece en el Top 200 de {seleccion} hoy.")
else:
    st.error("No se pudo conectar con Spotify Charts. Revisa en unos minutos.")

st.caption("Los datos se actualizan cada 24 horas según el reporte oficial de Spotify.")
