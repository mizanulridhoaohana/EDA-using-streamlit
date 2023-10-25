import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px 
import copy
import plotly.graph_objects as go
from plotly.subplots import make_subplots 


# Judul dashboard
st.title("Exploratory Data Analytics")

# Sidebar
st.sidebar.header("Pengaturan")

# Pilihan untuk mengunggah file CSV
# uploaded_file = st.sidebar.file_uploader("Unggah File CSV", type=["csv"])

# Dataframe untuk menampilkan data
df = pd.read_csv('./dataset/dataset_normalization.csv')

# Tampilkan dataset
st.sidebar.header("Dataset")
if st.sidebar.checkbox("Tampilkan Dataframe"):
    st.subheader("Dataframe")
    st.write(df)

# Pilihan statistik
st.sidebar.header("Statistik")
if st.sidebar.checkbox("Tampilkan Statistik"):
    st.subheader("Statistik Deskriptif")
    st.write(df.describe())

# Pilihan visualisasi
st.sidebar.header("Visualisasi")
chart_type = st.sidebar.selectbox("Pilih Jenis Visualisasi", ["Pilih Kategori","Correlation", "Casual Rental per Season",
                                                              "Casual Rental by Season and Year", "Casual Rental per Month",
                                                              "Casual Rental by Hour and Season","Casual Rental per Holiday",
                                                              "Casual Rental per Work Day"])

chart_comparation = st.sidebar.selectbox("Komparasi penggunan Casual vs Registered User", 
                                         ["Temperature","Humidity"])
# Preprocessing
hour_df = copy.copy(df)

hour_df['s1_daylight_hrs'] = hour_df.apply(lambda x: 1 if (x['hour'] > 7 and x['hour'] < 19 and x['season'] == 1) else 0, axis=1)
hour_df['s2_daylight_hrs'] = hour_df.apply(lambda x: 1 if (x['hour'] > 6 and x['hour'] < 20 and x['season'] == 2) else 0, axis=1)
hour_df['s3_daylight_hrs'] = hour_df.apply(lambda x: 1 if (x['hour'] > 5 and x['hour'] < 21 and x['season'] == 3) else 0, axis=1)
hour_df['s4_daylight_hrs'] = hour_df.apply(lambda x: 1 if (x['hour'] > 7 and x['hour'] < 19 and x['season'] == 4) else 0, axis=1)

hour_df['midnight'] = np.where(hour_df['hour'].between(23, 2, inclusive='right'), 1, 0)
hour_df['early_morning'] = np.where(hour_df['hour'].between(2, 6, inclusive='right'), 1, 0)
hour_df['morning'] = np.where(hour_df['hour'].between(6, 9, inclusive='right'), 1, 0)
hour_df['late_morning'] = np.where(hour_df['hour'].between(9, 12, inclusive='right'), 1, 0)
hour_df['afternoon'] = np.where(hour_df['hour'].between(12, 16, inclusive='right'), 1, 0)
hour_df['late_afternoon'] = np.where(hour_df['hour'].between(16, 17, inclusive='right'), 1, 0)
hour_df['early_evening'] = np.where(hour_df['hour'].between(17, 19, inclusive='right'), 1, 0)
hour_df['evening'] = np.where(hour_df['hour'].between(19, 21, inclusive='right'), 1, 0)
hour_df['late_evening'] = np.where(hour_df['hour'].between(21, 23, inclusive='right'), 1, 0)


