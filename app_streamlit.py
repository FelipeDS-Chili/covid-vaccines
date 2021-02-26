
from covidvaccines.funciones import get_df, test
import streamlit as st
from bs4 import BeautifulSoup
import pandas as pd
import requests
import os
import json

#title = st.text_input('Nombre del Anime', 'naruto')

st.table(get_df().head())



