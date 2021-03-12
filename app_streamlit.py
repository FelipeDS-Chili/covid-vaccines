
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
data['date'] = pd.to_datetime(data.date)







def len_data():
    print(' Calculando largo de data ...')
    return len(data)

@st.cache(suppress_st_warning = True)
def get_bar_chart_data():


    if fecha_desde == 'no':

        top_20_vaccines = get_df(data, 'no').sort_values('totvacc_per_100000', ascending = False).head(30)

        return top_20_vaccines[['country', 'totvacc_per_100000']].sort_values('totvacc_per_100000', ascending = True)
    else:

        top_20_vaccines = get_df(data, fecha_desde).sort_values('delta_totvaccinations_per_100000', ascending = False).head(30)

        return top_20_vaccines[['country', 'delta_totvaccinations_per_100000']]


@st.cache(suppress_st_warning = True)
def get_bar_chart_data_total():
    print('get_bar_chart_data called')

    top_20_vaccines = get_df(data, 'no').sort_values('total_vaccinations', ascending = False).head(30)

    return top_20_vaccines[['country', 'total_vaccinations']]



# @st.cache
# def get_line_chart_data():
#     print('get_line_chart_data called')
#     df = data_2[(data_2.location=='Israel') | (data_2.location=='Chile')]
#     df = df.pivot(index='date',columns='location',values='people_vaccinated',margins = True)
#     #df = data_2.pivot(index='date',columns='location',values='people_vaccinated')
#     return df


# df = get_line_chart_data()


# st.line_chart(df)


# df2 = get_line_chart_data()

# st.line_chart(df2)






st.header('Covid Vaccination Progress')

if st.checkbox('Mostrar tasa de incremento de vacunas respecto a una fecha anterior ?', value=False, key=None):

    fecha_desde_s = st.date_input('Fecha desde: ')

    fecha_desde = pd.to_datetime(fecha_desde_s)



    if st.button('Mostrar gráficos'):


        st.write('Total data in database: ', len_data())

        st.write('Territories in database: ', len(get_df(data, 'no')))

        st.subheader('Total Vaccinations')

        chart_total = get_bar_chart_data_total()

        st.altair_chart(alt.Chart(chart_total, width = 800, height = 800).mark_bar().encode(
            x=alt.X('total_vaccinations'),
            y=alt.Y('country', sort ='-x'
                ),color = "country:N"
        ).interactive().properties(title="Top 30: Total Vaccinations by Country").resolve_scale(color='shared'))

        st.subheader(f'Change rate from {fecha_desde_s} until today')

        chart_data = get_bar_chart_data()

        brush = alt.selection(type='interval', encodings=['y'])

        st.altair_chart(alt.Chart(chart_data, width = 800, height = 800).mark_bar().encode(
            x=alt.X('delta_totvaccinations_per_100000'),
            y=alt.Y('country', sort ='-x'
                ),color = "country:N"
        ).interactive().properties(title="Top 30: Change Rate Total Vaccinations per 100.000 inhabitants").resolve_scale(color='shared'))



else:
    fecha_desde = 'no'

    if st.button('Mostrar gráficos de hoy'):


        st.write('Total data in database: ', len_data())

        st.write('Territories in database: ', len(get_df(data, 'no')))

        st.subheader('Total Vaccinations')

        chart_total = get_bar_chart_data_total()

        st.altair_chart(alt.Chart(chart_total, width = 800, height = 800).mark_bar().encode(
            x=alt.X('total_vaccinations'),
            y=alt.Y('country', sort ='-x'
                ),color = "country:N"
        ).interactive().properties(title="Top 30: Total Vaccinations by Country").resolve_scale(color='shared'))

        st.subheader('Vaccinations per inhabitants')

        chart_data = get_bar_chart_data()

        brush = alt.selection(type='interval', encodings=['y'])

        st.altair_chart(alt.Chart(chart_data, width = 800, height = 800).mark_bar().encode(
            x=alt.X('totvacc_per_100000'),
            y=alt.Y('country', sort ='-x'
                ),color = "country:N"
        ).interactive().properties(title="Top 30: Vaccinations per 100.000 inhabitants").resolve_scale(color='shared'))














