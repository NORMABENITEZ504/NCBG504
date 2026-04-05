import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

# 1. Configuración de la App (Estilo Fanbase)
st.set_page_config(page_title="LISA Global Tracker", layout="wide")

st.markdown("""
<style>
    .main {background-color: #0b0b0b;}
    .stMetric {background-color: #111; border: 1px solid #ff007f; padding: 15px; border-radius: 10px;}
    h1 {color: #ff007f; text-align: center; text-shadow: 2px 2px #000;}
</style>
""", unsafe_allow_html=True)

st.title("🤳 LISA Global Spotify Tracker")

# 2. TUS CREDENCIALES ACTUALIZADAS
CID = 'f693630ca5df44fa8f10bbcd5fbc6830'
SEC = '5ebbe4d9a3b94065a9c7f321d471937c'

try:
    # 3. Conexión oficial con las nuevas llaves
    auth_manager = SpotifyClientCredentials(client_id=CID.strip(), client_secret=SEC.strip())
    sp = spotipy.Spotify(auth_manager=auth_manager)

    # ID oficial de LISA de BLACKPINK
    lisa_id = '5L1oOat9Y8mYvRsmVOSI0O'
    
    # 4. Obtener Perfil Global
    artist = sp.artist(lisa_id)
    
    # 5. Mostrar los números reales (millones de seguidores)
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Seguidores Globales 👥", f"{artist['followers']['total']:,}")
    with col2:
        st.metric("Popularidad Mundial 🔥", f"{artist['popularity']}/100")

    st.write("---")
    st.subheader("🎵 Top 10 Canciones más populares hoy")

    # 6. Obtener las canciones más escuchadas (Top Tracks)
    top_tracks = sp.artist_top_tracks(lisa_id, country='US')
    
    lista_datos = []
    for t in top_tracks['tracks']:
        lista_datos.append({
            "Canción": t['name'],
            "Popularidad": t['popularity'],
            "Álbum": t['album']['name'],
            "Lanzamiento": t['album']['release_date']
        })
    
    df = pd.DataFrame(lista_datos)
    
    # Mostramos la tabla completa
    st.table(df)
    
    st.success("✅ ¡CONEXIÓN EXITOSA! Datos globales cargados correctamente.")
    st.balloons() # ¡Celebración!

except Exception as e:
    st.error("⚠️ Error de conexión.")
    st.write("Asegúrate de que no haya espacios extra en GitHub al pegar el código.")
    st.info(f"Detalle técnico: {e}")
