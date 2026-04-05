import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

# 1. Configuración básica
st.set_page_config(page_title="LISA Global Tracker", layout="wide")

# 2. Tus llaves de Spotify
CID = 'f693630ca5df44fa8f10bbcd5fbc6830'
SEC = '9f90223ed60f46d2b5f39d3a1eb06c2e'

# 3. Conexión a la API
auth_manager = SpotifyClientCredentials(client_id=CID, client_secret=SEC)
sp = spotipy.Spotify(auth_manager=auth_manager)

st.title("🤳 LISA Global Stats Tracker")

try:
    # --- PASO 1: BUSCAR A LA ARTISTA ---
    # Buscamos 'LISA' y tomamos el primer resultado de tipo 'artist'
    search_result = sp.search(q='LISA', type='artist', limit=1)
    artist_data = search_result['artists']['items'][0]
    
    # Datos globales
    nombre = artist_data['name']
    seguidores = artist_data['followers']['total']
    puntos_popularidad = artist_data['popularity']
    lisa_id = artist_data['id']

    # Mostrar números globales
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Seguidores Globales", f"{seguidores:,}")
    with col2:
        st.metric("Popularidad Global", f"{puntos_popularidad}/100")

    st.write("---")
    st.subheader("🎵 Canciones más escuchadas en el mundo hoy")

    # --- PASO 2: BUSCAR SUS CANCIONES TOP ---
    # Usamos el ID que encontramos automáticamente para evitar el error 404
    top_tracks = sp.artist_top_tracks(lisa_id, country='US')
    
    lista_final = []
    for t in top_tracks['tracks']:
        lista_final.append({
            'Canción': t['name'],
            'Popularidad Global': t['popularity'],
            'Álbum': t['album']['name']
        })

    df = pd.DataFrame(lista_final)
    # Mostramos la tabla fija para que no se mueva
    st.table(df)
    st.success("¡Éxito! Estos son los números totales de Spotify.")

except Exception as e:
    st.error(f"Hubo un detalle con la conexión: {e}")
    st.info("Revisa que no haya espacios extra en tus llaves (CID y SEC).")
