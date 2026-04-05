import streamlit as st
import pandas as pd
import requests
from io import StringIO
from datetime import datetime, timedelta

# 1. Configuración de la página
st.set_page_config(page_title="LISA Spotify Top 200 Tracker", layout="wide")

st.title("🏆 LISA Spotify Top 200 Tracker")
st.write("Datos extraídos directamente del Top 200 Global de Spotify")

# 🌎 LISTA DE PAÍSES PARA EL TOP 200
paises = {
    "Global": "global",
    "Honduras 🇭🇳": "hn",
    "Tailandia 🇹🇭": "th",
    "Brasil 🇧🇷": "br",
    "Estados Unidos 🇺🇸": "us",
    "Corea del Sur 🇰🇷": "kr",
    "México 🇲🇽": "mx",
    "España 🇪🇸": "es"
}

seleccion = st.selectbox("Selecciona el país para ver el Top 200:", list(paises.keys()))
codigo_pais = paises[seleccion]

# 2. FUNCIÓN PARA DESCARGAR EL TOP 200 REAL
def get_spotify_top_200(country):
    # Intentamos obtener el de ayer porque el de hoy a veces tarda en subir
    fecha_ayer = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    url = f"https://charts-csv.s3.us-east-1.amazonaws.com/regional/{country}/daily/latest/regional-{country}-daily-latest.csv"
    
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            # El CSV de Spotify tiene una línea de encabezado extra que hay que saltar
            csv_data = StringIO(response.text)
            df = pd.read_csv(csv_data)
            return df
        else:
            return None
    except:
        return None

# 3. PROCESAR Y FILTRAR
df_top = get_spotify_top_200(codigo_pais)

if df_top is not None:
    # Limpiamos nombres de columnas por si acaso
    df_top.columns = [c.lower().strip() for c in df_top.columns]
    
    # Buscamos a LISA en la columna de artista
    # (Usamos artist_names o artist según como venga el CSV)
    col_artista = 'artist_names' if 'artist_names' in df_top.columns else 'artist'
    col_cancion = 'track_name' if 'track_name' in df_top.columns else 'track'
    
    lisa_in_chart = df_top[df_top[col_artista].str.contains("LISA", case=False, na=False)]

    # MÉTRICAS
    st.write("---")
    c1, c2 = st.columns(2)
    c1.metric("Total Canciones en Top 200", len(df_top))
    c2.metric("Canciones de LISA hoy", len(lisa_in_chart))

    if not lisa_in_chart.empty:
        st.subheader(f"🔥 LISA en el Top 200 de {seleccion}")
        # Ajustamos los nombres para que se vean bien
        display_df = lisa_in_chart.copy()
        st.table(display_df[[col_cancion, col_artista, 'rank', 'streams']])
        st.success(f"¡LISA tiene {len(lisa_in_chart)} canciones en el chart de hoy!")
    else:
        st.warning(f"LISA no entró hoy en el Top 200 de {seleccion}. ¡A seguir haciendo stream!")
    
    # OPCIONAL: Ver el Top 10 general del país
    with st.expander("Ver el Top 10 General de este país"):
        st.dataframe(df_top.head(10))

else:
    st.error("No se pudo conectar con el servidor de Charts de Spotify.")
    st.info("A veces Spotify tarda en actualizar el archivo. Intenta de nuevo en unos minutos.")
