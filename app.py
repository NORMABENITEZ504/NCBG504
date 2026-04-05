import streamlit as st
import pandas as pd
import requests
import base64

# 1. Configuración de la página
st.set_page_config(page_title="LISA Worldwide Tracker", layout="wide")
st.title("🤳 LISA Worldwide Charts Tracker")

# 2. Tus Llaves (Verificadas)
CID = 'f693630ca5df44fa8f10bbcd5fbc6830'.strip()
SEC = '5ebbe4d9a3b94065a9c7f321d471937c'.strip()

def get_token():
    try:
        auth_url = "https://accounts.spotify.com/api/token"
        auth_str = f"{CID}:{SEC}"
        b64_auth = base64.b64encode(auth_str.encode()).decode()
        headers = {"Authorization": f"Basic {b64_auth}"}
        data = {"grant_type": "client_credentials"}
        res = requests.post(auth_url, headers=headers, data=data)
        return res.json().get('access_token')
    except:
        return None

token = get_token()

if token:
    headers = {"Authorization": f"Bearer {token}"}
    lisa_id = '5L1oOat9Y8mYvRsmVOSI0O'
    
    # 🌎 LISTA DE PAÍSES AMPLIADA
    st.subheader("🌎 Selecciona la Región para ver el Chart")
    paises = {
        "Global (Mundo)": "US", 
        "Tailandia 🇹🇭": "TH", 
        "Honduras 🇭🇳": "HN", 
        "Brasil 🇧🇷": "BR", 
        "Corea del Sur 🇰🇷": "KR",
        "México 🇲🇽": "MX",
        "España 🇪🇸": "ES",
        "Argentina 🇦🇷": "AR",
        "Francia 🇫🇷": "FR"
    }
    seleccion = st.selectbox("Ver ranking de:", list(paises.keys()))
    codigo_pais = paises[seleccion]

    try:
        # 1. Pedir datos de la artista (con seguro por si falla 'followers')
        artist_res = requests.get(f"https://api.spotify.com/v1/artists/{lisa_id}", headers=headers).json()
        
        # 2. Pedir Top Tracks del país seleccionado
        tracks_res = requests.get(f"https://api.spotify.com/v1/artists/{lisa_id}/top-tracks?market={codigo_pais}", headers=headers).json()

        # Mostrar métricas con protección
        col1, col2 = st.columns(2)
        f_total = artist_res.get('followers', {}).get('total', 0)
        pop_total = artist_res.get('popularity', 0)
        
        col1.metric("Seguidores Globales", f"{f_total:,}")
        col2.metric(f"Popularidad en {seleccion}", f"{pop_total}/100")

        st.write("---")
        
        # Procesar canciones
        canciones = []
        for t in tracks_res.get('tracks', []):
            canciones.append({
                "Canción": t['name'],
                "Popularidad Local": t['popularity'],
                "Álbum": t['album']['name']
            })
        
        if canciones:
            df = pd.DataFrame(canciones)
            st.subheader(f"🎵 Top Hits de LISA en {seleccion}")
            st.table(df)
            st.bar_chart(df.set_index("Canción")["Popularidad Local"])
        else:
            st.warning(f"LISA no aparece en el Top 10 de {seleccion} en este momento.")

    except Exception as e:
        st.error(f"Hubo un problema al cargar los datos: {e}")
else:
    st.error("Error de conexión. Por favor, dale a 'Reboot App' en Streamlit.")