# Visualisasi
st.subheader("Visualisasi Data")
if chart_type == "Correlation":
    st.write("Analisis Korelasi")
    
    df_2=df.drop(['weekday'], axis=1)
    corr = df_2.corr()
    plt.figure(figsize=(12, 8))
    st.dataframe(corr.style.background_gradient(cmap='coolwarm'))

    st.write("Korelasi terkuat dengan pengguna kasual adalah suhu, diikuti oleh fitur-fitur per jam. Kelembaban dan hari kerja adalah fitur-fitur yang paling berkorelasi negatif dengan pengguna kasual, yang mengindikasikan bahwa peningkatan kelembaban akan berdampak buruk pada penyewaan sepeda oleh pengguna kasual. Dan itu wajar. \n\n Korelasi terkuat dengan pengguna terdaftar juga serupa, tetapi dengan variabel per jam yang sedikit lebih tinggi dibandingkan dengan suhu. Hari kerja memiliki korelasi yang lebih tinggi dengan pengguna terdaftar, mungkin karena berbagi perjalanan selama berkomute. Kelembaban tidak memiliki korelasi negatif yang begitu kuat dengan pengguna terdaftar, yang mungkin merupakan indikasi lain bahwa pengguna terdaftar menggunakan sepeda selama berkomute. \n\n Ada korelasi yang kuat dan jelas antara pengguna terdaftar dan jumlah penyewaan, tetapi yang saya ingin lakukan di sini adalah melihat kondisi terbaik untuk penggunaan kasual. Jika pengguna kasual dapat diubah menjadi pengguna terdaftar, itu akan menjadi hal yang baik. Meskipun pengguna kasual mungkin lebih suka menyewa sepeda secara santai (seperti penggunaan akhir pekan), akan menarik untuk melihat perbedaan-perbedaan yang ada.")

elif chart_type == "Casual Rental per Season":
    st.write("Berikut adalah data untuk Casual Rental per Season")

    # Data
    season_registered = hour_df.groupby(['season'])['registered'].sum()
    season_casual = hour_df.groupby(['season'])['casual'].sum()
    season_registered = season_registered / season_registered.sum()
    season_casual = season_casual / season_casual.sum()

    season_registered = season_registered.reset_index()
    season_casual = season_casual.reset_index()
    season_casual

    st.write('Visualisasi dalam bentuk grafik:')

    seasons = season_casual['season']
    casual_rentals = season_casual['casual']
    registered_rentals = season_registered['registered']

    # Create a Matplotlib figure
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(seasons, casual_rentals, label='Casual', color='#564E95', linewidth=4)
    ax.plot(seasons, registered_rentals, label='Registered', color='#F1D31F', linewidth=4)

    ax.set_title('Casual vs. Registered rentals per season')
    ax.set_xlabel('Season')
    ax.set_ylabel('Rentals')

    ax.legend()
    ax.grid(True)

    # Display the Matplotlib figure using Streamlit
    st.pyplot(fig)

    st.write("Dengan jumlah total penggunaan baik pengguna terdaftar maupun pengguna kasual divisualisasikan, kita dapat melihat bahwa penggunaan terdaftar lebih tinggi jika dibandingkan dengan penggunaan kasual pada bulan-bulan yang lebih dingin, yang mulai meningkat pada musim 3 dan 4. Musim 2 mengalami peningkatan sekitar 20% dalam penggunaan kasual dibandingkan dengan penggunaan terdaftar untuk musim yang sama.")

elif chart_type == "Casual Rental by Season and Year":
    st.write("Berikut adalah data untuk Casual Rental by Season and Year")

    df_casual_avg = hour_df.groupby(['season', 'year']).agg({'casual': 'mean'}).reset_index()
    df_casual_avg.rename(columns={'casual': 'casual_avg'}, inplace=True)
    df_casual_avg

    st.write('Visualisasi dalam bentuk grafik:')
    
    # Data
    seasons = [1, 2, 3, 4]
    year_0_data = [10.360251, 35.208352, 42.611607, 24.748360]
    year_1_data = [18.029899, 57.097915, 57.908245, 36.686845]

    # Create a Matplotlib figure
    fig, ax = plt.subplots(figsize=(10, 6))
    bar1 = ax.bar(seasons, year_0_data, label='Year 0', color='#564E95')
    bar2 = ax.bar(seasons, year_1_data, bottom=year_0_data, label='Year 1', color='#F1D31F')

    ax.set_title('Casual rental averages per season and year (Stacked Bar Plot)')
    ax.set_xlabel('Season')
    ax.set_ylabel('Casual Average')

    ax.legend()

    # Display the Matplotlib figure using Streamlit
    st.pyplot(fig)

    st.write("Data hasil dari pengguna kasual yang dikelompokkan berdasarkan musim dan tahun. Seperti yang disebutkan sebelumnya, kita melihat bahwa musim ketiga pada tahun pertama memiliki nilai total maksimum dan rata-rata tertinggi, diikuti oleh musim kedua juga pada tahun pertama.")

