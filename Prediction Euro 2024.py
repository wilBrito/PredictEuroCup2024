#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import pickle
from scipy.stats import poisson


# In[2]:


# Cambio de idioma
traduccion_equipos = {
    'Albania': 'Albania',
    'Alemania': 'Germany',
    'Andorra': 'Andorra',
    'Armenia': 'Armenia',
    'Austria': 'Austria',
    'Azerbaiyán': 'Azerbaijan',
    'Bélgica': 'Belgium',
    'Bielorrusia': 'Belarus',
    'Bosnia y Herzegovina': 'Bosnia and Herzegovina',
    'Bulgaria': 'Bulgaria',
    'Chipre': 'Cyprus',
    'Croacia': 'Croatia',
    'Dinamarca': 'Denmark',
    'Escocia': 'Scotland',
    'Eslovaquia': 'Slovakia',
    'Eslovenia': 'Slovenia',
    'España': 'Spain',
    'Estonia': 'Estonia',
    'Finlandia': 'Finland',
    'Francia': 'France',
    'Georgia': 'Georgia',
    'Grecia': 'Greece',
    'Hungría': 'Hungary',
    'Inglaterra': 'England',
    'Irlanda': 'Ireland',
    'Irlanda del Norte': 'Northern Ireland',
    'Islandia': 'Iceland',
    'Islas Feroe': 'Faroe Islands',
    'Israel': 'Israel',
    'Italia': 'Italy',
    'Kazajistán': 'Kazakhstan',
    'Kosovo': 'Kosovo',
    'Letonia': 'Latvia',
    'Liechtenstein': 'Liechtenstein',
    'Lituania': 'Lithuania',
    'Luxemburgo': 'Luxembourg',
    'Macedonia del Norte': 'North Macedonia',
    'Malta': 'Malta',
    'Moldavia': 'Moldova',
    'Montenegro': 'Montenegro',
    'Noruega': 'Norway',
    'Países Bajos': 'Netherlands',
    'Polonia': 'Poland',
    'Portugal': 'Portugal',
    'República Checa': 'Czech Republic',
    'Rumania': 'Romania',
    'Rusia': 'Russia',
    'San Marino': 'San Marino',
    'Suecia': 'Sweden',
    'Suiza': 'Switzerland',
    'Serbia': 'Serbia',
    'Turquía': 'Turkey',
    'Ucrania': 'Ukraine',
    'Gales': 'Wales',
    'Ganador Ruta A' : 'Play-off winner A',
    'Ganador Ruta B' : 'Play-off winner B',
    'Ganador Ruta C' : 'Play-off winner C'
}


# In[3]:


# Traemos todos los archivos necesarios
dict_tables = pickle.load(open('dict_tables', 'rb'))
df_historical_data = pd.read_csv('clean_eurocup_historical_data.csv')
df_fixture_data = pd.read_csv('clean_eurocup_fixture_data.csv')


# In[4]:


# Función para traducir palabras
def traducir_palabra(palabra, diccionario_traducciones):
    palabra_traducida = diccionario_traducciones.get(palabra)
    return palabra_traducida


# In[5]:


# Traducimos los nombres de equipos para no encotrar ningun problema por el idioma
for grupo, valor in dict_tables.items():
    for i in range(0, 4):
        dict_tables[grupo]['Equipo'][i] = traducir_palabra(dict_tables[grupo]['Equipo'][i], traduccion_equipos)
    


# In[6]:


# Cálculamos cual es el mejor equipo en cuanto a goles se refiere

# Dividimos por cada columna de equipos sus repectivos goles marcados y recibidos 
df_home = df_historical_data[['HomeTeam', 'HomeGoals', 'AwayGoals']]
df_away = df_historical_data[['AwayTeam', 'HomeGoals', 'AwayGoals']]

#Renombramos columnas de los anteriores df
df_home = df_home.rename(columns = {'HomeTeam' : 'Team', 'HomeGoals' : 'GoalsScored', 'AwayGoals' : 'GoalsConceded'})
df_away = df_away.rename(columns = {'AwayTeam' : 'Team', 'HomeGoals' : 'GoalsConceded', 'AwayGoals' : 'GoalsScored'})


# In[7]:


# Concatenamos los dos anteriores df y calculamos el promedio de goles
df_team_strength = pd.concat([df_home, df_away], ignore_index=True).groupby('Team').mean()  #Fortaleza en goles


# In[8]:


#Realizamos una función aplicando la Distribución de Poission, con el fin de ver la probabilidad de puntos que tiene de sacar 
# los equipos en sus enfrentamientos

