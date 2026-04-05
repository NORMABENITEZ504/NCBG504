import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

# 1. Estilo Visual
st.set_page_config(page_title="LISA Global Tracker", layout="wide")

st.markdown("""
<style>
    .main {background-color: #0b0b0b;}
    .stMetric {background-color: #111; border: 1px solid #ff007f; padding: 15px; border-radius: 10px;}
    h1 {color: #ff007f; text-align: center;}
</style>
""", unsafe_allow_html=True)

st.title("🤳 LISA Global Spotify Tracker")

# 2. TUS LLAVES (Verificadas)
CID = 'f693630ca5df44fa8f10bbcd5fbc6830'
SEC = '5ebbe4d9a3b94065a9c7f321d471937c'

try:
    # 3. CONEXIÓN DIRECTA
    # Forzamos a que use la dirección oficial de Spotify para evitar el error 404
    auth_manager = SpotifyClientCredentials(
        client_id=CID.strip(), 
        client_secret=SEC.strip()
    )
    sp = spotipy.Spotify(auth_manager=auth_manager)

    # El ID único de LISA (sacado directamente de su perfil oficial)
    lisa_id = '5L1oOat9Y8mYvRsmVOSI0O'
    
    # 4. PEDIR DATOS AL SERVIDOR OFICIAL
    artist = sp.artist(lisa_id)
    
    # MOSTRAR NÚMEROS GLOBALES
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Seguidores Totales", f"{artist['followers']['total']:,}")
    with col2:
        st.metric("Popularidad Mundial", f"{artist['popularity']}/100")

    st.write("---")
    st.subheader("🎵 Top Canciones más populares (Global)")

    # 5. TOP TRACKS
    top_tracks = sp.artist_top_tracks(lisa_id, country='US')
    
    lista = []
    for t in top_tracks['tracks']:
        lista.append({
            "Canción": t['name'],
            "Popularidad": t['popularity'],
            "Álbum": t['album']['name']
        })
    
    df = pd.DataFrame(lista)
    st.table(df)
    
    st.success("✅ ¡CONEXIÓN EXITOSA! Datos de LISA cargados.")
    st.balloons()

except Exception as e:
    st.error("⚠️ Error de conexión con el servidor.")
    st.write("Spotify rechazó la solicitud. Intenta darle a 'Reboot App' en Streamlit.")
    st.info(f"Nota técnica: {e}")
