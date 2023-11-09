import streamlit as st
from dbhelper import DB

import pandas as pd
import plotly.graph_objects as go

db = DB()

st.sidebar.title('Flights Analytics')

user_option = st.sidebar.selectbox('Menu',['Select One','Check Flights','Analytics'])

if user_option == 'Check Flights':
    st.title('Check Flights')
    city = db.fetch_city_names()

    col1, col2 = st.columns(2)

    with col1:
        source = st.selectbox('Source',sorted(city))

    with col2:
        destination = st.selectbox('Destination',sorted(city))

    if st.button('search'):
        data = db.fetch_all_flights(source,destination)
        st.dataframe(data)

elif user_option == 'Analytics':
    st.title('Analytics')
    airline,frequency = db.fetch_airline_frequency()
    fig = go.Figure(
        go.Pie(
            labels=airline,
            values=frequency,
            hoverinfo="label+percent",
            textinfo="value"
        ))
    st.header("Pie chart")
    st.plotly_chart(fig)

    city, frequency1 = db.busy_airport()
    chart_data = pd.DataFrame(frequency1, city)
    st.header("Bar chart")
    st.bar_chart(chart_data)
    #st.header("Bar chart")
    #st.plotly_chart(fig)

    date,frequency3 = db.daily_frequency()
    chart_data = pd.DataFrame(frequency3, date)
    st.header("line chart")
    st.line_chart(chart_data)
else:
    st.title('Tell about the project')