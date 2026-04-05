import streamlit as st
import pandas as pd
import requests
import base64

# 1. Configuración de la página
st.set_page_config(page_title="LISA Global Tracker", layout="wide")
st.title("🤳 LISA Worldwide Charts Tracker")

# 2. Tus Llaves
CID = 'f693630ca5df44fa8f10bbcd5fbc6830'.strip()
SEC = '5ebbe4d9a3b94065a9c7f321d471937c'.strip()

def get_token():
    auth_url = "https://accounts.spotify.com/api/token"
    auth_str = f"{CID}:{SEC}"
    b64_auth = base64.b64encode(auth_str.encode()).decode()
    headers = {"Authorization": f"Basic {b64_auth}"}
    data = {"grant_type": "client_credentials"}
    res = requests.post(auth_url, headers=headers, data=data)
    return res.json().get('access_token') if res.status_code == 200 else None

token = get_token()

if token:
    headers = {"Authorization": f"Bearer {token}"}
    lisa_id = '5L1oOat9Y8mYvRsmVOSI0O'
    
    # Selector de Países
    st.subheader("🌎 Selecciona la Región")
    paises = {
        "Global": "US", 
        "Tailandia 🇹🇭": "TH", 
        "Honduras 🇭🇳": "HN", 
        "Brasil 🇧🇷": "BR", 
        "Corea del Sur 🇰🇷": "KR",
        "México 🇲🇽": "MX"
    }
    seleccion = st.selectbox("Ver ranking de:", list(paises.keys()))
    codigo_pais = paises[seleccion]

    try:
        # 1. Datos Generales (Seguidores)
        artist_data = requests.get(f"https://api.spotify.com/v1/artists/{lisa_id}", headers=headers).json()
        
        # 2. Datos por País Seleccionado
        tracks_res = requests.get(f"https://api.spotify.com/v1/artists/{lisa_id}/top-tracks?market={codigo_pais}", headers=headers).json()

        col1, col2 = st.columns(2)
        col1.metric("Seguidores Totales", f"{artist_data['followers']['total']:,}")
        col2.metric("Popularidad Global", f"{artist_data['popularity']}/100")

        st.write("---")
        st.subheader(f"🎵 Top Canciones en {seleccion}")
        
        canciones = []
        for t in tracks_res.get('tracks', []):
            canciones.append({
                "Canción": t['name'],
                "Popularidad Local": t['popularity'],
                "Álbum": t['album']['name'],
                "Preview": t['preview_url'] # Link para escuchar un pedacito
            })
        
        if canciones:
            df = pd.DataFrame(canciones)
            st.table(df[['Canción', 'Popularidad Local', 'Álbum']])
            
            # Gráfica de éxito local
            st.bar_chart(df.set_index("Canción")["Popularidad Local"])
        else:
            st.warning(f"LISA no tiene canciones en el Top 10 de {seleccion} hoy.")

    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.error("Error de conexión. Revisa tus llaves.")
