import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Judul dashboard
st.title("Contoh Dashboard Streamlit")

# Sidebar
st.sidebar.header("Pengaturan")

# Pilihan untuk mengunggah file CSV
uploaded_file = st.sidebar.file_uploader("Unggah File CSV", type=["csv"])

# Dataframe untuk menampilkan data
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("Dataframe:", df)

# Pilihan visualisasi
st.sidebar.header("Visualisasi")
chart_type = st.sidebar.selectbox("Pilih Jenis Visualisasi", ["Grafik Batang", "Grafik Scatter"])
x = st.sidebar.selectbox("Pilih sumbu x", df.columns.tolist())
y = st.sidebar.selectbox("Pilih sumbu y", df.columns.tolist())

# Visualisasi
st.subheader("Visualisasi Data")
if chart_type == "Grafik Batang":
    st.bar_chart(df[[x, y]])
elif chart_type == "Grafik Scatter":
    st.line_chart(df[[x, y]])

# Pilihan statistik
st.sidebar.header("Statistik")
if st.sidebar.checkbox("Tampilkan Statistik"):
    st.subheader("Statistik Deskriptif")
    st.write(df.describe())

# Pilihan lainnya
st.sidebar.header("Pilihan Lainnya")
if st.sidebar.checkbox("Tampilkan Dataframe Lainnya"):
    st.subheader("Dataframe Lainnya")
    st.write(df)

# Menampilkan gambar
st.sidebar.header("Gambar")
st.image("https://www.example.com/sample_image.jpg", use_column_width=True)

# Menampilkan teks
st.sidebar.header("Teks")
st.write("Ini adalah contoh dashboard Streamlit sederhana.")

# Menampilkan HTML
st.sidebar.header("HTML")
st.markdown("<b>Ini adalah teks HTML tebal</b>", unsafe_allow_html=True)

# Menampilkan audio
st.sidebar.header("Audio")
audio_file = open("sample_audio.mp3", "rb")
st.audio(audio_file.read(), format="audio/mp3")

# Menampilkan video
st.sidebar.header("Video")
video_file = open("sample_video.mp4", "rb")
st.video(video_file.read(), format="video/mp4")

