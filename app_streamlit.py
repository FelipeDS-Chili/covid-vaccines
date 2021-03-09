
from covidvaccines.funciones import get_df, reconstruct_data
import streamlit as st
from bs4 import BeautifulSoup
import pandas as pd
import requests
import os
import json
import time
import altair as alt
import base64
import numpy as np



url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv'
data = pd.read_csv(url, error_bad_lines=False).drop(columns = ['iso_code'])
data_2 = reconstruct_data(data, columna_filtro = 'location', columna_a_reconstruir = 'total_vaccinations', n = 2)

#data['date'] = pd.to_datetime(data.date)




def len_data():
    print(' Calculando largo de data ...')
    return len(data)

@st.cache(suppress_st_warning = True)
def get_bar_chart_data():
    print('get_bar_chart_data called')

    top_20_vaccines = get_df(data).sort_values('total_vaccinations', ascending = False).head(30)

    return top_20_vaccines[['country', 'vac_per_100000']].sort_values('vac_per_100000', ascending = True)




@st.cache(suppress_st_warning = True)
def get_bar_chart_data_total():
    print('get_bar_chart_data called')

    top_20_vaccines = get_df(data).sort_values('total_vaccinations', ascending = False).head(30)

    return top_20_vaccines[['country', 'total_vaccinations']]

@st.cache
def get_line_chart_data():
    print('get_line_chart_data called')
    df = data_2.pivot(index='date',columns='location',values='people_vaccinated')
    return df.head(5)


df = get_line_chart_data()


st.line_chart(df)


# df2 = get_line_chart_data()

# st.line_chart(df2)





st.header('Covid Vaccination Progress')


st.subheader('Total Vaccinations')



chart_total = get_bar_chart_data_total()

st.write('Total data in database: ', len_data())

st.write('Territories in database: ', len(get_df(data)))




st.altair_chart(alt.Chart(chart_total, width = 800, height = 800).mark_bar().encode(
    x=alt.X('total_vaccinations'),
    y=alt.Y('country', sort ='-x'
        ),color = "country:N"
).interactive().properties(title="Top 30: Total Vaccinations by Country").resolve_scale(color='shared'))




st.subheader('Vaccinations per inhabitants')

chart_data = get_bar_chart_data()

brush = alt.selection(type='interval', encodings=['y'])

st.altair_chart(alt.Chart(chart_data, width = 800, height = 800).mark_bar().encode(
    x=alt.X('vac_per_100000'),
    y=alt.Y('country', sort ='-x'
        ),color = "country:N"
).interactive().properties(title="Top 30: Vaccinations per 100.000 inhabitants").resolve_scale(color='shared'))



