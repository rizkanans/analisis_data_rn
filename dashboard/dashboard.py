import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import numpy as np

# Konfigurasi Layout
st.set_page_config(page_title="Air Quality Dashboard", layout="wide")

# Judul Dashboard
st.title("🌍 Air Quality Dashboard")
st.markdown("Dibuat dengan ❤️ oleh Data Analyst")

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("dashboard/main_data.csv")  # Pastikan file ada di direktori yang benar
    df["date"] = pd.to_datetime(df["year"].astype(str) + "-" + df["month"].astype(str) + "-" + df["day"].astype(str) + " " + df["hour"].astype(str) + ":00")
    return df

df = load_data()

# Sidebar untuk Filter Data
st.sidebar.header("📌 Filter Data")
selected_year = st.sidebar.selectbox("Pilih Tahun", df["year"].unique())
selected_month = st.sidebar.selectbox("Pilih Bulan", df["month"].unique())

# Filter Data berdasarkan Pilihan User
filtered_df = df[(df["year"] == selected_year) & (df["month"] == selected_month)]

# --- **Statistik Umum** ---
st.subheader("📊 Statistik Umum")
st.write(filtered_df.describe())

# --- **Tren PM2.5 dari Bulan ke Bulan** ---
st.subheader("📈 Tren PM2.5 dari Bulan ke Bulan")
pm25_trend = df.groupby(["year", "month"])["PM2.5"].mean().reset_index()
pm25_trend["month_year"] = pm25_trend["year"].astype(str) + "-" + pm25_trend["month"].astype(str)

# Plot Tren PM2.5
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(data=pm25_trend, x="month_year", y="PM2.5", marker="o", ax=ax)
plt.xticks(rotation=45)
plt.xlabel("Bulan")
plt.ylabel("PM2.5")
st.pyplot(fig)

# --- **Scatterplot PM2.5 vs Dew Point Temperature** ---
st.subheader("🌡️ Hubungan Dew Point Temperature dan PM2.5")
fig, ax = plt.subplots(figsize=(8, 5))
sns.scatterplot(data=df, x="DEWP", y="PM2.5", alpha=0.5, ax=ax)
plt.xlabel("Dew Point Temperature (°C)")
plt.ylabel("PM2.5")
st.pyplot(fig)

# --- **Perbandingan Polusi Weekday vs Weekend** ---
st.subheader("📅 Perbandingan PM2.5: Weekday vs Weekend")
df["day_of_week"] = df["date"].dt.day_name()
df["is_weekend"] = df["day_of_week"].isin(["Saturday", "Sunday"])
df_weekend = df.groupby("is_weekend")["PM2.5"].mean().reset_index()

fig, ax = plt.subplots(figsize=(6, 4))
sns.barplot(data=df_weekend, x="is_weekend", y="PM2.5", palette="viridis", ax=ax)
plt.xticks(ticks=[0, 1], labels=["Weekday", "Weekend"])
plt.xlabel("Hari")
plt.ylabel("PM2.5")
st.pyplot(fig)

# --- **Geospatial Analysis: Distribusi Polusi Udara** ---
st.subheader("🗺️ Geospatial Analysis: Peta Distribusi Polusi Udara")

# Contoh data latitude dan longitude (asumsi dataset memiliki lokasi stasiun)
stations_geo = pd.DataFrame({
    "station": df["station"].unique(),
    "latitude": np.random.uniform(39.8, 40.1, len(df["station"].unique())),
    "longitude": np.random.uniform(116.2, 116.6, len(df["station"].unique()))
})

# Gabungkan dengan rata-rata PM2.5
geo_data = df.groupby("station")["PM2.5"].mean().reset_index()
geo_data = geo_data.merge(stations_geo, on="station")

# Plot peta dengan Plotly
fig = px.scatter_mapbox(geo_data, lat="latitude", lon="longitude", color="PM2.5",
                        size="PM2.5", hover_name="station", zoom=10,
                        mapbox_style="carto-positron", color_continuous_scale="Plasma")
st.plotly_chart(fig)

# --- **Informasi Tambahan** ---
st.markdown("---")
st.markdown("📌 **Air Quality Dashboard** | Data dari Aotizhongxin.csv")
