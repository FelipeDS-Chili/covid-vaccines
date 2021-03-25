
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



# Solo para el caso de ""no""
variable_ordenar = 'people_vaccinated' # people_vaccinated | total_vaccinations
variable_graficar = 'peoplevaccinated_per_100'  # totvacc_per_100000 |  peoplevaccinated_per_100000
variable_graficar_desde = 'delta_peoplevaccinated_per_100' # delta_totvaccinations_per_100000 | delta_peoplevaccinated_per_100000

def len_data():
    print(' Calculando largo de data ...')
    return len(data)

@st.cache(suppress_st_warning = True)
def get_chart_per_inhabitants(df, fecha_desde):


    if fecha_desde == 'no':

        top_20_vaccines = df.sort_values( variable_ordenar, ascending = False ).head(30)

        return top_20_vaccines[['country', variable_graficar]].sort_values( variable_graficar, ascending = False )

    else:


        top_20_vaccines = df.sort_values('total_vaccinations_today', ascending = False).head(30)


        return top_20_vaccines[['country', 'delta_peoplevaccinated_per_100']].sort_values( 'delta_peoplevaccinated_per_100' , ascending = False)




@st.cache(suppress_st_warning = True)
def get_total_vaccinations(df):
    print('get_bar_chart_data called')

    top_20_vaccines = df.sort_values('total_vaccinations', ascending = False).head(30)

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

data_deploy = get_df(data, 'no')
chart_total = get_total_vaccinations( data_deploy )




st.header('Covid Vaccination Progress')

if st.checkbox('Mostrar tasa de incremento de vacunas respecto a una fecha anterior ?', value=False, key=None):

    fecha_desde_s = st.date_input('Fecha desde: ')

    fecha_desde = pd.to_datetime(fecha_desde_s)




    if st.button('Mostrar gráficos'):


        data_with_date = get_df(data, fecha_desde)

        st.write('Total data in database: ', len(data) )

        st.write('Territories in database: ', len( data_deploy ) )

        st.subheader('Total Vaccinations')



        st.altair_chart(alt.Chart(chart_total, width = 800, height = 800).mark_bar().encode(
            x=alt.X('total_vaccinations'),
            y=alt.Y('country', sort ='-x'
                ),color = "country:N"
        ).interactive().properties(title="Top 30: Total Vaccinations by Country").resolve_scale(color='shared'))




        st.subheader(f'Change rate from {fecha_desde_s} until today')


        chart_data = get_chart_per_inhabitants(data_with_date, fecha_desde)

        brush = alt.selection(type='interval', encodings=['y'])

        st.altair_chart(alt.Chart(chart_data, width = 800, height = 800).mark_bar().encode(
            x=alt.X('delta_peoplevaccinated_per_100'),
            y=alt.Y('country', sort ='-x'
                ),color = "country:N"
        ).interactive().properties(title="Top 30: Change Rate People Vaccinated per 100 inhabitants").resolve_scale(color='shared'))




else:

    fecha_desde = 'no'


    if st.button('Mostrar gráficos de hoy'):


        st.write('Total data in database: ', len(data) )

        st.write('Territories in database: ', len(data_deploy) )

        st.subheader('Total Vaccinations')


        st.altair_chart(alt.Chart(chart_total, width = 800, height = 800).mark_bar().encode(
            x=alt.X('total_vaccinations'),
            y=alt.Y('country', sort ='-x'
                ),color = "country:N"
        ).interactive().properties(title="Top 30: Total Vaccinations by Country").resolve_scale(color='shared'))

        st.subheader('Vaccinations per inhabitants')

        chart_data = get_chart_per_inhabitants( data_deploy , fecha_desde)

        brush = alt.selection(type='interval', encodings=['y'])

        st.altair_chart(alt.Chart(chart_data, width = 800, height = 800).mark_bar().encode(
            x=alt.X(variable_graficar),
            y=alt.Y('country', sort ='-x'
                ),color = "country:N"
        ).interactive().properties(title="Top 30: People Vaccinated per 100.000 inhabitants").resolve_scale(color='shared'))














