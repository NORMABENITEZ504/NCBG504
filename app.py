import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

# 1. Configuracion de pagina
st.set_page_config(page_title="LISA Tracker", layout="wide")

# 2. Credenciales reales
CID = 'f693630ca5df44fa8f10bbcd5fbc6830'
SEC = '9f90223ed60f46d2b5f39d3a1eb06c2e'

# 3. Conexion
auth_manager = SpotifyClientCredentials(client_id=CID, client_secret=SEC)
sp = spotipy.Spotify(auth_manager=auth_manager)

st.title("LISA Discography Tracker")

try:
    # Busqueda simple sin limites ni filtros raros
    results = sp.search(q='LISA', type='track')
    tracks = results['tracks']['items']
    
    lista = []
    for t in tracks:
        # Filtro de seguridad para asegurar que sea la LISA de BLACKPINK
        if 'LISA' in t['artists'][0]['name'].upper():
            lista.append({
                'Cancion': t['name'],
                'Popularidad': t['popularity'],
                'Album': t['album']['name']
            })
    
    df = pd.DataFrame(lista)
    
    if not df.empty:
        # Ordenar por popularidad
        df = df.sort_values(by='Popularidad', ascending=False).drop_duplicates(subset=['Cancion'])
        
        # Mostrar datos
        st.metric("Cancion mas popular", df.iloc[0]['Cancion'], f"{df.iloc[0]['Popularidad']}/100")
        st.write("---")
        st.dataframe(df, use_container_width=True)
        st.success("Conexion establecida exitosamente")
    else:
        st.info("No se encontraron resultados para LISA")

except Exception as e:
    st.error(f"Error tecnico: {e}")
