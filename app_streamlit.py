
from covidvaccines.funciones import get_df, test
import streamlit as st
from bs4 import BeautifulSoup
import pandas as pd
import requests
import os
import json

#title = st.text_input('Nombre del Anime', 'naruto')

url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv'
data = pd.read_csv(url, error_bad_lines=False).drop(columns = ['source_website', 'iso_code'])


st.table(get_df(data).head())



