
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

    top_20_vaccines = get_df(data).sort_values('total_vaccinations', ascending = False).head(20)

    return top_20_vaccines[['country', 'vac_per_100000']].sort_values('vac_per_100000', ascending = True)
#.set_index('country') antes de sort




'Starting a long computation...'



chart_data = get_bar_chart_data()

st.write('COVID19')
st.bar_chart(chart_data, width = 0, height = 0)

brush = alt.selection(type='interval', encodings=['y'])

st.altair_chart(alt.Chart(chart_data, width = 800, height = 800).mark_bar().encode(
    x=alt.X('vac_per_100000'),
    y=alt.Y('country', sort ='-x'),
).add_selection(
    brush
).interactive().transform_filter(
    brush ).properties(title="Vaccinations per 100000 inhabitants"))


