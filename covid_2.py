import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import collections

csv_url     = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'
req         = requests.get(csv_url, allow_redirects = True)
open('owid-covid-data.csv', 'wb').write(req.content)

# Settings:

pd.set_option('display.max_rows', 1000)

# Global vars:

useful_columns  = ['date',
                   'location',
                   'new_cases',
                   'total_cases',
                   'total_deaths']

today           = datetime.date(datetime.now())
yesterday       = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')

covid_df        = pd.read_csv('owid-covid-data.csv')
country_list    = covid_df['location'].drop_duplicates().to_list()

alphabet = collections.defaultdict(list)

for word in country_list:
    alphabet[word[0].upper()].append(word)

for key in alphabet:
    print('{}:'.format(key))
    print('\n'.join(alphabet[key]))
    print()


def check(country):
    return country.title() in country_list

def search(country):
    # Returns a data frame of the country
    print(country.title())
    covid_list      = covid_df[covid_df['location'] == country.title()]
    covid_list      = covid_list[useful_columns]
    # covid_list.set_index('date', inplace = True)
    
    df_graph        = pd.DataFrame({'New cases': covid_list['new_cases'].to_list(),
                                    'Total Deaths': covid_list['total_deaths'].to_list(),
                                    'Total Cases': covid_list['total_cases'].to_list()}, index = covid_list['date'])
    df_graph.index = pd.to_datetime(df_graph.index)
    print(df_graph)
    df_graph        = df_graph.ffill()
    return df_graph


def ranking():
    ranking = covid_df[covid_df['date'] == yesterday]
    ranking = ranking[ranking['location'] != 'World']
    ranking = ranking[['location',
                      'new_cases',
                      'total_cases',
                      'total_deaths']]

    ranking = ranking.sort_values(['total_deaths', 'total_cases'], ascending = False)
    ranking.set_index('location', inplace = True)
    # print(ranking.round().astype(int))

    ranking_list = (ranking.index[:3].tolist(), ranking[:3]['total_cases'])
    print('Covid-19 total cases ranking ('  + str(today) + '): ')
    print('1st: {country} ({qtd:2d} cases)'.format(country = ranking_list[0][0],
                                                   qtd = int(ranking_list[1][0])))
    print('2nd: {country} ({qtd:2d} cases)'.format(country = ranking_list[0][1],
                                                   qtd = int(ranking_list[1][1])))
    print('3rd: {country} ({qtd:2d} cases)'.format(country = ranking_list[0][2],
                                                   qtd = int(ranking_list[1][2])))


ranking()

country         = input('Country to search: ')

while True:
    
    if check(country):
        # If the country exists at our list...
        print('Found')
        graph = search(country)
        graph.plot()
        # plt.gcf().autofmt_xdate(bottom=0.2, rotation=45, ha='right', which=None)
        plt.show()

        if str(input("""Do you wan't to search again? (Y/N)\n""")).lower() == 'y':
            country = input('Country name: ')
        else:
            break

    else:
        print('Country not found')
        
        if str(input("""Do you wan't to search again? (Y/N)\n""")).lower() == 'y':
            country = input('Country name: ')
        else:
            break