import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from matplotlib.dates import MonthLocator, DateFormatter

sns.set(style='dark')

# Helper function yang dibutuhkan untuk menyiapkan berbagai dataframe


def create_season_effect_df(df):
    season_effect_df = df.groupby(
        by="season").total_rentals.mean().reset_index()
    return season_effect_df


def create_weather_effect_df(df):
    weather_effect_df = df.groupby(
        by="weathersit").total_rentals.mean().reset_index()
    return weather_effect_df


def create_working_day_effect_df(df):
    working_day_effect_df = df.groupby(
        by="is_working_day").total_rentals.mean().reset_index()
    working_day_effect_df.rename(
        index={0: 'Not Working Day', 1: 'Working Day'}, inplace=True)
    return working_day_effect_df


def create_monthly_rentals_df(df):
    monthly_rentals_df = df.resample('MS', on='date')['total_rentals'].sum()
    return monthly_rentals_df


# Load cleaned data
main_df = pd.read_csv("main_data.csv")

datetime_columns = ["date"]
for column in datetime_columns:
    main_df[column] = pd.to_datetime(main_df[column])


# # Menyiapkan berbagai dataframe
df_2011 = main_df[main_df['date'].dt.year == 2011]
df_2012 = main_df[main_df['date'].dt.year == 2012]

season_effect_df = create_season_effect_df(main_df)
weather_effect_df = create_weather_effect_df(main_df)
working_day_effect_df = create_working_day_effect_df(main_df)
monthly_rentals_2011_df = create_monthly_rentals_df(df_2011)
monthly_rentals_2012_df = create_monthly_rentals_df(df_2012)


# Create Dashboard
st.header('Bike Sharing Dashboard :bike:')

# # Season and Wather Effect
st.subheader("Season and Weather Effect")

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(30, 15))
    colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

    sns.barplot(
        y="total_rentals",
        x="season",
        data=season_effect_df,
        palette=colors,
        ax=ax
    )
    ax.set_title("Average Bike Rentals by Season", loc="center", fontsize=50)
    ax.set_ylabel('Average Bike Rentals', fontsize=30)
    ax.set_xlabel('Season', fontsize=30)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(30, 15))

    colors = ["#90CAF9", "#D3D3D3", "#D3D3D3"]

    sns.barplot(
        y="total_rentals",
        x="weathersit",
        data=weather_effect_df,
        palette=colors,
        ax=ax
    )
    ax.set_title("Average Bike Rentals by Weather", loc="center", fontsize=50)
    ax.set_ylabel('Average Bike Rentals', fontsize=30)
    ax.set_xlabel('Weather Condition', fontsize=30)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)


# # Workingday vs Non-Workingday
st.subheader("Workingday vs Non-Workingday")

fig, ax = plt.subplots(figsize=(30, 15))

colors = ["#FF6347", "#1E90FF"]

sns.barplot(
    y="total_rentals",
    x="is_working_day",
    data=working_day_effect_df,
    palette=colors,
    ax=ax
)
ax.set_title("Average Bike Rentals on Working Day vs Non-working Day",
             loc="center", fontsize=50)
ax.set_ylabel('Average Bike Rentals', fontsize=30)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=35)
ax.tick_params(axis='y', labelsize=30)
ax.set_xticklabels(['Not Working Day', 'Working Day'])
st.pyplot(fig)


# # Bike Rentals Trends in 2011 and 2012
st.subheader("Bike Rentals Trends in 2011 and 2012")

# # # 2011
fig, ax = plt.subplots(figsize=(12, 6))

sns.lineplot(data=monthly_rentals_2011_df, marker='o', color='b', ax=ax)
ax.set_title('Tren Jumlah Peminjaman Sepeda (2011)')
ax.set_xlabel('Bulan')
ax.set_ylabel('Jumlah Peminjaman')
ax.grid(True)
plt.gca().xaxis.set_major_locator(MonthLocator())
plt.gca().xaxis.set_major_formatter(DateFormatter('%b'))
st.pyplot(fig)

# # # 2012
fig, ax = plt.subplots(figsize=(12, 6))

sns.lineplot(data=monthly_rentals_2012_df, marker='o', color='b', ax=ax)
ax.set_title('Tren Jumlah Peminjaman Sepeda (2011)')
ax.set_xlabel('Bulan')
ax.set_ylabel('Jumlah Peminjaman')
ax.grid(True)
plt.gca().xaxis.set_major_locator(MonthLocator())
plt.gca().xaxis.set_major_formatter(DateFormatter('%b'))
st.pyplot(fig)
