
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
import plotly.express as px
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

@st.cache(persist = True)
def get_chart_per_inhabitants( fecha_desde):


    if fecha_desde == 'no':

        top_20_vaccines = get_df(data, 'no').sort_values( variable_ordenar, ascending = False ).head(30)

        return top_20_vaccines[['country', variable_graficar]].sort_values( variable_graficar, ascending = False )

    else:


        top_20_vaccines = get_df(data, fecha_desde).sort_values('total_vaccinations_today', ascending = False).head(30)


        return top_20_vaccines[['country', 'delta_peoplevaccinated_per_100']].sort_values( 'delta_peoplevaccinated_per_100' , ascending = False)




@st.cache(persist = True)
def get_total_vaccinations():
    print('get_bar_chart_data called')

    top_20_vaccines = get_df(data, 'no').sort_values('total_vaccinations', ascending = False).head(30)

    return top_20_vaccines[['country', 'total_vaccinations']]

@st.cache(persist = True)
def get_lines(data):
    print('Grafico de lineas')

    df = reconstruct_data (data, 'location', 'people_vaccinated', 3 )
    col = df.groupby('location').max()[['date','total_vaccinations', 'people_vaccinated']].reset_index().sort_values('total_vaccinations', ascending = False)
    col_usables = col.head(16).location.to_list()
    col_usables.remove('World')
    col_todos = col.location.to_list()

    for pais in col_usables:
        col_todos.remove(pais)

    data_line = df.set_index('location').drop(index = col_todos).reset_index()
    data_line.date = pd.to_datetime(data_line.date)

    return data_line





st.header('Covid Vaccination Progress')



if st.checkbox('Mostrar tasa de incremento de vacunas respecto a una fecha anterior ?', value=False, key=None):

    fecha_desde_s = st.date_input('Fecha desde: ')

    fecha_desde = pd.to_datetime(fecha_desde_s)



    if st.button('Mostrar gráficos'):



        st.subheader(f'Change rate from {fecha_desde_s} until today')


        chart_data = get_chart_per_inhabitants( fecha_desde)

        # brush = alt.selection(type='interval', encodings=['y'])

        # st.altair_chart(alt.Chart(chart_data, width = 800, height = 800).mark_bar().encode(
        #     x=alt.X('delta_peoplevaccinated_per_100'),
        #     y=alt.Y('country', sort ='-x'
        #         ),color = "country:N"
        # ).interactive().properties(title="Top 30: Change Rate People Vaccinated per 100 inhabitants").resolve_scale(color='shared'))


        fig = px.bar( chart_data, x = "delta_peoplevaccinated_per_100", y = "country",\
                     orientation = 'h', title = 'Top 30: People Vaccinated per 100.000 inhabitants', hover_name = 'country',\
                     template = 'plotly_white', color = 'country',width=900, height=1000)


        st.plotly_chart(fig)





        fig = px.line(get_lines(data), x="date", y="people_vaccinated", color="location", hover_name="location", render_mode="svg")
        st.plotly_chart(fig)








else:

    fecha_desde = 'no'


    if st.button('Mostrar gráficos de hoy'):


        # st.write('Total data in database: ', len(data) )

        # st.write('Territories in database: ', len(get_df(data, 'no')) )

        # st.subheader('Total Vaccinations')

        # chart_total = get_total_vaccinations()

        # st.altair_chart(alt.Chart(chart_total, width = 800, height = 800).mark_bar().encode(
        #     x=alt.X('total_vaccinations'),
        #     y=alt.Y('country', sort ='-x'
        #         ),color = "country:N"
        # ).interactive().properties(title="Top 30: Total Vaccinations by Country").resolve_scale(color='shared'))

        # st.subheader('Vaccinations per inhabitants')

        # chart_data = get_chart_per_inhabitants(fecha_desde)



        # brush = alt.selection(type='interval', encodings=['y'])

        # st.altair_chart(alt.Chart(chart_data, width = 800, height = 800).mark_bar().encode(
        #     x=alt.X(variable_graficar),
        #     y=alt.Y('country', sort ='-x'
        #         ),color = "country:N"
        # ).interactive().properties(title="Top 30: People Vaccinated per 100.000 inhabitants").resolve_scale(color='shared'))


        df = get_total_vaccinations()


        fig = px.bar( df, x = "total_vaccinations", y = "country",\
                     orientation = 'h', title = 'Top 30: Total Vaccinations by Country', hover_name = 'country',\
                     template = 'plotly_white', color = 'country',width=900, height=1000)

        st.plotly_chart(fig)

        chart_data = get_chart_per_inhabitants(fecha_desde)

        fig = px.bar( chart_data, x = "peoplevaccinated_per_100", y = "country",\
                     orientation = 'h', title = 'Top 30: People Vaccinated per 100.000 inhabitants', hover_name = 'country',\
                     template = 'plotly_white', color = 'country',width=900, height=1000)


        st.plotly_chart(fig)






