import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

# 1. Configuración de la App
st.set_page_config(page_title="LISA Global Tracker", layout="wide")

st.markdown("""
<style>
    .main {background-color: #0b0b0b;}
    .stMetric {background-color: #111; border: 1px solid #ff007f; padding: 15px; border-radius: 10px;}
    h1 {color: #ff007f; text-align: center;}
</style>
""", unsafe_allow_html=True)

st.title("🤳 LISA Global Spotify Tracker")

# 2. Tus Credenciales (Asegúrate de que sean estas exactamente)
CID = 'f693630ca5df44fa8f10bbcd5fbc6830'
SEC = '9f90223ed60f46d2b5f39d3a1eb06c2e'

try:
    # 3. Conexión oficial
    auth_manager = SpotifyClientCredentials(client_id=CID, client_secret=SEC)
    sp = spotipy.Spotify(auth_manager=auth_manager)

    # ID de LISA
    lisa_id = '5L1oOat9Y8mYvRsmVOSI0O'
    
    # 4. Obtener Perfil de Artista
    artist = sp.artist(lisa_id)
    
    # 5. Mostrar los números que querías ver
    col1, col2 = st.columns(2)
    col1.metric("Seguidores Totales", f"{artist['followers']['total']:,}")
    col2.metric("Popularidad Global", f"{artist['popularity']}/100")

    st.write("---")
    st.subheader("🏆 Canciones más populares hoy")

    # 6. Obtener Top Tracks
    top_tracks = sp.artist_top_tracks(lisa_id, country='US')
    
    lista = []
    for t in top_tracks['tracks']:
        lista.append({
            "Canción": t['name'],
            "Popularidad": t['popularity'],
            "Álbum": t['album']['name']
        })
    
    df = pd.DataFrame(lista)
    st.dataframe(df, use_container_width=True)
    
    st.success("✅ Conectado al servidor oficial de Spotify")

except Exception as e:
    # Mensaje simplificado por si las llaves fallan
    st.error("⚠️ No se pudo conectar con Spotify.")
    st.info("Por favor, verifica que tu Client Secret sea correcto en el Dashboard de Spotify.")
