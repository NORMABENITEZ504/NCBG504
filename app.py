import streamlit as st
import pandas as pd
from spotifycharts import SpotifyCharts

# 1. ESTILO VISUAL "B-CD STYLE"
st.set_page_config(page_title="LISA Charts Center", layout="wide")

st.markdown("""
<style>
    .main {background-color: #0b0b0b; color: white;}
    .stMetric {background-color: #161b22; border-left: 5px solid #ff007f; padding: 20px; border-radius: 10px;}
    h1 {text-align: center; color: #ff007f; font-family: 'Arial';}
</style>
""", unsafe_allow_html=True)

st.title("🤳 LISA Worldwide Charts Dashboard")

# 2. CONFIGURACIÓN DE MERCADOS
paises = {
    "Global 🌍": "global",
    "Tailandia 🇹🇭": "th",
    "Honduras 🇭🇳": "hn",
    "Brasil 🇧🇷": "br",
    "Estados Unidos 🇺🇸": "us",
    "Corea del Sur 🇰🇷": "kr",
    "México 🇲🇽": "mx"
}
seleccion = st.selectbox("Selecciona mercado para analizar el Top 200:", list(paises.keys()))
codigo = paises[seleccion]

# 3. OBTENER EL TOP 200 REAL
try:
    api = SpotifyCharts()
    # Traemos el chart diario más reciente
    df = api.get_chart(region=codigo, freq='daily', chart='top200')
    
    if df is not None and not df.empty:
        # Filtramos a LISA (buscamos en la columna de artistas)
        lisa_tracks = df[df['artist'].str.contains('LISA', case=False, na=False)].copy()

        if not lisa_tracks.empty:
            # MÉTRICAS PRO
            m1, m2, m3 = st.columns(3)
            with m1:
                st.metric("Mejor Posición", f"#{int(lisa_tracks['rank'].min())}")
            with m2:
                st.metric("Total Streams", f"{int(lisa_tracks['streams'].sum()):,}")
            with m3:
                st.metric("Canciones en Chart", len(lisa_tracks))

            st.write("---")
            st.subheader(f"📊 Desempeño detallado en {seleccion}")
            
            # Formateamos la tabla para que se vea limpia
            lisa_tracks = lisa_tracks[['rank', 'track', 'artist', 'streams']]
            lisa_tracks.columns = ['Puesto', 'Canción', 'Artista', 'Streams']
            
            st.table(lisa_tracks)
            st.balloons()
        else:
            st.warning(f"LISA no entró en el Top 200 de {seleccion} hoy.")
            st.info("¡Sigue haciendo stream para que aparezca mañana!")
            
    else:
        st.error("Spotify no ha publicado los datos de hoy todavía.")

except Exception as e:
    st.error("Error de conexión con los servidores oficiales.")
    st.info("Intenta darle a 'Manage app' -> 'Reboot' en Streamlit para limpiar la conexión.")
