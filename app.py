import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

# 1. Configuración de página
st.set_page_config(page_title="LISA Tracker", layout="wide")

# 2. Credenciales (Tus llaves reales)
CID = 'f693630ca5df44fa8f10bbcd5fbc6830'
SEC = '9f90223ed60f46d2b5f39d3a1eb06c2e'

# 3. Conexión
auth_manager = SpotifyClientCredentials(client_id=CID, client_secret=SEC)
sp = spotipy.Spotify(auth_manager=auth_manager)

st.title("🤳 LISA Discography Tracker")
st.write("Estadísticas en tiempo real obtenidas de Spotify")

try:
    # Buscamos directamente las canciones de Lisa
    results = sp.search(q='artist:LISA', type='track', limit=15)
    tracks = results['tracks']['items']
    
    lista = []
    for t in tracks:
        # Solo agregamos si el artista principal es LISA para evitar confusiones
        if 'LISA' in t['artists'][0]['name'].upper():
            lista.append({
                'Canción': t['name'],
                'Popularidad 🔥': t['popularity'], # Aquí estaba el error, ahora está corregido
                'Álbum': t['album']['name'],
                'Lanzamiento': t['album']['release_date']
            })
    
    df = pd.DataFrame(lista)
    
    # Ordenar por las más populares
    df = df.sort_values(by='Popularidad 🔥', ascending=False).drop_duplicates(subset=['Canción'])

    # Mostrar métricas
    if not df.empty:
        c1, c2 = st.columns(2)
        c1.metric("Top Song", df.iloc[0]['Canción'], f"{df.iloc[0]['Popularidad 🔥']}/100")
        c2.metric("País", "Honduras 🇭🇳", "Spotify API")

        st.write("---")
        st.subheader("🎵 Ranking de Popularidad")
        st.dataframe(df, use_container_width=True)
        st.success("¡Datos actualizados con éxito!")
    else:
        st.warning("No se encontraron canciones recientes. Intenta refrescar.")

except Exception as e:
    st.error(f"Error técnico: {e}")
