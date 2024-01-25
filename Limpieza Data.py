#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


# Cargamos los datos anteriormente obtenidos por web scraping
df_data_historica = pd.read_csv('eurocup_historical_data.csv')
df_data_fixture = pd.read_csv('eurocup_fixture_data.csv')
df_data_lost = pd.read_csv('eurocup_historical_data_lost.csv')


# In[3]:


#Limpieza de espacios en blanco
df_data_fixture['home'] = df_data_fixture['home'].str.strip()
df_data_fixture['away'] = df_data_fixture['away'].str.strip()

df_data_historica['home'] = df_data_historica['home'].str.strip()
df_data_historica['away'] = df_data_historica['away'].str.strip()


# In[13]:


#df_data_lost[df_data_lost['home'].isnull()]  # Verificamos si tiene elementos nulos (datos faltantes)


# In[5]:


# Unimos la data historica con la faltante
df_data_historica = pd.concat([df_data_historica, df_data_lost], ignore_index=True)
df_data_historica.drop_duplicates(inplace=True)   #Eliminamos duplicados
df_data_historica.sort_values('year', inplace=True)  # Ordenado por años


# In[6]:


#Buscamos partidos que acabaron en w/o, cancelados o resultados extraños para eliminarlos
index_delete_1 = df_data_historica[df_data_historica['score'].str.contains('w.o.')].index # Son dos, me guardo el index
index_delete_2 = df_data_historica[df_data_historica['score'].str.contains('Cancelled')].index # Solo es uno, me guardo el index 
index_delete_3 = df_data_historica[df_data_historica['score'].str.contains('coin')].index # Solo es uno, me guardo el index
index_delete_4 = df_data_historica[df_data_historica['score'].str.contains('Annulled')].index # Solo es uno, me guardo el index

#Eliminamos los index
df_data_historica.drop(index=index_delete_1, inplace=True)   
df_data_historica.drop(index=index_delete_2, inplace=True) 
df_data_historica.drop(index=index_delete_3, inplace=True) 
df_data_historica.drop(index=index_delete_4, inplace=True) 


# In[7]:


# Buscamos resultados que contengan textos no numericos y lo eliminamos

#df_data_historica[df_data_historica['score'].str.contains('a')]     #Buscando los no numericos

df_data_historica['score'] = df_data_historica['score'].str.replace(r'\(a.e.t.\)||\(a.e.t.\/g.g.\)||\(a.e.t.\/s.g.\)', '', regex=True)


# In[8]:


# Separamos el valor de score en dos columnas
df_data_historica[['HomeGoals', 'AwayGoals']] = df_data_historica['score'].str.split('–', expand=True)


# In[9]:


# Eliminamos columna score
df_data_historica.drop('score', axis=1, inplace=True)


# In[10]:


# Renombramos columnas
df_data_historica.rename(columns={'home':'HomeTeam', 'away':'AwayTeam', 'year':'Year'}, inplace=True)


# In[11]:


# Cambiamos tipo de datos
#df_data_historica.dtypes   #Verificamos tipos de datos

df_data_historica = df_data_historica.astype({'HomeGoals': int, 'AwayGoals': int})


# In[12]:


#Obtenemos csv tras haber limpiado los datos 
df_data_historica.to_csv('clean_eurocup_historical_data.csv', index=False)
df_data_fixture.to_csv('clean_eurocup_fixture_data.csv', index=False)

