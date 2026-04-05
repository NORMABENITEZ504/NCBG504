import streamlit as st
import pandas as pd
import requests
import os
from datetime import datetime

st.set_page_config(page_title="LISA Charts Tracker", layout="wide")

st.title("🌍 LISA Spotify Charts Tracker")

# CONFIG
artist_name = "LISA"
countries = ["global", "us", "gb", "kr", "th", "br"]

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

    if df is not None:
        # Filtrar canciones de LISA
        lisa_tracks = df[df['Artist'].str.contains("LISA", case=False)]

        for _, row in lisa_tracks.iterrows():
            all_results.append({
                "date": datetime.now(),
                "country": country.upper(),
                "track": row["Track Name"],
                "position": row["Position"],
                "streams": row["Streams"]
            })

new_df = pd.DataFrame(all_results)

# --------------------------
# COMPARAR CON HISTORIAL
# --------------------------
if not history.empty:
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
        elif row["position"] == row["position_old"]:
            return "➖ Same"
        else:
            return "?"

    merged["status"] = merged.apply(get_status, axis=1)

else:
    merged = new_df.copy()
    merged["status"] = "🆕 New"

# --------------------------
# DETECTAR RE-ENTRY
# --------------------------
if not history.empty:
    old_tracks = history["track"].unique()
    merged["re_entry"] = merged.apply(
        lambda x: "🔁 Re-entry" if x["track"] in old_tracks and pd.isna(x["position_old"]) else "",
        axis=1
    )
else:
    merged["re_entry"] = ""

# --------------------------
# GUARDAR HISTORIAL
# --------------------------
final_history = pd.concat([history, new_df], ignore_index=True)
final_history.to_csv(file, index=False)

# --------------------------
# MOSTRAR DATA
# --------------------------
st.subheader("📊 Charts actuales")

st.dataframe(merged[[
    "country", "track", "position", "streams", "status", "re_entry"
]])

# --------------------------
# TOP STATS
# --------------------------
st.subheader("🔥 Estadísticas")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total apariciones", len(merged))

with col2:
    st.metric("Mejor posición", merged["position"].min())

with col3:
    st.metric("Total streams", f"{merged['streams'].sum():,}")

# --------------------------
# GRÁFICA
# --------------------------
st.subheader("📈 Streams por canción")

chart_df = merged.groupby("track")["streams"].sum().reset_index()
st.bar_chart(chart_df.set_index("track"))

st.success("Charts actualizados 🚀")
