import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="LISA Discography Tracker", layout="wide")

st.title("🤳 LISA Stats Tracker")
st.markdown("Monitoreo de streams y popularidad diaria.")

# Simulación de base de datos (Aquí conectarías el script anterior)
data = {
    'Canción': ['Rockstar', 'New Woman', 'Moonlit Floor', 'LALISA', 'MONEY'],
    'Streams Diarios': [520000, 410000, 890000, 150000, 280000],
    'Cambio': [15000, -5000, 45000, 2000, -1000]
}

df = pd.DataFrame(data)

# Layout de métricas
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Top Song", "Moonlit Floor", "+12%")
with col2:
    st.metric("Total Daily Streams", "2.25M", "▲ 5.2%")
with col3:
    st.metric("Honduras Top Chart", "Puesto #34", "▲ 3")

# Gráfica de rendimiento
st.subheader("Rendimiento por Canción")
fig = px.bar(df, x='Canción', y='Streams Diarios', color='Cambio', 
             color_continuous_scale='RdYlGn', title="Flujo de Streams (24h)")
st.plotly_chart(fig, use_container_width=True)

# Tabla interactiva
st.dataframe(df.style.highlight_max(axis=0, subset=['Streams Diarios']))
