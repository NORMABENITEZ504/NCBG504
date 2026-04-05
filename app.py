import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# 1. Configuración rápida
st.set_page_config(page_title="LISA Global Stats")

# 2. Credenciales (Limpiadas de cualquier espacio invisible)
CID = 'f693630ca5df44fa8f10bbcd5fbc6830'.strip()
SEC = '9f90223ed60f46d2b5f39d3a1eb06c2e'.strip()

st.title("📊 LISA Global Stats")

try:
    # 3. Intentar conexión
    auth_manager = SpotifyClientCredentials(client_id=CID, client_secret=SEC)
    sp = spotipy.Spotify(auth_manager=auth_manager)
    
    # 4. ID Directo de LISA
    lisa_id = '5L1oOat9Y8mYvRsmVOSI0O'
    
    # 5. Pedir datos
    artist = sp.artist(lisa_id)
    
    # Si llega aquí, es que funcionó
    name = artist['name']
    followers = artist['followers']['total']
    popularity = artist['popularity']

    st.balloons() # ¡Festejo si funciona!
    
    col1, col2 = st.columns(2)
    col1.metric("Seguidores Globales", f"{followers:,}")
    col2.metric("Popularidad", f"{popularity}/100")
    
    st.write(f"Conectado exitosamente al perfil oficial de **{name}**")

except Exception as error:
    # ESTO NOS DIRÁ EL ERROR REAL
    st.error("⚠️ Error detectado")
    st.code(f"Tipo de error: {type(error).__name__}")
    st.code(f"Mensaje: {error}")
    
    if "invalid_client" in str(error):
        st.warning("El problema son las llaves (ID o Secret). Revisa que estén bien copiadas en Spotify Developer.")
    elif "404" in str(error):
        st.warning("Spotify no encuentra el ID de la artista. Revisaremos el código de nuevo.")
