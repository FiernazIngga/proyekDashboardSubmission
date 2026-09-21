import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from pathlib import Path

sns.set(style='dark')

def create_pm25_tahunan_df(df):
    pm25_tahunan_df = df.groupby("year")["PM2.5"].mean().reset_index()
    return pm25_tahunan_df

def create_pm25_stasiun_df(df):
    pm25_stasiun_df = (
        df.groupby("station")["PM2.5"]
        .mean()
        .sort_values(ascending=False)
        .reset_index()
    )
    return pm25_stasiun_df

def create_pm25_bulanan_df(df):
    pm25_bulanan_df = df.groupby("month")["PM2.5"].mean().reset_index()
    return pm25_bulanan_df

def create_pm25_jam_df(df):
    pm25_jam_df = df.groupby("hour")["PM2.5"].mean().reset_index()
    return pm25_jam_df

def create_korelasi_df(df):
    kolom_polusi = ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"]
    korelasi_df = df[kolom_polusi].corr()
    return korelasi_df

def create_kategori_stasiun_df(df):
    kategori_stasiun_df = (
        df.groupby("station")["PM2.5"].mean().reset_index()
    )
    bins = [0, 70, 80, float("inf")]
    labels = ["Rendah", "Sedang", "Tinggi"]
    kategori_stasiun_df["kategori"] = pd.cut(
        kategori_stasiun_df["PM2.5"],
        bins=bins,
        labels=labels
    )
    return kategori_stasiun_df

# Load data
BASE_DIR = Path(__file__).resolve().parent
all_df = pd.read_csv(BASE_DIR / "air_df.csv")

# Mengubah data menjadi datetime
all_df["date"] = pd.to_datetime(
    all_df[["year", "month", "day"]]
)
all_df.sort_values(by="date", inplace=True)
all_df.reset_index(drop=True, inplace=True)

# Mengambil tanggal minimum dan maksimum
min_date = all_df["date"].min()
max_date = all_df["date"].max()

with st.sidebar:
    # Menambahkan logo Dicoding (pada bagian ini sama seperti latihan yang dilaksanakan dalam modul kelas Fundamental Analisis Data)
    st.image(
        "https://github.com/dicodingacademy/assets/raw/main/logo.png"
    )
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Filter data berdasarkan tanggal
main_df = all_df[
    (all_df["date"] >= str(start_date)) &
    (all_df["date"] <= str(end_date))
]

# Membuat dataframe untuk masing-masing analisis
pm25_tahunan_df = create_pm25_tahunan_df(main_df)
pm25_stasiun_df = create_pm25_stasiun_df(main_df)
pm25_bulanan_df = create_pm25_bulanan_df(main_df)
pm25_jam_df = create_pm25_jam_df(main_df)
korelasi_df = create_korelasi_df(main_df)
kategori_stasiun_df = create_kategori_stasiun_df(main_df)

# Dashboard
st.header('Dashboard Kualitas Udara di Beijing :sparkles:')

# PM2.5
st.subheader('PM2.5 Overview')
col1, col2 = st.columns(2)

with col1:
    rata_rata_pm25 = main_df["PM2.5"].mean()
    st.metric(
        "Rata-rata PM2.5",
        value=f"{rata_rata_pm25:.2f}"
    )

with col2:
    pm25_tertinggi = main_df["PM2.5"].max()
    st.metric(
        "PM2.5 Tertinggi",
        value=f"{pm25_tertinggi:.2f}"
    )

# Grafik tren PM2.5
fig, ax = plt.subplots(figsize=(16, 8))

ax.plot(
    pm25_tahunan_df["year"],
    pm25_tahunan_df["PM2.5"],
    marker='o',
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
ax.set_xlabel("Tahun")
ax.set_ylabel("Rata-rata PM2.5")
ax.set_title("Tren Rata-rata PM2.5 Tahun 2013 - 2017", fontsize=25)
st.pyplot(fig)

# Stasius
st.subheader("Highest & Lowest PM2.5 Station")

fig, ax = plt.subplots(
    nrows=1,
    ncols=2,
    figsize=(35, 15)
)

colors = [
    "#90CAF9",
    "#D3D3D3",
    "#D3D3D3",
    "#D3D3D3",
    "#D3D3D3"
]

# Stasiun dengan PM2.5 tertinggi
sns.barplot(
    x="PM2.5",
    y="station",
    data=pm25_stasiun_df.head(5),
    palette=colors,
    ax=ax[0]
)
ax[0].set_ylabel(None)
ax[0].set_xlabel("Rata-rata PM2.5", fontsize=30)
ax[0].set_title("Stasiun PM2.5 Tertinggi", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)

# Stasiun dengan PM2.5 terendah
sns.barplot(
    x="PM2.5",
    y="station",
    data=pm25_stasiun_df.sort_values(
        by="PM2.5",
        ascending=True
    ).head(5),
    palette=colors,
    ax=ax[1]
)
ax[1].set_ylabel(None)
ax[1].set_xlabel("Rata-rata PM2.5", fontsize=30)
ax[1].set_title("Stasiun PM2.5 Terendah", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)
st.pyplot(fig)

# Pola Waktu
st.subheader("PM2.5 Patterns")
col1, col2 = st.columns(2)
# Pola berdasarkan bulan
with col1:
    fig, ax = plt.subplots(figsize=(20, 10))
    sns.lineplot(
        x="month",
        y="PM2.5",
        data=pm25_bulanan_df,
        marker="o",
        linewidth=2,
        color="#90CAF9",
        ax=ax
    )
    ax.set_title("Average PM2.5 by Month")
    ax.set_ylabel(None)
    ax.set_xlabel("Month")
    ax.tick_params(axis='x', labelsize=20)
    ax.tick_params(axis='y', labelsize=20)
    st.pyplot(fig)

# Pola berdasarkan jam
with col2:
    fig, ax = plt.subplots(figsize=(20, 10))
    sns.lineplot(
        x="hour",
        y="PM2.5",
        data=pm25_jam_df,
        marker="o",
        linewidth=2,
        color="#90CAF9",
        ax=ax
    )
    ax.set_title(
        "Average PM2.5 by Hour",
        loc="center",
        fontsize=30
    )
    ax.set_ylabel(None)
    ax.set_xlabel("Hour")
    ax.tick_params(axis='x', labelsize=20)
    ax.tick_params(axis='y', labelsize=20)
    st.pyplot(fig)

# Korelasi
st.subheader("Pollutant Correlation")
fig, ax = plt.subplots(figsize=(20, 10))
sns.heatmap(
    korelasi_df,
    annot=True,
    cmap="coolwarm",
    fmt=".2f",
    ax=ax
)
ax.set_title("Korelasi antara polusi udara")
st.pyplot(fig)

# Kategori Stasiun
st.subheader("Station Classification Based on PM2.5")
fig, ax = plt.subplots(figsize=(20, 10))
sns.barplot(x="PM2.5", y="station", hue="kategori",
    data=kategori_stasiun_df.sort_values(
        by="PM2.5",
        ascending=False
    ),
    ax=ax
)
ax.set_title(
    "Station Classification Based on Average PM2.5",
    loc="center",
    fontsize=30
)
ax.set_ylabel(None)
ax.set_xlabel("Average PM2.5", fontsize=20)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

# Tabel
st.subheader("Station Summary")
st.dataframe(
    kategori_stasiun_df.sort_values(
        by="PM2.5",
        ascending=False
    ),
    use_container_width=True
)

st.caption('Data dari dicoding')