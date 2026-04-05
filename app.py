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

# 3. CONEXIÓN MANUAL (Directo a Spotify)
def get_access_token():
    auth_url = "https://accounts.spotify.com/api/token"
    auth_str = f"{CID}:{SEC}"
    b64_auth = base64.b64encode(auth_str.encode()).decode()
    
    headers = {"Authorization": f"Basic {b64_auth}"}
    data = {"grant_type": "client_credentials"}
    
    response = requests.post(auth_url, headers=headers, data=data)
    if response.status_code == 200:
        return response.json()['access_token']
    return None

token = get_access_token()

if token:
    headers = {"Authorization": f"Bearer {token}"}
    lisa_id = '5L1oOat9Y8mYvRsmVOSI0O' # ID oficial de LISA
    
    try:
        # Petición oficial de Artista
        artist_url = f"https://api.spotify.com/v1/artists/{lisa_id}"
        artist_res = requests.get(artist_url, headers=headers)
        artist_data = artist_res.json()
        
        # Petición oficial de Canciones
        tracks_url = f"https://api.spotify.com/v1/artists/{lisa_id}/top-tracks?market=US"
        tracks_res = requests.get(tracks_url, headers=headers)
        tracks_data = tracks_res.json()

        # Mostrar Métricas
        col1, col2 = st.columns(2)
        
        # Usamos .get() para que si no hay datos, no crashee
        f_count = artist_data.get('followers', {}).get('total', 0)
        pop_score = artist_data.get('popularity', 0)

        col1.metric("Seguidores Globales", f"{f_count:,}")
        col2.metric("Popularidad Global", f"{pop_score}/100")

        st.write("---")
        st.subheader("🎵 Canciones Top de LISA")
        
        canciones = []
        for t in tracks_data.get('tracks', []):
            canciones.append({
                "Canción": t['name'],
                "Popularidad": t['popularity'],
                "Álbum": t['album']['name']
            })
        
        if canciones:
            st.table(pd.DataFrame(canciones))
            st.success("✅ ¡CONECTADO EXITOSAMENTE!")
            st.balloons()
        else:
            st.warning("No se encontraron canciones en este momento.")

    except Exception as e:
        st.error(f"Hubo un detalle al procesar los datos: {e}")
else:
    st.error("⚠️ Error de Token. Verifica tus llaves en el Dashboard de Spotify.")
