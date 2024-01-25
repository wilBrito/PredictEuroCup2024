#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
from string import ascii_uppercase as abecedario
import pickle


# In[22]:


all_tables = pd.read_html('https://es.wikipedia.org/wiki/Eurocopa_2024')

dict_tables = {}
for letra, i in zip(abecedario, range(7, 49, 7)):
    df = all_tables[i]
    dict_tables[f'Grupo {letra}'] = df


# In[ ]:


with open('dict_tables', 'wb') as output:
    pickle.dump(dict_tables, output)

