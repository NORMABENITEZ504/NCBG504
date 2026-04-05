import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

# 1. Configuracion de la pagina
st.set_page_config(page_title="LISA Tracker", layout="wide")

# 2. Tus llaves de Spotify
CID = 'f693630ca5df44fa8f10bbcd5fbc6830'
SEC = '9f90223ed60f46d2b5f39d3a1eb06c2e'

# 3. Conexion segura
auth_manager = SpotifyClientCredentials(client_id=CID, client_secret=SEC)
sp = spotipy.Spotify(auth_manager=auth_manager)

st.title("LISA Discography Tracker")

try:
    # Buscamos canciones de LISA
    results = sp.search(q='artist:LISA', type='track')
    items = results['tracks']['items']
    
    datos_limpios = []
    
    for t in items:
        # Solo si es la LISA que buscamos
        if 'LISA' in t['artists'][0]['name'].upper():
            datos_limpios.append({
                'Track': t['name'],
                'Popularity_Score': t['popularity'], # Usamos el nombre que Spotify entiende
                'Album_Name': t['album']['name']
            })
    
    # Creamos la tabla
    df = pd.DataFrame(datos_limpios)
    
    if not df.empty:
        # Quitamos canciones repetidas y ordenamos
        df = df.sort_values(by='Popularity_Score', ascending=False).drop_duplicates(subset=['Track'])
        
        # Mostramos la cancion mas top
        top_name = df.iloc[0]['Track']
        top_score = df.iloc[0]['Popularity_Score']
        st.metric("Cancion mas popular", top_name, f"{top_score}/100")
        
        st.write("---")
        # Cambiamos los nombres de la tabla para que se vean bonitos en tu web
        df.columns = ['Cancion', 'Popularidad', 'Album']
        st.dataframe(df, use_container_width=True)
        st.success("¡Conectado exitosamente!")
    else:
        st.warning("No se encontraron canciones. Reintenta en unos segundos.")

except Exception as e:
    # Este mensaje te dira exactamente que palabra esta fallando si vuelve a ocurrir
    st.error(f"Error en los datos: {e}")
