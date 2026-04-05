import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

# 1. Configuración de la página
st.set_page_config(page_title="LISA Tracker", layout="wide")

# 2. Tus llaves de Spotify
CID = 'f693630ca5df44fa8f10bbcd5fbc6830'
SEC = '9f90223ed60f46d2b5f39d3a1eb06c2e'

# 3. Conexión segura
try:
    auth_manager = SpotifyClientCredentials(client_id=CID, client_secret=SEC)
    sp = spotipy.Spotify(auth_manager=auth_manager)
except Exception as e:
    st.error(f"Error de llaves: {e}")

st.title("LISA Discography Tracker")

try:
    # Buscamos canciones de LISA
    results = sp.search(q='artist:LISA', type='track')
    items = results['tracks']['items']
    
    datos_limpios = []
    
    for t in items:
        # Solo si es la LISA que buscamos
        if 'LISA' in t['artists'][0]['name'].upper():
            # USAMOS .get() PARA EVITAR EL ERROR DE 'POPULARITY'
            # Si no lo encuentra, pondrá un 0 en lugar de dar error
            pop = t.get('popularity', 0)
            
            datos_limpios.append({
                'Cancion': t['name'],
                'Popularidad': pop,
                'Album': t['album']['name']
            })
    
    # Creamos la tabla
    df = pd.DataFrame(datos_limpios)
    
    if not df.empty:
        # Quitamos canciones repetidas y ordenamos por las más famosas
        df = df.sort_values(by='Popularidad', ascending=False).drop_duplicates(subset=['Cancion'])
        
        # Métrica principal
        st.metric("Canción más popular hoy", df.iloc[0]['Cancion'], f"{df.iloc[0]['Popularidad']}/100")
        
        st.write("---")
        st.subheader("Estadísticas de Spotify")
        st.dataframe(df, use_container_width=True)
        st.success("¡Datos cargados correctamente!")
    else:
        st.warning("No se encontraron canciones en este momento.")

except Exception as e:
    # Este mensaje nos dirá exactamente qué línea está fallando
    st.error(f"Ocurrió un detalle técnico: {e}")
