import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
import re
import os




def fill_people_full_vacc(x,column,data):

    if np.isnan(data['people_vaccinated'][x]) or np.isnan(data['total_vaccinations'][x]):
        if pd.notna(data[column][x]):
            return data[column][x]
        return np.nan
    else:
        if data['total_vaccinations'][x] == data['people_vaccinated'][x]:
            return 0
        else:
            return data[column][x]



def get_population(country):

    if country:

        country = country.replace(' ','-')
        country = country.lower()

        url = f'https://www.worldometers.info/world-population/{country}-population/'

        response = requests.get(url)

        if response.status_code == 200:

            html = response.text

            soup = BeautifulSoup(html, 'html.parser')

            if re.search(r"\d{5,}", soup.find(class_ = "col-md-8 country-pop-description").find_all('li')[0].text.replace(',','')):

                population = int(re.search(r"\d{5,}", soup.find(class_ = "col-md-8 country-pop-description").find_all('li')[0].text.replace(',','')).group(0))

                return population

            return None

        return None

    return None


def get_df(data):


    #data = pd.read_csv(os.path.join(os.path.dirname(__file__) , 'data', 'country_vaccinations.csv')).drop(columns = ['source_website', 'iso_code'])

    data = data.rename(columns={"location": "country"})
    data.people_fully_vaccinated = data.index.map(lambda x: fill_people_full_vacc(x,'people_fully_vaccinated',data))
    data.people_fully_vaccinated_per_hundred = data.index.map(lambda x: fill_people_full_vacc(x,'people_fully_vaccinated_per_hundred',data))

    data_by_country = data.groupby('country').max()[['date','total_vaccinations', 'people_vaccinated']].reset_index()

    data_full = data_by_country
    data_full.country = data_full.country.replace('United Kingdom', 'UK').replace('United States', 'US')
    data_full = data_full.set_index('country')

    data_full['pop_data_2019'] = data_full.index.map(lambda x: get_population(x))

    #relleno de data no encontrada
    data_full.at['England', 'pop_data_2019'] = 55980000
    data_full.at['Falkland Islands', 'pop_data_2019'] = 2840
    data_full.at['Guernsey', 'pop_data_2019'] = 63155
    data_full.at['Jersey', 'pop_data_2019'] = 97857
    data_full.at['Macao', 'pop_data_2019'] = 631636
    data_full.at['Northern Cyprus', 'pop_data_2019'] = 326000
    data_full.at['Northern Ireland', 'pop_data_2019'] = 1882000
    data_full.at['Saint Helena', 'pop_data_2019'] = 6600
    data_full.at['Scotland', 'pop_data_2019'] = 5454000
    data_full.at['Wales', 'pop_data_2019'] = 3136000
    data_full.at['World', 'pop_data_2019'] = 7700000000
    data_full.at['European Union', 'pop_data_2019'] = 446000000



    data_full = data_full.reset_index()

    data_full['vac_per_100000'] = data_full.total_vaccinations/data_full.pop_data_2019*100000

    return data_full

def test():
    return __file__



def grafico_vacunas_totales(data):
    fig, ax = plt.subplots(figsize=(10, 20), tight_layout=True)

    ax.barh(y = 'country', width= 'people_vaccinated', data = data[data.people_vaccinated>1000000].sort_values('people_vaccinated'), label = 'total vacunados')

    ax.tick_params(axis='x', rotation=0)
    ax.get_xaxis().get_major_formatter().set_scientific(False)
    plt.legend()

    return plt.show()


def grafico_vacunas_per_100000():

    top_20_vaccines = data_full.sort_values('total_vaccinations', ascending = False).head(20)
    fig, ax = plt.subplots(figsize=(12, 20), tight_layout=True)



    ax.barh(y = 'country', width= 'vac_per_100000', data = top_20_vaccines.sort_values('vac_per_100000', ascending = True), label = 'vacunados per 100.000')


    ax.tick_params(axis='x', rotation=0)
    ax.get_xaxis().get_major_formatter().set_scientific(False)
    plt.legend()

    for i, v in enumerate(top_20_vaccines.sort_values('vac_per_100000', ascending = True).vac_per_100000):
        ax.text(v + 3, i - 0.05, str(int(v)), color='blue', fontsize = 10)



        return None




if __name__ == '__main__':
    pass
