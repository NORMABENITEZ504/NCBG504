import streamlit as st
import pandas as pd
import requests

# 1. Configuración Visual
st.set_page_config(page_title="LISA Global Tracker", layout="wide")

st.markdown("""
<style>
    .main {background-color: #0e1117;}
    .stMetric {background-color: #1a1c23; border: 1px solid #ff007f; padding: 15px; border-radius: 10px;}
    h1 {color: #ff007f; text-shadow: 2px 2px #000;}
</style>
""", unsafe_allow_html=True)

st.title("🤳 LISA Global Spotify Tracker PRO")

# 2. Tus Llaves (Sin espacios)
CID = 'f693630ca5df44fa8f10bbcd5fbc6830'.strip()
SEC = '9f90223ed60f46d2b5f39d3a1eb06c2e'.strip()

# 3. Función para obtener el Token (La llave de acceso)
def get_token():
    auth_url = 'https://accounts.spotify.com/api/token'
    data = {'grant_type': 'client_credentials'}
    auth_response = requests.post(auth_url, auth=(CID, SEC), data=data)
    if auth_response.status_code != 200:
        return None
    return auth_response.json().get('access_token')

token = get_token()

if token:
    headers = {'Authorization': f'Bearer {token}'}
    # ID de LISA
    lisa_id = '5L1oOat9Y8mYvRsmVOSI0O'
    
    try:
        # Petición 1: Datos de la Artista
        artist_res = requests.get(f'https://api.spotify.com/v1/artists/{lisa_id}', headers=headers).json()
        
        # Petición 2: Canciones Top
        tracks_res = requests.get(f'https://api.spotify.com/v1/artists/{lisa_id}/top-tracks?market=US', headers=headers).json()

        # Mostrar Métricas
        col1, col2 = st.columns(2)
        col1.metric("Seguidores Globales", f"{artist_res['followers']['total']:,}")
        col2.metric("Popularidad Global", f"{artist_res['popularity']}/100")

        st.write("---")
        st.subheader("🏆 Top Canciones Globales")

        # Procesar canciones
        tracks_data = []
        for track in tracks_res['tracks']:
            tracks_data.append({
                "Canción": track['name'],
                "Popularidad": track['popularity'],
                "Álbum": track['album']['name'],
                "Fecha": track['album']['release_date']
            })
        
        df = pd.DataFrame(tracks_data)
        st.dataframe(df, use_container_width=True)
        
        # Gráfica
        st.bar_chart(df.set_index("Canción")["Popularidad"])
        st.success("✅ Datos sincronizados con el servidor global de Spotify")

    except Exception as e:
        st.error(f"Error al leer los datos: {e}")
else:
    st.error("⚠️ Error de Autorización (401)")
    st.info("Tus llaves CID o SEC no son válidas. Revisa tu Dashboard de Spotify.")
