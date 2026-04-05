import streamlit as st
import pandas as pd
import requests
import base64

# 1. Configuración Visual
st.set_page_config(page_title="LISA Global Tracker", layout="wide")
st.title("🤳 LISA Global Spotify Tracker")

# 2. TUS LLAVES (Limpia cualquier espacio)
CID = 'f693630ca5df44fa8f10bbcd5fbc6830'.strip()
SEC = '5ebbe4d9a3b94065a9c7f321d471937c'.strip()

# 3. CONEXIÓN MANUAL (Sin librerías que fallen)
def get_access_token():
    auth_str = f"{CID}:{SEC}"
    b64_auth = base64.b64encode(auth_str.encode()).decode()
    
    headers = {"Authorization": f"Basic {b64_auth}"}
    data = {"grant_type": "client_credentials"}
    
    # USAMOS LA URL OFICIAL DIRECTA
    response = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=data)
    if response.status_code == 200:
        return response.json()['access_token']
    return None

token = get_access_token()

if token:
    headers = {"Authorization": f"Bearer {token}"}
    lisa_id = '5L1oOat9Y8mYvRsmVOSI0O'
    
    try:
        # Petición oficial de Artista
        artist_url = f"https://api.spotify.com/v1/artists/{lisa_id}"
        artist_data = requests.get(artist_url, headers=headers).json()
        
        # Petición oficial de Canciones
        tracks_url = f"https://api.spotify.com/v1/artists/{lisa_id}/top-tracks?market=US"
        tracks_data = requests.get(tracks_url, headers=headers).json()

        # Mostrar Métricas
        col1, col2 = st.columns(2)
        col1.metric("Seguidores Globales", f"{artist_data['followers']['total']:,}")
        col2.metric("Popularidad", f"{artist_data['popularity']}/100")

        st.write("---")
        st.subheader("🎵 Canciones Top")
        
        canciones = []
        for t in tracks_data['tracks']:
            canciones.append({
                "Canción": t['name'],
                "Popularidad": t['popularity'],
                "Álbum": t['album']['name']
            })
        
        st.table(pd.DataFrame(canciones))
        st.success("✅ ¡CONECTADO EXITOSAMENTE!")
        st.balloons()

    except Exception as e:
        st.error(f"Error al leer datos: {e}")
else:
    st.error("⚠️ Error de Token. Verifica que el Secret sea el nuevo en Spotify Dashboard.")
