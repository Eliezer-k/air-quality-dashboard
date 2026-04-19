import streamlit as st
import pandas as pd
import plotly.express as px


@st.cache_data
def load_data():
    station_day = pd.read_csv("station_day.csv")
    station_hour = pd.read_csv("station_hour.csv")
    stations = pd.read_csv("stations.csv")
    city_day = pd.read_csv("city_day.csv")
    city_hour = pd.read_csv("city_hour.csv")

   
    station_day['Date'] = pd.to_datetime(station_day['Date'], errors='coerce')
    station_hour['Datetime'] = pd.to_datetime(station_hour['Datetime'], errors='coerce')
    city_day['Date'] = pd.to_datetime(city_day['Date'], errors='coerce')
    city_hour['Datetime'] = pd.to_datetime(city_hour['Datetime'], errors='coerce')

    return station_day, station_hour, stations, city_day, city_hour

station_day, station_hour, stations, city_day, city_hour = load_data()

st.title("Air Quality Monitoring Dashboard")

mode = st.sidebar.selectbox("Select visualization mode:", 
                            ["Station - Day", "Station - Hour", "City - Day", "City - Hour"])

if mode == "Station - Day":
    station_list = sorted(stations["StationId"].dropna().unique())
    station_sel = st.sidebar.selectbox("Select a station:", station_list)

    df = station_day[station_day["StationId"] == station_sel]
    if df.empty:
        st.warning("No data available for this station.")
    else:
        dates = df['Date'].dropna().dt.date.unique()
        date_sel = st.sidebar.selectbox("Select a date:", sorted(dates))

        df_date = df[df['Date'].dt.date == date_sel]
        if df_date.empty:
            st.warning("No data available for this date.")
        else:
            st.subheader(f"Data for station {station_sel} on {date_sel}")
            st.dataframe(df_date)

            # Prepare pollutant data for plot
            pollutants = ['PM2.5', 'PM10', 'NO', 'NO2', 'NOx', 'NH3', 'CO', 'SO2', 'O3', 'Benzene', 'Toluene', 'Xylene']
            df_melt = df_date.melt(id_vars=['StationId', 'Date'], value_vars=pollutants,
                                   var_name='Pollutant', value_name='Value').dropna()

            fig = px.bar(df_melt, x='Pollutant', y='Value', color='Pollutant',
                         title=f"Pollutant levels for {station_sel} on {date_sel}")
            st.plotly_chart(fig)

elif mode == "Station - Hour":
    station_list = sorted(stations["StationId"].dropna().unique())
    station_sel = st.sidebar.selectbox("Select a station:", station_list)

    df = station_hour[station_hour["StationId"] == station_sel]
    if df.empty:
        st.warning("No data available for this station.")
    else:
        dates = df['Datetime'].dt.date.dropna().unique()
        date_sel = st.sidebar.selectbox("Select a date:", sorted(dates))

        df_date = df[df['Datetime'].dt.date == date_sel]
        if df_date.empty:
            st.warning("No data available for this date.")
        else:
            st.subheader(f"Hourly data for station {station_sel} on {date_sel}")
            st.dataframe(df_date)

            pollutants = ['PM2.5', 'PM10', 'NO', 'NO2', 'NOx', 'NH3', 'CO', 'SO2', 'O3', 'Benzene', 'Toluene', 'Xylene']
            df_melt = df_date.melt(id_vars=['StationId', 'Datetime'], value_vars=pollutants,
                                   var_name='Pollutant', value_name='Value').dropna()

            fig = px.line(df_melt, x='Datetime', y='Value', color='Pollutant',
                          title=f"Hourly pollutant levels for {station_sel} on {date_sel}")
            st.plotly_chart(fig)

elif mode == "City - Day":
    city_list = sorted(city_day["City"].dropna().unique())
    city_sel = st.sidebar.selectbox("Select a city:", city_list)

    df = city_day[city_day["City"] == city_sel]
    if df.empty:
        st.warning("No data available for this city.")
    else:
        dates = df['Date'].dt.date.dropna().unique()
        date_sel = st.sidebar.selectbox("Select a date:", sorted(dates))

        df_date = df[df['Date'].dt.date == date_sel]
        if df_date.empty:
            st.warning("No data available for this date.")
        else:
            st.subheader(f"Data for city {city_sel} on {date_sel}")
            st.dataframe(df_date)

            pollutants = ['PM2.5', 'PM10', 'NO', 'NO2', 'NOx', 'NH3', 'CO', 'SO2', 'O3', 'Benzene', 'Toluene', 'Xylene']
            df_melt = df_date.melt(id_vars=['City', 'Date'], value_vars=pollutants,
                                   var_name='Pollutant', value_name='Value').dropna()

            fig = px.bar(df_melt, x='Pollutant', y='Value', color='Pollutant',
                         title=f"Pollutant levels for {city_sel} on {date_sel}")
            st.plotly_chart(fig)

elif mode == "City - Hour":
    city_list = sorted(city_hour["City"].dropna().unique())
    city_sel = st.sidebar.selectbox("Select a city:", city_list)

    df = city_hour[city_hour["City"] == city_sel]
    if df.empty:
        st.warning("No data available for this city.")
    else:
        dates = df['Datetime'].dt.date.dropna().unique()
        date_sel = st.sidebar.selectbox("Select a date:", sorted(dates))

        df_date = df[df['Datetime'].dt.date == date_sel]
        if df_date.empty:
            st.warning("No data available for this date.")
        else:
            st.subheader(f"Hourly data for city {city_sel} on {date_sel}")
            st.dataframe(df_date)

            pollutants = ['PM2.5', 'PM10', 'NO', 'NO2', 'NOx', 'NH3', 'CO', 'SO2', 'O3', 'Benzene', 'Toluene', 'Xylene']
            df_melt = df_date.melt(id_vars=['City', 'Datetime'], value_vars=pollutants,
                                   var_name='Pollutant', value_name='Value').dropna()

            fig = px.line(df_melt, x='Datetime', y='Value', color='Pollutant',
                          title=f"Hourly pollutant levels for {city_sel} on {date_sel}")
            st.plotly_chart(fig)
