#!/usr/bin/env python
# coding: utf-8

# SCRIPT DE TESTS

# In[13]:


import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
import time

driver=webdriver.Chrome(executable_path='C:\\Users\\kwalc\\Downloads\\chromedriver_win32\\chromedriver.exe')
print(type(driver))


# In[25]:



pays=" "

# Scraping test unitaire
def get_tx_chom_from_country(pays):
    '''
        Get taux chomage info par pays

        :param pays: nom de pays
        :type pays: String
        :return: 
                - noms_pays: nom de pays
                - taux_chom: taux correspondant
        :rtype: tuple(string, string)
    '''
    
    url = 'https://fr.countryeconomy.com/marche-du-travail/chomage'
    driver.get(url)
    
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    table_pays_tx_chom = soup.find('table', class_ = 'table tabledat table-striped table-condensed table-hover')

    for pays in table_pays_tx_chom.find_all('tbody'):
        lignes = pays.find_all('tr')
        for ligne in lignes: 
            noms_pays = ligne.find('td').text.strip('[+]')
            taux_chom = ligne.find('td', class_ = 'numero').text.strip()
    return(noms_pays, taux_chom)


# In[26]:


get_tx_chom_from_country("Afrique du Sud")


# In[11]:


pays = ' '

# API test unitaire
def get_distance_and_duration_from_france_to_germany(pays):
    '''
        Get distance et durée qui sépare un français d'un autre pays

        :param pays_ue: liste de pays de l'union européene
        :type pays_ue: liste de String
        :return: 
                - output: dictionnaire contenant des données json de la page d'url=url_full
                - data['distance']: données distances en km
                - data['duration']: données durées en prenant la voiture en heures et minutes
        :rtype: dict
    '''

    
    
    apikey = "AIzaSyCouNtR_wHK7g20CTnB5b6h6aMWdatk4q0"
    url1 = "https://maps.googleapis.com/maps/api/distancematrix/json?origins="
    origin = "France"
    url2 = "&destinations="
    destination = 'Allemagne'
    url3 = "&mode=car&key="

    url_full = url1+origin+url2+destination+url3+apikey
    output = requests.get(url_full).json()
    print(output)
    print(type(output))
    for obj in output['rows']:
        for data in obj['elements']:
            print(data['distance']['text'])
            print(data['duration']['text'])


# In[12]:



get_distance_and_duration_from_france_to_germany(pays)


# In[ ]:




