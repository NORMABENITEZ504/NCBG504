import streamlit as st
import pandas as pd

# --- CONFIGURACIÓN TEMPORAL (Aquí irán tus códigos reales luego) ---
CLIENT_ID = 'TU_CLIENT_ID_PROVISIONAL'
CLIENT_SECRET = 'TU_CLIENT_SECRET_PROVISIONAL'

st.set_page_config(page_title="LISA Discography Tracker", layout="wide")

st.title("🤳 LISA Stats Tracker")
st.subheader("Monitoreo de la discografía de Lisa")

# Datos de ejemplo para que veas cómo funciona el aumento/disminución
data = {
    'Canción': ['Rockstar', 'New Woman', 'Moonlit Floor', 'LALISA', 'MONEY'],
    'Streams Diarios': [520000, 410000, 890000, 150000, 280000],
    'Cambio (vs Ayer)': ['▲ 15,000', '▼ 5,000', '▲ 45,000', '▲ 2,000', '▼ 1,000']
}

df = pd.DataFrame(data)

# Mostrar métricas rápidas
col1, col2 = st.columns(2)
with col1:
    st.metric("Top en Honduras 🇭🇳", "Rockstar", "Puesto #34")
with col2:
    st.metric("Más escuchada hoy", "Moonlit Floor", "+12%")

st.write("---")
st.write("### Estado de la discografía")
st.table(df)

st.info("Nota: Los datos reales se actualizarán cuando conectes tu Client ID de Spotify.")
