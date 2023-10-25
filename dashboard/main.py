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
st.write("Exploratory Data Analysis (EDA) merupakan tahap eksplorasi data yang telah dibersihkan guna memperoleh insight dan menjawab pertanyaan analisis.")

# Sidebar
st.sidebar.header("Pengaturan")

# Pilihan untuk mengunggah file CSV
# uploaded_file = st.sidebar.file_uploader("Unggah File CSV", type=["csv"])

# Dataframe untuk menampilkan data
df = pd.read_csv('./dashboard/dataset_normalization.csv')

# Tampilkan dataset
# st.sidebar.header("Dataset")
# if st.sidebar.checkbox("Tampilkan Dataframe"):
#     st.subheader("Dataframe")
#     st.write(df)

# # Pilihan statistik
# st.sidebar.header("Statistik")
# if st.sidebar.checkbox("Tampilkan Statistik"):
#     st.subheader("Statistik Deskriptif")
#     st.write(df.describe())


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
# correlation
st.subheader("Visualisasi Data")

# "Casual Rental per Season":
st.write("Berikut adalah visualisasi data untuk Casual Rental per Season")

# Data
season_registered = hour_df.groupby(['season'])['registered'].sum()
season_casual = hour_df.groupby(['season'])['casual'].sum()
season_registered = season_registered / season_registered.sum()
season_casual = season_casual / season_casual.sum()

season_registered = season_registered.reset_index()
season_casual = season_casual.reset_index()

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

# "Casual Rental by Season and Year":
st.write("Berikut adalah data untuk Casual Rental by Season and Year")

df_casual_avg = hour_df.groupby(['season', 'year']).agg({'casual': 'mean'}).reset_index()
df_casual_avg.rename(columns={'casual': 'casual_avg'}, inplace=True)

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


# "Casual Rental per Month":
st.write("Berikut adalah visualisasi data untuk Casual rentals per month")

# Data
df_casual_month = hour_df.groupby(['month']).agg({'casual': 'sum'}).reset_index()
df_casual_month.rename(columns={'casual': 'casual_sum'}, inplace=True)

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


# "Casual Rental by Hour and Season":
st.write("Berikut adalah Visualisasi data untuk Casual Rental by Hour and Season")

df_casual_hour_season = hour_df.groupby(['hour', 'season']).agg({'casual': 'sum'}).reset_index()
df_casual_hour_season.rename(columns={'casual': 'casual_sum'}, inplace=True)

# Data
df_casual_hour_season = hour_df.groupby(['hour', 'season']).agg({'casual': 'sum'}).reset_index()
df_casual_hour_season.rename(columns={'casual': 'casual_sum'}, inplace=True)


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


# "Casual Rental per Holiday":
st.write("Berikut adalah visualisasi data untuk Casual Rental per Holiday")    

df_holiday_casual = hour_df.groupby(['holiday']).agg({'casual': 'sum'}).reset_index()
df_holiday_casual.rename(columns={'casual': 'casual_sum'}, inplace=True)

fig = px.pie(df_holiday_casual, values='casual_sum', names='holiday', title='Casual rentals per holiday', hole=0.3, color_discrete_sequence=px.colors.sequential.Emrld)
fig.update_layout(height=600, width=600)

st.plotly_chart(fig)


# "Casual Rental per Work Day":
st.write("Berikut adalah visualisasi data untuk Casual Rental per Work Day")    

df_workday_casual = hour_df.groupby(['work_day']).agg({'casual': 'sum'}).reset_index()
df_workday_casual.rename(columns={'casual': 'casual_sum'}, inplace=True)

fig = px.pie(df_workday_casual, values='casual_sum', names='work_day', title='Casual rentals per work day', hole=0.3, color_discrete_sequence=px.colors.sequential.Emrld)
fig.update_layout(height=600, width=600)

st.plotly_chart(fig)




# Komparasi

# 'Temperature'):
st.subheader("Komparasi Data Pengguna Casual vs Register")
st.write("Berikut adalah visualisasi data komparasi dari Casual vs. Registered rentals per temperature value")

# Data
df_casual_reg_wind = hour_df.groupby(['temp']).agg({'casual': 'sum', 'registered': 'sum'}).reset_index()
df_casual_reg_wind.rename(columns={'casual': 'casual_sum', 'registered': 'registered_sum'}, inplace=True)

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


# 'Humidity':
st.write('Berikut adalah visualisasi data untuk komparasi berdasarkan Humidity:')
df_casual_reg_humid = hour_df.groupby(['humidity']).agg({'casual': 'sum', 'registered': 'sum'}).reset_index()
df_casual_reg_humid.rename(columns={'casual': 'casual_sum', 'registered': 'registered_sum'}, inplace=True)

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


# Menampilkan gambar
# st.sidebar.header("Gambar")
# st.image("https://www.example.com/sample_image.jpg", use_column_width=True)

