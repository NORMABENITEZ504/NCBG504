import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="LISA Charts Tracker", layout="wide")

st.title("🌍 LISA Spotify Charts Tracker")

# CONFIG
artist_name = "LISA"
countries = ["global", "us", "gb", "kr", "th", "br"]

# --------------------------
# FUNCIÓN PARA OBTENER CHART
# --------------------------
def get_chart(country):
    url = f"https://spotifycharts.com/regional/{country}/daily/latest/download"
    try:
        df = pd.read_csv(url)
        return df
    except:
        return None

# --------------------------
# HISTORIAL
# --------------------------
file = "charts_history.csv"

if os.path.exists(file):
    history = pd.read_csv(file)
else:
    history = pd.DataFrame()

all_results = []

# --------------------------
# PROCESAR CADA PAÍS
# --------------------------
for country in countries:
    df = get_chart(country)

    if df is None:
        continue

    # 🔧 LIMPIAR COLUMNAS
    df.columns = df.columns.str.strip()

    # 🔍 DETECTAR COLUMNAS DINÁMICAMENTE
    artist_col = None
    track_col = None
    streams_col = None
    position_col = None

    for col in df.columns:
        col_lower = col.lower()
        if "artist" in col_lower:
            artist_col = col
        elif "track" in col_lower:
            track_col = col
        elif "stream" in col_lower:
            streams_col = col
        elif "position" in col_lower:
            position_col = col

    # ⚠️ VALIDACIÓN
    if not all([artist_col, track_col, streams_col, position_col]):
        st.warning(f"⚠️ Columnas no detectadas correctamente en {country}")
        st.write(df.columns)
        continue

    # 🎯 FILTRAR LISA
    lisa_tracks = df[df[artist_col].str.contains("LISA", case=False, na=False)]

    for _, row in lisa_tracks.iterrows():
        all_results.append({
            "date": datetime.now(),
            "country": country.upper(),
            "track": row[track_col],
            "position": int(row[position_col]),
            "streams": int(row[streams_col])
        })

# --------------------------
# DATAFRAME NUEVO
# --------------------------
new_df = pd.DataFrame(all_results)

if new_df.empty:
    st.warning("No se encontraron canciones de LISA en los charts hoy.")
    st.stop()

# --------------------------
# COMPARAR CON HISTORIAL
# --------------------------
if not history.empty:
    history["date"] = pd.to_datetime(history["date"], errors="coerce")

    merged = pd.merge(
        new_df,
        history,
        on=["country", "track"],
        how="left",
        suffixes=("", "_old")
    )

    def get_status(row):
        if pd.isna(row["position_old"]):
            return "🆕 New"
        elif row["position"] < row["position_old"]:
            return "⬆️ Up"
        elif row["position"] > row["position_old"]:
            return "⬇️ Down"
        else:
            return "➖ Same"

    merged["status"] = merged.apply(get_status, axis=1)

    # 🔁 RE-ENTRY
    old_tracks = history["track"].unique()

    merged["re_entry"] = merged.apply(
        lambda x: "🔁 Re-entry"
        if (x["track"] in old_tracks and pd.isna(x["position_old"]))
        else "",
        axis=1
    )

else:
    merged = new_df.copy()
    merged["status"] = "🆕 New"
    merged["re_entry"] = ""

# --------------------------
# GUARDAR HISTORIAL
# --------------------------
final_history = pd.concat([history, new_df], ignore_index=True)
final_history.to_csv(file, index=False)

# --------------------------
# MOSTRAR TABLA
# --------------------------
st.subheader("📊 Charts actuales")

st.dataframe(
    merged[["country", "track", "position", "streams", "status", "re_entry"]],
    use_container_width=True
)

# --------------------------
# ESTADÍSTICAS
# --------------------------
st.subheader("🔥 Estadísticas globales")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total apariciones", len(merged))

with col2:
    st.metric("Mejor posición", int(merged["position"].min()))

with col3:
    st.metric("Total streams", f"{merged['streams'].sum():,}")

# --------------------------
# TOP TRACK
# --------------------------
top_track = merged.loc[merged["streams"].idxmax()]

st.info(
    f"🏆 Top canción: **{top_track['track']}** "
    f"con {top_track['streams']:,} streams en {top_track['country']}"
)

# --------------------------
# GRÁFICA GLOBAL
# --------------------------
st.subheader("📈 Streams por canción")

chart_df = merged.groupby("track")["streams"].sum().reset_index()
st.bar_chart(chart_df.set_index("track"))

# --------------------------
# GRÁFICAS POR PAÍS
# --------------------------
st.subheader("🌎 Charts por país")

for country in merged["country"].unique():
    st.write(f"### {country}")

    df_country = merged[merged["country"] == country]

    st.bar_chart(
        df_country.set_index("track")["streams"]
    )

st.success("🚀 Tracker actualizado correctamente")
