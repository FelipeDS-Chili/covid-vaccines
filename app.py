from flask import Flask, escape, request, render_template,jsonify
from bs4 import BeautifulSoup
import pandas as pandas
import requests
import json


app = Flask(__name__)

@app.route('/')
def home():
   return render_template('home.html')

@app.route('/buscar_episodios', methods = ['GET'])
def get_api():

    name = request.args.get('name')

    response = requests.get(f'https://cdn.animenewsnetwork.com/encyclopedia/api.xml?title=~{name}')

    soup = BeautifulSoup(response.text,'html.parser')


    anime = soup.find_all('anime', type ='TV')

    season = 0

    epis = { 'Mensaje : ': 'Aqui esta el listado de los episodios' }

    for i in range(len(anime)):

       if anime[i].find_all('episode'):

            episodes = anime[i].find_all('episode')

            season += 1


            for index, episode in enumerate(episodes):

                n_partes_episodios = len( episode.find_all('title', lang = 'EN') )

                for parte_n in range ( n_partes_episodios ):

                    nombre_parte = episode.find_all('title')[parte_n].string

                    if n_partes_episodios > 1:
                        jkey = f'S{season}E{index + 1}P{parte_n + 1}'

                        detalle = f'Season {season} ,' + 'Episodio ' + f' {index + 1}: '+ f'Parte: {parte_n + 1}'
                        impresion = detalle + ' {} '
                        epis[jkey] = nombre_parte

                       # print (impresion.format(nombre_parte))
                    else:

                        jkey = f'S{season}E{index + 1}'

                        detalle = f'Season {season} ,' + 'Episodio ' + f' {index + 1}: '
                        impresion = detalle +' {} '
                        epis[jkey] = nombre_parte

                      #  print (impresion.format(nombre_parte))


    return jsonify(epis)
    #return json.dumps(epis, indent = 4)
    #return epis

#anime[1].find_all('episode')[0].find_all('title')

if __name__ == '__main__':
    app.run(host = '127.0.0.1', port =5000, debug=True)

    #print(get_api('naruto'))
