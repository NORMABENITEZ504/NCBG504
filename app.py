import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

# 1. Configuración de página
st.set_page_config(page_title="LISA Tracker", layout="wide")

# 2. Credenciales
CID = 'f693630ca5df44fa8f10bbcd5fbc6830'
SEC = '9f90223ed60f46d2b5f39d3a1eb06c2e'

# 3. Conexión
auth_manager = SpotifyClientCredentials(client_id=CID, client_secret=SEC)
sp = spotipy.Spotify(auth_manager=auth_manager)

st.title("🤳 LISA Discography Tracker")
st.write("Estadísticas en tiempo real")

try:
    # Buscamos directamente las canciones de Lisa
    # Usamos country='US' o 'HN', pero 'US' es el más estable para la API
    results = sp.search(q='artist:LISA', type='track', limit=10)
    tracks = results['tracks']['items']
    
    lista = []
    for t in tracks:
        lista.append({
            'Canción': t['name'],
            'Popularidad 🔥': t['popularity'],
            'Álbum': t['album']['name'],
            'Link': t['external_urls']['spotify']
        })
    
    df = pd.DataFrame(lista)
    
    # Ordenar por popularidad
    df = df.sort_values(by='Popularidad 🔥', ascending=False)

    # Mostrar métricas
    c1, c2 = st.columns(2)
    c1.metric("Top Song", df.iloc[0]['Canción'], f"{df.iloc[0]['Popularidad 🔥']}/100")
    c2.metric("País Actual", "Honduras 🇭🇳", "Spotify API")

    st.write("---")
    st.dataframe(df, use_container_width=True)
    st.success("¡Conexión exitosa!")

except Exception as e:
    st.error(f"Error técnico: {e}")
    st.info("Revisa que tus llaves de Spotify no tengan espacios extra.")
