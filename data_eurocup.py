# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 15:39:18 2023

@author: wilson
"""

from bs4 import BeautifulSoup
import requests
import pandas as pd



years = [1960, 1964, 1968, 1972, 1976, 1980, 1984, 1988, 1992, 1996, 2000,
             2004, 2008, 2012, 2016, 2020]


def get_matches(year):    
    web = f'https://en.wikipedia.org/wiki/UEFA_Euro_{year}'
    response = requests.get(web)
    content = response.text
    
    soup = BeautifulSoup(content, 'lxml')
    matches = soup.find_all('div', class_='footballbox')
    
    
    home = []
    score = []
    away = []
    
    for match in matches:
        home.append(match.find('th', class_='fhome').get_text())
        score.append(match.find('th', class_='fscore').get_text())
        away.append(match.find('th', class_='faway').get_text())
        
    
        
    dict_football = {'home': home , 'score': score, 'away': away}
    
    df_football = pd.DataFrame(dict_football)
    df_football['year'] = year
    
    return df_football

#historical_data
euro = [get_matches(year) for year in years]
df_euro = pd.concat(euro, ignore_index=True)
df_euro.to_csv('eurocup_historical_data.csv', index=False)

#fixture
df_fixture = get_matches(2024)
df_fixture.to_csv('eurocup_fixture_data.csv', index=False)

    
    