elif chart_type == "Casual Rental per Month":
    st.write("Berikut adalah data untuk Casual rentals per month")

    # Data
    df_casual_month = hour_df.groupby(['month']).agg({'casual': 'sum'}).reset_index()
    df_casual_month.rename(columns={'casual': 'casual_sum'}, inplace=True)
    df_casual_month

    st.write("Visualisasi dalam bentuk bar chart")

    casual_sum = df_casual_month['casual_sum']
    months = df_casual_month['month']

    # Mencari tiga data tertinggi
    top3_indices = casual_sum.nlargest(3).index

    # Membuat daftar warna
    colors = ['#564E95' if i in top3_indices else '#F1D31F' for i in range(len(months))]

    # Create a bar chart
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(months, casual_sum, color=colors)

    # Add labels and title
    ax.set_title('Casual rentals per month')
    ax.set_xlabel('Month')
    ax.set_ylabel('Casual rentals')

    for i in top3_indices:
        ax.text(i+1, casual_sum[i], casual_sum[i], ha='center', va='bottom')

    # Show the plot
    st.pyplot(fig)

    st.write("Berdasarkan grafik di atas, angka penyewaan kasual terbesar terjadi pada musim ke-3 dan ke-2, dengan bulan Juli, Mei, Juni, Agustus, September, dan April memiliki jumlah penyewaan kasual terbanyak dalam urutan tersebut.")

elif chart_type == "Casual Rental by Hour and Season":
    st.write("Berikut adalah data untuk Casual Rental by Hour and Season")

    df_casual_hour_season = hour_df.groupby(['hour', 'season']).agg({'casual': 'sum'}).reset_index()
    df_casual_hour_season.rename(columns={'casual': 'casual_sum'}, inplace=True)
    df_casual_hour_season

    st.write("Visualisasi dalam bentuk bar chart")

    # Data
    df_casual_hour_season = hour_df.groupby(['hour', 'season']).agg({'casual': 'sum'}).reset_index()
    df_casual_hour_season.rename(columns={'casual': 'casual_sum'}, inplace=True)

    # Create a Streamlit app
    st.title('Casual rentals per hour and season')

    # Create a Plotly Express line plot
    fig = px.line(df_casual_hour_season, x='hour', y='casual_sum', color='season', title='Casual rentals per hour and season')

    # Customize line width and colors
    fig.update_traces(line=dict(width=4), mode='lines+markers')
    fig.update_traces(line_color='#FCEE9E', selector=dict(name='1'))
    fig.update_traces(line_color='#F2D499', selector=dict(name='2'))
    fig.update_traces(line_color='#8D9EC7', selector=dict(name='3'))
    fig.update_traces(line_color='#A4CEDB', selector=dict(name='4'))

    # Display the Plotly figure using Streamlit
    st.plotly_chart(fig)

    st.write("Jam 10 pagi hingga 8 malam tampaknya menjadi rentang waktu yang paling umum untuk penyewaan kasual sepanjang musim, dengan peningkatan penggunaan yang sedikit pada pukul 17.00 di musim semi dan musim panas. Kami melihat penurunan yang cukup tajam dalam penggunaan kasual setelah pukul 17.00 di musim dingin, serta beberapa penggunaan tambahan sekitar pukul 19.00 di musim panas.")

elif chart_type == "Casual Rental per Holiday":
    st.write("Berikut adalah data untuk Casual Rental per Holiday")    

    df_holiday_casual = hour_df.groupby(['holiday']).agg({'casual': 'sum'}).reset_index()
    df_holiday_casual.rename(columns={'casual': 'casual_sum'}, inplace=True)
    df_holiday_casual

    st.write("Visualisasi dalam bentuk bar chart")

    fig = px.pie(df_holiday_casual, values='casual_sum', names='holiday', title='Casual rentals per holiday', hole=0.3, color_discrete_sequence=px.colors.sequential.Emrld)
    fig.update_layout(height=600, width=600)

    st.plotly_chart(fig)

    st.write("Dari grafik di atas, dapat diketahui bahwa penyewaan kasual tidak terlalu populer selama liburan, dengan hanya 3,61% dari total penggunaan kasual terjadi pada hari-hari libur ini.")

