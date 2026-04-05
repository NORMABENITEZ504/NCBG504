import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

# 1. Configuración
st.set_page_config(page_title="LISA Global Tracker", layout="wide")

# 2. Tus llaves
CID = 'f693630ca5df44fa8f10bbcd5fbc6830'
SEC = '9f90223ed60f46d2b5f39d3a1eb06c2e'

auth_manager = SpotifyClientCredentials(client_id=CID, client_secret=SEC)
sp = spotipy.Spotify(auth_manager=auth_manager)

st.title("🤳 LISA Global Stats Tracker")
st.write("Datos globales de Spotify (No de tu cuenta)")

try:
    # ID de Lisa
    LISA_URI = '5L1oOat9Y8mYvRsmVOSI0O'
    
    # 1. Traer info general del artista (Seguidores totales)
    artist = sp.artist(LISA_URI)
    seguidores = artist['followers']['total']
    popularidad_artista = artist['popularity']

    # 2. Traer las canciones mas famosas globalmente
    # Usamos 'US' porque es el mercado global mas grande para ver numeros reales
    results = sp.artist_top_tracks(LISA_URI, country='US')
    tracks = results['tracks']

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Seguidores Globales", f"{seguidores:,}")
    with col2:
        st.metric("Popularidad Artista", f"{popularidad_artista}/100")

    st.write("---")
    st.subheader("🎵 Top 10 Canciones más populares hoy")

    lista_final = []
    for t in tracks:
        lista_final.append({
            'Canción': t['name'],
            'Popularidad (0-100)': t['popularity'],
            'Álbum': t['album']['name'],
            'Disponible en': f"{len(t['available_markets'])} países"
        })

    df = pd.DataFrame(lista_final)
    st.dataframe(df, use_container_width=True)
    
    st.info("Nota: Spotify no permite ver el número exacto de reproducciones totales por este medio, pero la 'Popularidad' indica qué tan cerca está de ser la #1 del mundo.")

except Exception as e:
    st.error(f"Error al obtener datos globales: {e}")
