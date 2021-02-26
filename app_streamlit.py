
from covidvaccines.funciones import get_df()
import streamlit as st
from bs4 import BeautifulSoup
import pandas as pandas
import requests
import json

#title = st.text_input('Nombre del Anime', 'naruto')

st.table(get_df.head())



