import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

# 1. Configuración de la página
st.set_page_config(page_title="LISA Global Tracker", layout="wide")

# 2. Tus llaves de Spotify (Verifica que no tengan espacios al final)
CID = 'f693630ca5df44fa8f10bbcd5fbc6830'
SEC = '9f90223ed60f46d2b5f39d3a1eb06c2e'

# 3. Conexión a la API
auth_manager = SpotifyClientCredentials(client_id=CID, client_secret=SEC)
sp = spotipy.Spotify(auth_manager=auth_manager)

st.title("🤳 LISA Global Stats Tracker")

try:
    # EL TRUCO: Usamos el ID exacto de LISA para que no haya fallos
    lisa_id = '5L1oOat9Y8mYvRsmVOSI0O'
    
    # Obtenemos la info de la artista directamente
    artist = sp.artist(lisa_id)
    
    nombre = artist['name']
    seguidores = artist['followers']['total']
    popularidad = artist['popularity']

    # Mostramos los números grandes (Seguidores totales en el mundo)
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Seguidores Globales", f"{seguidores:,}")
    with col2:
        st.metric("Popularidad Global", f"{popularidad}/100")

    st.write("---")
    st.subheader("🎵 Canciones más populares hoy")

    # Buscamos sus canciones Top en el mercado global (US)
    top_tracks = sp.artist_top_tracks(lisa_id, country='US')
    
    lista_final = []
    for t in top_tracks['tracks']:
        lista_final.append({
            'Canción': t['name'],
            'Popularidad 🔥': t['popularity'],
            'Álbum': t['album']['name']
        })

    df = pd.DataFrame(lista_final)
    
    # Mostramos la tabla
    st.table(df)
    st.success("¡Lo logramos! Estos son los datos oficiales de Spotify.")

except Exception as e:
    st.error(f"Error técnico: {e}")
    st.info("Asegúrate de que tus llaves CID y SEC estén bien pegadas en el código.")
