# -*- coding: utf-8 -*-
"""
Created on Thu Jan  4 13:09:45 2024

@author: wilson
"""

from bs4 import BeautifulSoup
import requests
import pandas as pd
import re



years = [1960, 1964, 1968, 1972, 1976, 1980, 1984, 1988, 1992, 1996, 2000,
             2004, 2008, 2012, 2016, 2020]

groups = [1, 2, 3, 4, 5, 6, 7, 8]


def get_matches_qualifying(year):    
    web = f"https://en.wikipedia.org/wiki/{year}_European_Nations'_Cup_qualifying"
    response = requests.get(web)
    content = response.text
    
    soup = BeautifulSoup(content, 'lxml')
    matches = soup.find_all('tr')
    
    home = []
    score = []
    away = []
    
    for match in matches:
        aux1 = match.find('td', {'style': 'text-align: center;'}) 
        aux2 = match.find('td', {'style' : 'text-align: right;'})
        aux3 = match.find('td', {'style' : 'text-align: left;'})
        
        if aux1 or aux2 != None:
            aux1 =  aux1.get_text().replace('\n', "")
            score.append(aux1)
            
            aux2 = aux2.get_text().replace('\xa0\n', "")
            home.append(aux2)
            
            aux3 = aux3.get_text().replace('\xa0', "")
            aux3 = re.sub("\n", "", aux3)
            away.append(aux3)
    
    dict_football = {'home': home , 'score': score, 'away': away}
    
    df_football = pd.DataFrame(dict_football)
    df_football['year'] = year
        
        
    
    return df_football

def get_matches_qualifying_group(year):    
    home = []
    score = []
    away = []
    
    for group in groups:
        web = f"https://en.wikipedia.org/wiki/UEFA_Euro_{year}_qualifying_Group_{group}"
        response = requests.get(web)
        content = response.text
    
        soup = BeautifulSoup(content, 'lxml')
        matches = soup.find_all('div', class_='footballbox')

        for match in matches:
            home.append(match.find('th', class_='fhome').get_text())
            score.append(match.find('th', class_='fscore').get_text())
            away.append(match.find('th', class_='faway').get_text())
        
    
        
    dict_football = {'home': home , 'score': score, 'away': away}
    
    df_football = pd.DataFrame(dict_football)
    df_football['year'] = year
           
    
    return df_football

euro_qualifying = [get_matches_qualifying(year) for year in years]
euro_qualifying_group = [get_matches_qualifying_group(year) for year in years]


df_euro_qualifying = pd.concat(euro_qualifying, ignore_index=True)
df_euro_qualifying_group = pd.concat(euro_qualifying_group, ignore_index=True)

df_euro_data_lost = pd.concat([df_euro_qualifying, df_euro_qualifying_group])
print(df_euro_data_lost)
#df_euro_data_lost.to_csv('eurocup_historical_data_lost.csv', index=False)
    