elif chart_type == "Casual Rental per Work Day":
    st.write("Berikut adalah data untuk Casual Rental per Work Day")    

    df_workday_casual = hour_df.groupby(['work_day']).agg({'casual': 'sum'}).reset_index()
    df_workday_casual.rename(columns={'casual': 'casual_sum'}, inplace=True)
    df_workday_casual

    fig = px.pie(df_workday_casual, values='casual_sum', names='work_day', title='Casual rentals per work day', hole=0.3, color_discrete_sequence=px.colors.sequential.Emrld)
    fig.update_layout(height=600, width=600)
    
    st.plotly_chart(fig)

    st.write("Sebagian besar (51,1%) dari penyewaan kasual tidak terjadi pada hari kerja. Ini berarti 48,9% penyewaan terjadi selama lima hari kerja, jadi mari kita lihat penggunaan kasual berdasarkan hari kerja untuk memastikan sebagian besar penggunaan benar-benar terjadi di akhir pekan")
    
    st.write("Sabtu dan Minggu merupakan hari dengan jumlah penggunaan kasual tertinggi")

else:
    print("")


if(chart_comparation == 'Temperature'):
    import plotly.graph_objects as go
    st.write("Berikut adalah data comparasi dari Casual vs. Registered rentals per temperature value")

    # Data
    df_casual_reg_wind = hour_df.groupby(['temp']).agg({'casual': 'sum', 'registered': 'sum'}).reset_index()
    df_casual_reg_wind.rename(columns={'casual': 'casual_sum', 'registered': 'registered_sum'}, inplace=True)
    df_casual_reg_wind

    # Create a Plotly figure using make_subplots
    fig = go.Figure()

    # Add scatter plots to the figure
    fig.add_trace(go.Scatter(x=df_casual_reg_wind.temp, y=df_casual_reg_wind.casual_sum, name='Casual', line=dict(color='#F2D499', width=4)))
    fig.add_trace(go.Scatter(x=df_casual_reg_wind.temp, y=df_casual_reg_wind.registered_sum, name='Registered', line=dict(color='#8D9EC7', width=4)))

    # Update the layout
    fig.update_layout(
        title='Casual vs. registered rentals per temperature value',
        xaxis_title='Ambient temperature',
        yaxis_title='Sum of rentals',
        height=600,
        width=800,
    )

    # Display the Plotly figure using Streamlit
    st.plotly_chart(fig)
    st.write("Dan inilah gambaran yang lebih jelas, dengan hanya 12% dari total 86 ribu pengguna terdaftar (berwarna biru) merupakan penggunaan kasual pada skala suhu yang lebih rendah, yang mungkin mencerminkan bahwa pengguna terdaftar lebih cenderung menyewa sepeda selama bulan-bulan musim dingin. Penyewaan pada suhu ambient di atas 0,5 mengikuti tren yang hampir identik")

elif chart_comparation == 'Humidity':

    df_casual_reg_humid = hour_df.groupby(['humidity']).agg({'casual': 'sum', 'registered': 'sum'}).reset_index()
    df_casual_reg_humid.rename(columns={'casual': 'casual_sum', 'registered': 'registered_sum'}, inplace=True)
    df_casual_reg_humid

    # Create a Plotly figure using make_subplots
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add scatter plots to the figure
    fig.add_trace(go.Scatter(x=df_casual_reg_humid.humidity, y=df_casual_reg_humid.casual_sum, name='Casual', line=dict(color='#F2D499', width=4)))
    fig.add_trace(go.Scatter(x=df_casual_reg_humid.humidity, y=df_casual_reg_humid.registered_sum, name='Registered', line=dict(color='#8D9EC7', width=4), yaxis='y2'))

    # Update the layout
    fig.update_layout(
        title='Casual vs. registered rentals per humidity',
        xaxis_title='Humidity',
        yaxis_title='Sum of rentals',
        height=600,
        width=800,
    )

    # Display the Plotly figure using Streamlit
    st.plotly_chart(fig)

    st.write("Kelembaban mengikuti pola yang menarik bagi pengguna kasual dan pengguna terdaftar, dengan pengguna kasual cenderung menyewa dalam kondisi kelembaban rendah dan pengguna terdaftar lebih cenderung menyewa dalam skala kelembaban yang lebih tinggi")


# Menampilkan gambar
# st.sidebar.header("Gambar")
# st.image("https://www.example.com/sample_image.jpg", use_column_width=True)

