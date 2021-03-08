
from covidvaccines.funciones import get_df, test
import streamlit as st
from bs4 import BeautifulSoup
import pandas as pd
import requests
import os
import json
import time
import altair as alt
import base64

#title = st.text_input('Nombre del Anime', 'naruto')

url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv'
data = pd.read_csv(url, error_bad_lines=False).drop(columns = ['iso_code'])



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



st.header("File Download - A Workaround for small data")

text = """\
    There is currently (20191204) no official way of downloading data from Streamlit. See for
    example [Issue 400](https://github.com/streamlit/streamlit/issues/400)

    But I discovered a workaround
    [here](https://github.com/holoviz/panel/issues/839#issuecomment-561538340).

    It's based on the concept of
    [HTML Data URLs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/Data_URIs)

    You can try it out below for a dataframe csv file download.

    The methodology can be extended to other file types. For inspiration see
    [base64.guru](https://base64.guru/converter/encode/file)
    """
st.markdown(text)

data = [(1, 2, 3)]
# When no file name is given, pandas returns the CSV as a string, nice.
df = pd.DataFrame(data, columns=["Col1", "Col2", "Col3"])
csv = df.to_csv(index=False)
b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
href = f'<a href="data:file/csv;base64,{b64}">Download CSV File</a> (right-click and save as &lt;some_name&gt;.csv)'
st.markdown(href, unsafe_allow_html=True)

