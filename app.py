import streamlit as st
import pandas as pd
import requests
from io import StringIO
import os
from datetime import datetime

# --------------------------
# CONFIG UI (FANBASE STYLE)
# --------------------------
st.set_page_config(page_title="LISA Charts PRO", layout="wide")

st.markdown("""
<style>
body {background-color: #0b0b0b; color: white;}
.stMetric {background-color: #111; padding: 10px; border-radius: 10px;}
</style>
""", unsafe_allow_html=True)

st.title("🌍 LISA Spotify Charts Tracker PRO")

# --------------------------
# CONFIG
# --------------------------
artist_name = "LISA"
countries = ["global", "us", "gb", "kr", "th", "br"]

# --------------------------
# GET CHART (FIX REAL)
# --------------------------
def get_chart(country):
    url = f"https://spotifycharts.com/regional/{country}/daily/latest/download"

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://spotifycharts.com/"
    }

    try:
        res = requests.get(url, headers=headers)

        if res.status_code != 200:
            return None

        data = StringIO(res.text)
        df = pd.read_csv(data)

        df.columns = df.columns.str.strip()
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

today = datetime.now().date()

# evitar duplicados del mismo día
if not history.empty:
    history["date"] = pd.to_datetime(history["date"]).dt.date
    history = history[history["date"] != today]

# --------------------------
# EXTRAER DATA
# --------------------------
all_results = []

for country in countries:
    df = get_chart(country)

    if df is None:
        st.warning(f"⚠️ No se pudo cargar {country}")
        continue

    # detectar columnas
    cols = {c.lower(): c for c in df.columns}

    artist_col = [c for c in df.columns if "artist" in c.lower()][0]
    track_col = [c for c in df.columns if "track" in c.lower()][0]
    streams_col = [c for c in df.columns if "stream" in c.lower()][0]
    position_col = [c for c in df.columns if "position" in c.lower()][0]

    # filtrar LISA
    lisa_df = df[df[artist_col].str.contains("LISA", case=False, na=False)]

    for _, row in lisa_df.iterrows():
        all_results.append({
            "date": today,
            "country": country.upper(),
            "track": row[track_col],
            "position": int(row[position_col]),
            "streams": int(row[streams_col])
        })

new_df = pd.DataFrame(all_results)

if new_df.empty:
    st.warning("No hay entradas de LISA hoy.")
    st.stop()

# --------------------------
# COMPARACIÓN
# --------------------------
if not history.empty:
    merged = pd.merge(
        new_df,
        history,
        on=["country", "track"],
        how="left",
        suffixes=("", "_old")
    )

    def status(row):
        if pd.isna(row["position_old"]):
            return "🆕 NEW"
        elif row["position"] < row["position_old"]:
            return "⬆️ UP"
        elif row["position"] > row["position_old"]:
            return "⬇️ DOWN"
        else:
            return "➖ SAME"

    merged["status"] = merged.apply(status, axis=1)

    old_tracks = history["track"].unique()

    merged["reentry"] = merged.apply(
        lambda x: "🔁 RE-ENTRY"
        if x["track"] in old_tracks and pd.isna(x["position_old"])
        else "",
        axis=1
    )

else:
    merged = new_df.copy()
    merged["status"] = "🆕 NEW"
    merged["reentry"] = ""

# --------------------------
# GUARDAR HISTORIAL
# --------------------------
history = pd.concat([history, new_df], ignore_index=True)
history.to_csv(file, index=False)

# --------------------------
# ALERTAS FANBASE 🔥
# --------------------------
st.subheader("🚨 ALERTAS")

alerts = []

for _, row in merged.iterrows():
    if row["status"] == "🆕 NEW":
        alerts.append(
            f"🆕 {row['track']} debuta en #{row['position']} en {row['country']} con {row['streams']:,} streams"
        )

    if row["reentry"] == "🔁 RE-ENTRY":
        alerts.append(
            f"🔁 {row['track']} re-ingresa en #{row['position']} en {row['country']} con {row['streams']:,} streams"
        )

    if row["status"] == "⬆️ UP":
        alerts.append(
            f"⬆️ {row['track']} sube a #{row['position']} en {row['country']}"
        )

# mostrar alertas
if alerts:
    for a in alerts[:10]:
        st.success(a)
else:
    st.info("Sin cambios importantes hoy.")

# --------------------------
# MÉTRICAS
# --------------------------
st.subheader("📊 RESUMEN GLOBAL")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Entradas", len(merged))

with col2:
    st.metric("Mejor posición", int(merged["position"].min()))

with col3:
    st.metric("Total streams", f"{merged['streams'].sum():,}")

# --------------------------
# RANKING GLOBAL
# --------------------------
st.subheader("🏆 RANKING GLOBAL")

ranking = merged.groupby("track")["streams"].sum().reset_index()
ranking = ranking.sort_values(by="streams", ascending=False)

st.dataframe(ranking, use_container_width=True)

# --------------------------
# TABLA COMPLETA
# --------------------------
st.subheader("📋 Charts completos")

st.dataframe(
    merged[["country", "track", "position", "streams", "status", "reentry"]],
    use_container_width=True
)

# --------------------------
# GRÁFICA GLOBAL
# --------------------------
st.subheader("📈 Streams por canción")

st.bar_chart(ranking.set_index("track"))

# --------------------------
# GRÁFICAS POR PAÍS
# --------------------------
st.subheader("🌎 Charts por país")

for country in merged["country"].unique():
    st.write(f"### {country}")
    df_c = merged[merged["country"] == country]

    st.bar_chart(df_c.set_index("track")["streams"])

st.success("🔥 Tracker PRO actualizado correctamente")
