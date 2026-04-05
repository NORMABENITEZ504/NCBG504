import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

# 1. Configuración de la página
st.set_page_config(page_title="LISA Global Tracker", layout="wide")

# 2. Tus llaves (Limpias de espacios)
CID = 'f693630ca5df44fa8f10bbcd5fbc6830'.strip()
SEC = '9f90223ed60f46d2b5f39d3a1eb06c2e'.strip()

# 3. Conexión
auth_manager = SpotifyClientCredentials(client_id=CID, client_secret=SEC)
sp = spotipy.Spotify(auth_manager=auth_manager)

st.title("LISA Global Stats Tracker")

try:
    # ID real de LISA en Spotify
    lisa_id = '5L1oOat9Y8mYvRsmVOSI0O'
    
    # Pedimos la información del PERFIL GLOBAL de la artista
    artist = sp.artist(lisa_id)
    
    # Extraemos los SEGUIDORES TOTALES
    nombre_artista = artist['name']
    seguidores_totales = artist['followers']['total']
    popularidad_global = artist['popularity']

    # Mostramos los números que te interesan
    st.write(f"### Datos de: {nombre_artista}")
    
    col1, col2 = st.columns(2)
    with col1:
        # Esto mostrará los millones de seguidores con comas
        st.metric("Seguidores en el Mundo", f"{seguidores_totales:,}")
    with col2:
        st.metric("Popularidad Global", f"{popularidad_global}/100")

    st.write("---")
    
    # También traemos sus canciones más escuchadas hoy
    st.subheader("Canciones más populares actualmente")
    top_tracks = sp.artist_top_tracks(lisa_id, country='US')
    
    lista_canciones = []
    for t in top_tracks['tracks']:
        lista_canciones.append({
            'Canción': t['name'],
            'Popularidad': t['popularity'],
            'Álbum': t['album']['name']
        })
    
    df = pd.DataFrame(lista_canciones)
    st.table(df)
    
    st.success("¡Estos son los números oficiales de la cuenta de LISA!")

except Exception as e:
    st.error(f"No se pudieron cargar los seguidores: {e}")
