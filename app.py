import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

# 1. Configuración de la página
st.set_page_config(page_title="LISA Global Tracker", layout="wide")

# 2. Tus llaves de Spotify
CID = 'f693630ca5df44fa8f10bbcd5fbc6830'
SEC = '9f90223ed60f46d2b5f39d3a1eb06c2e'

# 3. Conexión automática
auth_manager = SpotifyClientCredentials(client_id=CID, client_secret=SEC)
sp = spotipy.Spotify(auth_manager=auth_manager)

st.title("🤳 LISA Global Stats Tracker")
st.write("Datos globales de Spotify en tiempo real")

try:
    # BUSQUEDA DIRECTA (Esto evita el error 404)
    # Buscamos a la artista para obtener sus seguidores
    search_artist = sp.search(q='LISA', type='artist', limit=1)
    artist = search_artist['artists']['items'][0]
    
    seguidores = artist['followers']['total']
    popularidad_global = artist['popularity']

    # Mostramos los números grandes
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Seguidores Totales", f"{seguidores:,}")
    with col2:
        st.metric("Ranking de Popularidad", f"{popularidad_global}/100")

    st.write("---")
    st.subheader("🎵 Top Canciones (Nivel Global)")

    # Buscamos las canciones actuales
    results = sp.search(q='artist:LISA', type='track', limit=10)
    tracks = results['tracks']['items']

    lista_datos = []
    for t in tracks:
        # Filtro para asegurar que sea LISA la de BLACKPINK
        if 'LISA' in t['artists'][0]['name'].upper():
            lista_datos.append({
                'Canción': t['name'],
                'Popularidad': t['popularity'],
                'Álbum': t['album']['name']
            })

    # Crear tabla y quitar repetidos
    df = pd.DataFrame(lista_datos).drop_duplicates(subset=['Canción'])
    df = df.sort_values(by='Popularidad', ascending=False)

    st.table(df)
    st.success("¡Conexión exitosa con el mercado global!")

except Exception as e:
    st.error(f"Hubo un detalle: {e}")
