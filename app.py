import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

# 1. Configuración de la página
st.set_page_config(page_title="LISA Global Tracker", layout="wide")

# 2. Tus llaves de Spotify
CID = 'f693630ca5df44fa8f10bbcd5fbc6830'
SEC = '9f90223ed60f46d2b5f39d3a1eb06c2e'

# 3. Conexión a la API
auth_manager = SpotifyClientCredentials(client_id=CID, client_secret=SEC)
sp = spotipy.Spotify(auth_manager=auth_manager)

st.title("🤳 LISA Global Stats Tracker")
st.write("Datos globales de Spotify (Estadísticas totales)")

try:
    # EL TRUCO: Buscamos 'LISA' y el código elegirá automáticamente a la artista correcta
    search_results = sp.search(q='LISA', type='artist', limit=1)
    artist = search_results['artists']['items'][0]
    
    lisa_id = artist['id']
    nombre = artist['name']
    seguidores = artist['followers']['total']
    popularidad = artist['popularity']

    # Mostramos los números grandes globales
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Seguidores Totales", f"{seguidores:,}")
    with col2:
        st.metric("Popularidad Global", f"{popularidad}/100")

    st.write("---")
    st.subheader("🎵 Canciones más populares en el mundo hoy")

    # Traemos el Top 10 global (usamos 'US' para asegurar datos completos)
    top_tracks = sp.artist_top_tracks(lisa_id, country='US')
    
    lista_datos = []
    for t in top_tracks['tracks']:
        lista_datos.append({
            'Canción': t['name'],
            'Popularidad': t['popularity'],
            'Álbum': t['album']['name'],
            'Lanzamiento': t['album']['release_date']
        })

    df = pd.DataFrame(lista_datos)
    st.table(df) # Usamos tabla fija para que se vea bien en celular
    st.success("¡Lo logramos! Estos son los números totales de Lisa en Spotify.")

except Exception as e:
    st.error(f"Hubo un detalle técnico: {e}")
    st.info("Intenta refrescar la página en unos segundos.")
