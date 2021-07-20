#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
from bs4 import BeautifulSoup
import requests


# In[3]:


response = requests.get('https://en.wikipedia.org/wiki/List_of_deaths_due_to_COVID-19#List')
doc = BeautifulSoup(response.text, 'html.parser')


# In[4]:


# target the table we want, which is table 4
doc = doc.find_all('table')[4]


# In[5]:


# select the rows
rows = doc.find_all('tr')


# In[6]:


# get all columns except names, which is in th tag
table_full_td = []

for row in rows:
    tds = row.find_all('td')
    cell = []
    for td in tds:
        cell.append(td.text)
        
    table_full_td.append(cell)


# In[7]:


table_full_td


# In[8]:


df = pd.DataFrame(table_full_td, columns=None)


# In[9]:


df


# In[10]:


df = df.drop(0)


# In[11]:


# rename the columns
df = df.rename(columns = {
        0: 
    'Date',
        1: 'Age',
        2: 'Profile description',
        3: 'Place of death'
})


# In[12]:


df


# In[13]:


# remove the \n from all columns
df = df.replace('\n', '', regex=True)


# In[22]:


df


# In[23]:


headers = doc.find_all('th')
headers


# In[48]:


name_list = []
for header in headers:
    name_dict ={}
    links = header.select_one('a')
    try:
       name_dict['Name']= links.text.strip()
    except:
       print("Couldn't find a name")
#     print(name_dict)
    name_list.append(name_dict)


# In[49]:


df2 = pd.DataFrame(name_list, columns = None)
df2.head(10)


# In[50]:


# drop rows 0-4
df2 = df2.drop(df2.index[0:5])
df2


# In[51]:


import numpy as np


# In[52]:


# make the index start at 1 to merge with other columns
df2.index = np.arange(1, len(df2) + 1)


# In[53]:


df2


# In[54]:


# merge df and df2 together using index
# .join merges using index by default
merged = df2.join(df)


# In[55]:


merged


# In[56]:


merged = merged.rename(columns = {
        0: 'Name'
    })


# In[57]:


merged


# In[58]:


# remove footnote [a] from 26 April 2020[a]
merged.Date = merged['Date'].str.replace('[a]', '', regex=False)


# In[59]:


import datetime


# In[60]:


# create separate column for day, month, and year
merged['Death_year'] = pd.DatetimeIndex(merged['Date']).year


# In[61]:


# create separate column for month and day
merged['Death_month'] = pd.DatetimeIndex(merged['Date']).month
merged['Death_day'] = pd.DatetimeIndex(merged['Date']).day


# In[62]:


merged


# In[63]:


merged.to_csv('covid_deaths.csv', index=False)

