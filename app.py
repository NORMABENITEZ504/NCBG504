import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

# 1. Configuración (Debe ser lo primero)
st.set_page_config(page_title="LISA Real-Time Stats", layout="wide")

# 2. TUS CLAVES (Pegadas directamente para evitar errores de Secrets)
CLIENT_ID = 'f693630ca5df44fa8f10bbcd5fbc6830'
CLIENT_SECRET = '9f90223ed60f46d2b5f39d3a1eb06c2e'

# 3. Función para conectar y traer datos
def cargar_datos():
    try:
        auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
        sp = spotipy.Spotify(auth_manager=auth_manager)
        
        # ID de Lisa
        LISA_URI = '5L1oOat9Y8mYvRsmVOSI0O'
        
        # Pedimos los datos (HN = Honduras)
        results = sp.artist_top_tracks(LISA_URI, country='HN')
        tracks = results['tracks']
        
        lista_canciones = []
        for track in tracks:
            lista_canciones.append({
                'Canción': track['name'],
                'Popularidad': track['popularity'],
                'Álbum': track['album']['name']
            })
        return pd.DataFrame(lista_canciones)
    except Exception as e:
        st.error(f"Error de conexión con Spotify: {e}")
        return None

# 4. Interfaz de la App
st.title("🤳 LISA Discography Tracker")
st.write("Monitoreo en tiempo real desde Honduras 🇭🇳")

df = cargar_datos()

if df is not None:
    # Métricas
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Más escuchada hoy", df.iloc[0]['Canción'], f"{df.iloc[0]['Popularidad']}/100")
    with col2:
        st.metric("País", "Honduras 🇭🇳", "Activo")

    st.write("---")
    st.subheader("🎵 Ranking de Popularidad")
    st.dataframe(df, use_container_width=True)
    st.success("¡Datos actualizados!")
