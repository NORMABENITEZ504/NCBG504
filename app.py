import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

# 1. Configuración de la página
st.set_page_config(page_title="LISA Global Tracker", layout="wide")

# 2. Tus llaves de Spotify
CID = 'f693630ca5df44fa8f10bbcd5fbc6830'
SEC = '9f90223ed60f46d2b5f39d3a1eb06c2e'

# 3. Conexión
auth_manager = SpotifyClientCredentials(client_id=CID, client_secret=SEC)
sp = spotipy.Spotify(auth_manager=auth_manager)

st.title("🤳 LISA Global Stats Tracker")

try:
    # Buscamos a la artista específica por su ID real para no fallar con los followers
    # Este ID es el de LISA de BLACKPINK
    lisa_id = '5L1oOat9Y8mYvRsmVOSI0O'
    artist = sp.artist(lisa_id)
    
    # Extraer datos con seguridad
    nombre = artist.get('name', 'LISA')
    seguidores = artist.get('followers', {}).get('total', 0)
    popularidad = artist.get('popularity', 0)

    # Mostrar métricas
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Seguidores en el Mundo", f"{seguidores:,}")
    with col2:
        st.metric("Popularidad Global", f"{popularidad}/100")

    st.write("---")
    st.subheader("🎵 Canciones más populares actualmente")

    # Traer el Top 10 real
    top_tracks = sp.artist_top_tracks(lisa_id, country='US')
    
    lista_canciones = []
    for t in top_tracks['tracks']:
        lista_canciones.append({
            'Canción': t['name'],
            'Popularidad': t['popularity'],
            'Álbum': t['album']['name']
        })

    df = pd.DataFrame(lista_canciones)
    st.table(df) # Usamos st.table para que se vea más claro en el cel
    st.success("¡Datos globales cargados!")

except Exception as e:
    st.error(f"Error al leer los seguidores: {e}")
    st.info("Intenta refrescar la página en unos segundos.")
