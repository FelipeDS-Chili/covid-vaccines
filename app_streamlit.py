
from covidvaccines.funciones import get_df, test
import streamlit as st
from bs4 import BeautifulSoup
import pandas as pd
import requests
import os
import json
import time
import altair as alt

#title = st.text_input('Nombre del Anime', 'naruto')

url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv'
data = pd.read_csv(url, error_bad_lines=False).drop(columns = ['iso_code'])

@st.cache
def get_bar_chart_data():
    print('get_bar_chart_data called')

    top_20_vaccines = get_df(data).sort_values('total_vaccinations', ascending = False).head(30)

    return top_20_vaccines[['country', 'vac_per_100000']].sort_values('vac_per_100000', ascending = True)


@st.cache
def get_bar_chart_data_total():
    print('get_bar_chart_data called')

    top_20_vaccines = get_df(data).sort_values('total_vaccinations', ascending = False).head(30)

    return top_20_vaccines[['country', 'total_vaccinations']]


st.header('Covid Vaccination Progress')


st.subheader('Total Vaccinations')



chart_total = get_bar_chart_data_total()

st.subheader('Dataset rows = ', len(chart_total))

brush = alt.selection(type='interval', encodings=['y'])

st.altair_chart(alt.Chart(chart_total, width = 800, height = 800).mark_bar().encode(
    x=alt.X('total_vaccinations'),
    y=alt.Y('country', sort ='-x'
        ),color = "country:N"
).add_selection(
    brush
).interactive().transform_filter(
    brush ).properties(title="Total Vaccinations by Country").resolve_scale(color='shared'))




st.subheader('Vaccinations per inhabitants')

chart_data = get_bar_chart_data()

brush = alt.selection(type='interval', encodings=['y'])

st.altair_chart(alt.Chart(chart_data, width = 800, height = 800).mark_bar().encode(
    x=alt.X('vac_per_100000'),
    y=alt.Y('country', sort ='-x'
        ),color = "country:N"
).add_selection(
    brush
).interactive().transform_filter(
    brush ).properties(title="Vaccinations per 100.000 inhabitants").resolve_scale(color='shared'))