def predict_points(home, away):
    #Verificamos la existencia de los equipos
    if home in df_team_strength.index and away in df_team_strength.index:
        # Calculamos la lambda en este caso por medio de la multiplicación de goles marcados y concedidos
        lamb_home = df_team_strength.at[home, 'GoalsScored'] * df_team_strength.at[away, 'GoalsConceded']
        lamb_away = df_team_strength.at[away, 'GoalsScored'] * df_team_strength.at[home, 'GoalsConceded']
        
        prob_home, prob_away, prob_draw = 0, 0, 0
        # Obtenemos las probabilidades de todos los resultados posible hasta un máximo de 10 goles
        for x in range(0,11):
            for y in range(0,11):
                p = poisson.pmf(x, lamb_home) * poisson.pmf(y, lamb_away)
                if x == y:
                    prob_draw += p
                elif x > y:
                    prob_home += p
                else:
                    prob_away += p
        
        # Puntos posibles, cuantos puntos posibles de 3 puntos como máximo recibirá cada equipo
        points_home = 3 * prob_home + prob_draw
        points_away = 3 * prob_away + prob_draw
        
        return (points_home, points_away)
    
    else:
        return (0,0)
        


# In[9]:


## Empezamos con la Predicción


# In[10]:


# Dividimos los datos futuros en grupo, octavos, cuartos ...
df_fixture_group_36 = df_fixture_data[:36].copy()
df_fixture_knockout = df_fixture_data[36:44].copy()
df_fixture_quarter = df_fixture_data[44:48].copy()
df_fixture_semi = df_fixture_data[48:50].copy()
df_fixture_final = df_fixture_data[50:].copy()


# In[11]:


# Por medio de la función de poisson calculamos los resultados de la fase de grupos
for group in dict_tables:

    teams_in_group = dict_tables[group]['Equipo'].values
    df_fixture_group_6 = df_fixture_group_36[df_fixture_group_36['home'].isin(teams_in_group)]
    
    for index, row in df_fixture_group_6.iterrows():
        home, away = row['home'], row['away']
        points_home, points_away = predict_points(home, away)

        dict_tables[group].loc[dict_tables[group]['Equipo'] == home, 'Pts'] += points_home
        dict_tables[group].loc[dict_tables[group]['Equipo'] == away, 'Pts'] += points_away
        
    # Formateo
    dict_tables[group] = dict_tables[group].sort_values('Pts', ascending=False).reset_index()
    dict_tables[group] = dict_tables[group][['Equipo', 'Pts']]
    dict_tables[group] = dict_tables[group].round(0)


# In[12]:


# Actualizamos el fixture de knowckout con los datos que hemos obtenido
for group in dict_tables:
    group_winner = dict_tables[group].loc[0, 'Equipo']
    runner_up = dict_tables[group].loc[1, 'Equipo']
    group_last = dict_tables[group].loc[2, 'Equipo']
    

    aux = group.replace("Grupo", "").strip()
    df_fixture_knockout = df_fixture_knockout.replace(f'Runner-up Group {aux}', runner_up)
    df_fixture_knockout = df_fixture_knockout.replace(f'Winner Group {aux}', group_winner)
    df_fixture_knockout = df_fixture_knockout.replace(f'3rd Group A/{aux}/C', group_last)
    df_fixture_knockout = df_fixture_knockout.replace(f'3rd Group A/B/{aux}/D', group_last)
    df_fixture_knockout = df_fixture_knockout.replace(f'3rd Group {aux}/D/E/F', group_last)
    df_fixture_knockout = df_fixture_knockout.replace(f'3rd Group D/{aux}/F', group_last)
    
    
# Agrego columna winner
df_fixture_knockout['winner'] = '?'


# In[13]:


# Función para saber quien es el ganador del partido
def get_winner(df_fixture_updated):
    for index, row in df_fixture_updated.iterrows():
        home, away = row['home'], row['away']
        p_home, p_away = predict_points(home, away)
        if p_home > p_away:
            winner = home
        else:
            winner = away
        
        df_fixture_updated.loc[index, 'winner'] = winner
        
    return df_fixture_updated
        


# In[14]:


get_winner(df_fixture_knockout)


# In[15]:


# Creamos función para completar los partidos de las tablas futuras
def update_table(df_fixture_round_1, df_fixture_round_2):
    for index, row in df_fixture_round_1.iterrows():
        winner = df_fixture_round_1.loc[index, 'winner'].strip()
        match = df_fixture_round_1.loc[index, 'score'].strip()
        df_fixture_round_2 = df_fixture_round_2.replace({f'Winner {match}':winner})
    
    df_fixture_round_2['winner'] = '?'
    return df_fixture_round_2


# In[16]:


# Tabla futura de ganadores de los cuartos de final
df_fixture_quarter = update_table(df_fixture_knockout, df_fixture_quarter)
get_winner(df_fixture_quarter)


# In[17]:


# Tabla futura de ganadores de las semis de final
df_fixture_semi = update_table(df_fixture_quarter, df_fixture_semi)
get_winner(df_fixture_semi)


# In[18]:


# Tabla futura del ganador
df_fixture_final = update_table(df_fixture_semi, df_fixture_final)
get_winner(df_fixture_final)

