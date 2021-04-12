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


def get_df(data, fecha_desde):


    #data = pd.read_csv(os.path.join(os.path.dirname(__file__) , 'data', 'country_vaccinations.csv')).drop(columns = ['source_website', 'iso_code'])
    #cambio
    data = reconstruct_data(data, columna_filtro = 'location', columna_a_reconstruir = 'total_vaccinations' , n = 2)
    data = reconstruct_data(data, columna_filtro = 'location', columna_a_reconstruir = 'people_vaccinated' , n = 3)
    data.date = pd.to_datetime(data.date)
    data = data.rename(columns={"location": "country"})
    data.people_fully_vaccinated = data.index.map(lambda x: fill_people_full_vacc(x,'people_fully_vaccinated',data))
    data.people_fully_vaccinated_per_hundred = data.index.map(lambda x: fill_people_full_vacc(x,'people_fully_vaccinated_per_hundred',data))





    #cambio  name
    data_by_country_today = data.groupby('country').max()[['date','total_vaccinations', 'people_vaccinated']].reset_index()

    data_full = data_by_country_today
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


    if fecha_desde == 'no':
        data_full['totvacc_per_100'] = data_full.total_vaccinations/data_full.pop_data_2019*100
        data_full['peoplevaccinated_per_100'] = data_full.people_vaccinated/data_full.pop_data_2019*100

        return data_full.drop(columns = 'date').reset_index()

    else:
        data_since = data[data.date <= fecha_desde]
        data_by_country_since = data_since.groupby('country').max()[['date','total_vaccinations', 'people_vaccinated']].reset_index()
        data_by_country_since = data_by_country_since.drop(columns = 'date').rename(columns={"total_vaccinations": "total_vaccinations_before", 'people_vaccinated': 'people_vaccinated_before' })
        data_by_country_since.country = data_by_country_since.country.replace('United Kingdom', 'UK').replace('United States', 'US')


        data_full = data_full.reset_index()

        data_full = data_full.rename(columns={"total_vaccinations": "total_vaccinations_today", 'people_vaccinated': 'people_vaccinated_today' })

        data_full = data_full.merge(data_by_country_since, how = 'left', on = 'country' )

        data_full['totvacc_per_100_today'] = data_full.total_vaccinations_today/data_full.pop_data_2019*100

        data_full['totvacc_per_100_before'] = data_full.total_vaccinations_before/data_full.pop_data_2019*100

        data_full['peoplevacc_per_100_today'] = data_full.people_vaccinated_today/data_full.pop_data_2019*100

        data_full['peoplevacc_per_100_before'] = data_full.people_vaccinated_before/data_full.pop_data_2019*100



        data_full['delta_peoplevaccinated_per_100'] = data_full.peoplevacc_per_100_today - data_full.peoplevacc_per_100_before

        data_full['delta_totvaccinations_per_100'] = data_full.totvacc_per_100_today - data_full.totvacc_per_100_before

        return data_full.drop(columns = 'date')




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


