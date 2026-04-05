import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# 1. Configuracion rapida
st.set_page_config(page_title="LISA Global Stats", page_icon="📊")

# 2. TUS LLAVES (Las he limpiado de espacios extra)
CID = "f693630ca5df44fa8f10bbcd5fbc6830".strip()
SEC = "9f90223ed60f46d2b5f39d3a1eb06c2e".strip()

st.title("📊 LISA Global Stats")

try:
    # 3. Conexion ultra-limpia
    client_credentials_manager = SpotifyClientCredentials(client_id=CID, client_secret=SEC)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    
    # 4. Pedir datos de LISA de BLACKPINK
    lisa_id = '5L1oOat9Y8mYvRsmVOSI0O'
    artist = sp.artist(lisa_id)
    
    # Si llegamos aqui, ¡FUNCIONO!
    followers = artist['followers']['total']
    popularity = artist['popularity']
    name = artist['name']

    st.balloons()
    
    st.subheader(f"Perfil Oficial de {name}")
    col1, col2 = st.columns(2)
    col1.metric("Seguidores Globales", f"{followers:,}")
    col2.metric("Popularidad", f"{popularity}/100")
    
    st.success("¡Conexión establecida con éxito! Ya puedes ver los números reales.")

except Exception as e:
    st.error("⚠️ Sigue habiendo un problema de permiso (Error 401)")
    st.write("Esto significa que Spotify no reconoce tus llaves.")
    
    st.info("💡 **Haz esto para arreglarlo:**")
    st.write("1. Ve a tu **Spotify Developer Dashboard**.")
    st.write("2. Abre tu App y dale al botón **'Settings'**.")
    st.write("3. Dale clic a **'View Client Secret'** y asegúrate de que sea EXACTAMENTE: `9f90223ed60f46d2b5f39d3a1eb06c2e`.")
    st.write("4. Si es diferente, cópialo y cámbialo en la línea 10 de tu código en GitHub.")
