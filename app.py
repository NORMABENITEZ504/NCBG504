import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

# --------------------------
# CONFIG UI (FANBASE STYLE)
# --------------------------
st.set_page_config(page_title="LISA Charts PRO", layout="wide")

st.markdown("""
<style>
body {background-color: #0b0b0b; color: white;}
.stMetric {background-color: #111; padding: 10px; border-radius: 10px; border: 1px solid #ff007f;}
</style>
""", unsafe_allow_html=True)

st.title("🌍 LISA Spotify Global Tracker PRO")

# --------------------------
# CONFIG - TUS LLAVES
# --------------------------
CID = 'f693630ca5df44fa8f10bbcd5fbc6830'.strip()
SEC = '9f90223ed60f46d2b5f39d3a1eb06c2e'.strip()

try:
    auth_manager = SpotifyClientCredentials(client_id=CID, client_secret=SEC)
    sp = spotipy.Spotify(auth_manager=auth_manager)

    # ID de LISA de BLACKPINK
    lisa_id = '5L1oOat9Y8mYvRsmVOSI0O'
    
    # 1. OBTENER DATOS DE LA ARTISTA
    artist = sp.artist(lisa_id)
    seguidores = artist['followers']['total']
    popularidad_global = artist['popularity']

    # 2. MÉTRICAS PRINCIPALES
    st.subheader("📊 RESUMEN GLOBAL")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Seguidores Totales", f"{seguidores:,}")
    with col2:
        st.metric("Popularidad Global", f"{popularidad_global}/100")

    st.write("---")

    # 3. OBTENER TRACKS (MERCADO GLOBAL)
    st.subheader("🏆 TOP CANCIONES ACTUALES")
    
    # Pedimos los datos del mercado de US (que es el estándar para el ranking global)
    results = sp.artist_top_tracks(lisa_id, country='US')
    tracks = results['tracks']

    lista_final = []
    for t in tracks:
        lista_final.append({
            "Canción": t['name'],
            "Popularidad 🔥": t['popularity'],
            "Álbum": t['album']['name'],
            "Lanzamiento": t['album']['release_date']
        })

    df = pd.DataFrame(lista_final)

    # Mostrar Tabla Pro
    st.dataframe(df, use_container_width=True)

    # 4. GRÁFICA DE POPULARIDAD
    st.subheader("📈 Análisis de Popularidad")
    st.bar_chart(df.set_index("Canción")["Popularidad 🔥"])

    st.success("🔥 Datos reales de Spotify actualizados correctamente")

except Exception as e:
    st.error(f"Error de conexión: {e}")
    st.info("Revisa que tus llaves CID y SEC sigan siendo las mismas en tu Dashboard de Spotify.")
