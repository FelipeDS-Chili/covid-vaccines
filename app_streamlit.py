
from toolbox.operations import get_data, get_episodes
import streamlit as st
from bs4 import BeautifulSoup
import pandas as pandas
import requests
import json

#title = st.text_input('Nombre del Anime', 'naruto')

st.table(get_data().head())



