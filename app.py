import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

# TUS CÓDIGOS REALES
CLIENT_ID = 'f693630ca5df44fa8f10bbcd5fbc6830'
CLIENT_SECRET = '9f90223ed60f46d2b5f39d3a1eb06c2e'

# Conexión con Spotify
auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)

st.set_page_config(page_title="LISA Real-Time Stats", layout="wide")
st.title("🤳 LISA Discography Tracker")

# ID de Lisa
LISA_URI = 'spotify:artist:5L1oOat9Y8mYvRsmVOSI0O'

try:
    # Traer canciones top de Lisa
    results = sp.artist_top_tracks(LISA_URI)
    tracks = results['tracks']

    data = []
    for track in tracks:
        data.append({
            'Canción': track['name'],
            'Popularidad': track['popularity'],
            'Álbum': track['album']['name']
        })

    df = pd.DataFrame(data)

    # Mostrar métricas
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Top en Honduras 🇭🇳", "Rockstar", "Puesto #34")
    with col2:
        st.metric("Más Popular hoy", df.iloc[0]['Canción'], f"{df.iloc[0]['Popularidad']}/100")

    st.write("---")
    st.subheader("🎵 Estadísticas Reales de Spotify")
    st.dataframe(df, use_container_width=True)
    st.success("¡Datos actualizados con éxito!")

except Exception as e:
    st.error(f"Error al conectar con Spotify: {e}")
