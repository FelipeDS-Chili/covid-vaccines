from flask import Flask, escape, request, render_template,jsonify
from bs4 import BeautifulSoup
import pandas as pandas
import requests
import json
from covidvaccines.funciones import get_df

app = Flask(__name__)

@app.route('/')
def home():
   return 'holllllllllllllllsdsad'

@app.route('/buscar_episodios', methods = ['GET'])
def get_api():

    pass


if __name__ == '__main__':
    app.run(host = '127.0.0.1', port =5000, debug=True)