def reconstruct_data(df, columna_filtro, columna_a_reconstruir, n):

    '''
    Esta función es para reconstruir los NaN values con regressiones lineales entre segmentos sin datos.
    De tal forma que los graficos de lineas se vean continuos y no con vacios
    La funcion completa los graficos lineales por para cada categoria (ej: pais)
    Columna_filtro es la columna por la cual se filtrara la data para tratarla parcialmente
    columna_a_reconstruir es la columna la cual se insertará data para ser utilizada en graficos
    n: es el numero de columna que es la columna a reconstruir
    '''

    for country in list(df[columna_filtro].unique()):

        data_pais = df[df[columna_filtro] == country].copy()

        if data_pais[data_pais[columna_filtro] == country][columna_a_reconstruir].isnull().sum() == len(data_pais[data_pais[columna_filtro] == country][columna_a_reconstruir]):
            continue


        if pd.isnull( data_pais.iloc[0,n] ):

            data_pais.iloc[0,n] = 0

        if pd.isnull( data_pais.iloc[len(data_pais)-1,n] ):

            data_pais.iloc[len(data_pais)-1,n] = data_pais[data_pais[columna_filtro] == country][columna_a_reconstruir].dropna().tail(1).iloc[0]

        empty = []

        for idx, value in enumerate(data_pais[columna_a_reconstruir]):

            if pd.isnull(value):
                empty.append(idx)

        if len(empty) > 0:



            last_digit = empty[0] #digito para iterar nan values index list
            diff_empty = []

            for idx in empty:
                diff = idx - last_digit
                diff_empty.append(diff)
                last_digit = idx

            del diff_empty[0]

            if len(diff_empty) > 0:

                before_value_idx = empty[0]-1
                before_value = data_pais[columna_a_reconstruir].iloc[before_value_idx]
                empty.insert(len(empty), 9) # numero ficticio para que se lean todos los valores después




                for idx, diff_num in enumerate(diff_empty):


                    if diff_num != 1:

                        ended_value_idx = empty[idx] + 1
                        ended_value = data_pais[columna_a_reconstruir].iloc[ended_value_idx]
                        coef = np.polyfit([before_value_idx, ended_value_idx], [before_value, ended_value], 1)

                        #calcular regression para nan values index
                        #insertarlos en el df
                        values_to_fill = np.array([i for i in range(before_value_idx+1,ended_value_idx)])*coef[0] + coef[1]

                        for idx_2, i in enumerate(range(before_value_idx+1, ended_value_idx)):

                            data_pais.iloc[i,n] = values_to_fill[idx_2]
                            df[df[columna_filtro]==country] = data_pais

                        if (idx + 1) < len(empty):

                            before_value_idx = empty[idx + 1] - 1
                            before_value = data_pais[columna_a_reconstruir].iloc[before_value_idx]

                        if (idx + 1) == len(diff_empty):

                            ended_value_idx = empty[idx+1] + 1
                            ended_value = data_pais[columna_a_reconstruir].iloc[ended_value_idx]
                            coef = np.polyfit([before_value_idx, ended_value_idx], [before_value, ended_value], 1)

                            #calcular regression para nan values index
                            #insertarlos en el df
                            values_to_fill = np.array([i for i in range(before_value_idx+1,ended_value_idx)])*coef[0] + coef[1]

                            for idx_2, i in enumerate(range(before_value_idx+1, ended_value_idx)):

                                data_pais.iloc[i,n] = values_to_fill[idx_2]
                                df[df[columna_filtro]==country] = data_pais

                    else:

                        if (idx + 1) == len(diff_empty):

                            ended_value_idx = empty[idx+1] + 1
                            ended_value = data_pais[columna_a_reconstruir].iloc[ended_value_idx]
                            coef = np.polyfit([before_value_idx, ended_value_idx], [before_value, ended_value], 1)

                            #calcular regression para nan values index
                            #insertarlos en el df
                            values_to_fill = np.array([i for i in range(before_value_idx+1,ended_value_idx)])*coef[0] + coef[1]

                            for idx_2, i in enumerate(range(before_value_idx+1, ended_value_idx)):

                                data_pais.iloc[i,n] = values_to_fill[idx_2]
                                df[df[columna_filtro]==country] = data_pais

            elif (len(diff_empty) ==0 and len(empty) == 1):

                        before_value_idx = empty[0] - 1

                        before_value = data_pais[columna_a_reconstruir].iloc[before_value_idx]


                        ended_value_idx = empty[0] + 1

                        ended_value = data_pais[columna_a_reconstruir].iloc[ended_value_idx]


                        coef = np.polyfit([before_value_idx, ended_value_idx], [before_value, ended_value], 1)


                        values_to_fill = np.array([i for i in range(before_value_idx+1,ended_value_idx)])*coef[0] + coef[1]

                        for idx_2, i in enumerate(range(before_value_idx+1, ended_value_idx)):

                            data_pais.iloc[i,n] = values_to_fill[idx_2]
                            df[df[columna_filtro]==country] = data_pais



    return df


if __name__ == '__main__':
    print('hola')
