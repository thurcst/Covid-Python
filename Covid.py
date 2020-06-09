import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Data is from www.ourworldindata.org

# Downloading new data:

csv_url     = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'
req         = requests.get(csv_url, allow_redirects = True)
open('owid-covid-data.csv', 'wb').write(req.content)

# Global vars:

columns_wbu = ['iso_code',
               'location',
               'total_cases',
               'new_cases',
               'population',
               'date',
               'total_deaths',
               'total_tests',
               'median_age']

covid_df    = pd.read_csv('owid-covid-data.csv')
today       = datetime.date(datetime.now())
yesterday   = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')

f_covid     = covid_df.copy()[columns_wbu]
f_covid.set_index(['location'], inplace = True)

country_list = f_covid.index
country_list = country_list.drop_duplicates().tolist()

# Settings:

pd.set_option('display.max_rows', 1000)

# Code:

def print_info(name, census):
    print('This data is from ' + str(census.loc[name]['date']))
    print('From ' + name  + ' we know:')
    print('Total cases: ' + str(census.loc[name]['total_cases']))
    print('Total Deaths: '+ str(census.loc[name]['total_deaths']))
    print('New cases: '   + str(census.loc[name]['new_cases']))
    return

def check_country(name, df, cl):
    try:
        census = df.loc[name]
        search(name, df, cl )
    except:
        print("""Missing Data or Country doesn't exist!""")
        answer = input("""Do you wan't to search a new country? (Yes/No) \n""")

        if answer.lower() == 'yes':
            name = input('País a ser pesquisado: ')
            res  = check_country(name, df, cl)



def search(name, df, cl):
    census = df.loc[name]
    census = census[census['date'] == today]
    if census.empty is True:
        census = df.loc[name]
        census = census[census['date'] == yesterday]

    graph = pd.DataFrame(df.loc[name][['date','total_cases','total_deaths']])

    for col in graph.columns:
        if col == 'total_cases':
            graph.rename(columns={col: 'Total Cases'}, inplace = True)
        if col == 'total_deaths':
            graph.rename(columns={col: 'Total Deaths'}, inplace = True)

    graph.set_index('date', inplace = True)
    graph.plot()

    plt.gcf().autofmt_xdate(bottom=0.2, rotation=45, ha='right', which=None)

    print_info(name, census)

    plt.show()

    answer = input("""Do you wan't to search a new country? (Yes/No) \n""")
    if answer.lower() == 'yes':
        name = input('País a ser pesquisado: ')
        res = check_country(name, df, cl)
    return

def ranking(f_covid):
    ranking = f_covid[f_covid['date'] == yesterday]
    ranking = ranking[['total_cases', 'total_deaths']]
    ranking = ranking.drop('World')
    ranking.sort_values(by = 'total_cases', ascending = False, inplace = True)
    ranking_list = (ranking.index[:3].tolist(), ranking[:3]['total_cases'])
    print('Covid-19 total cases ranking ('  + str(today) + '): ')
    print('1st: ' + ranking_list[0][0] + '('+str(ranking_list[1][0])+' cases)')
    print('2nd: ' + ranking_list[0][1] + '('+str(ranking_list[1][1])+' cases)')
    print('3rd: ' + ranking_list[0][2] + '('+str(ranking_list[1][2])+' cases)')


ranking(f_covid)

name = '-'

while (name == '?' or name == '-'):
    name = input('You can type ? for country list.\nCountry name: ')

    if name == '?':
        print('Countries available:')
        for country in country_list:
            print(country)


check_country(name, f_covid, country_list)
