

#!/usr/bin/env python
# coding: utf-8

import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver


driver=webdriver.Chrome(executable_path="chromedriver.exe")
print(type(driver))

df_world_happiness_report = pd.read_csv('world-happiness-report-2021.csv',sep=';')
print(df_world_happiness_report)

taux_chom_pays=pd.read_csv('name_translate.csv',sep=';')
print(taux_chom_pays)


# Fonction qui récupère les taux de chomage par pays
L_pays_taux=[]
pays_taux=[]
def get_tx_chom_from_country(pays_taux):
    '''
        Get taux chomage info par pays

        :param pays_taux: liste de pays
        :type pays_taux: liste de String
        :return: 
                - noms_pays: liste de pays
                - taux_chom: liste des taux correspondants
        :rtype: tuple(string, string)
    '''
    
    url = 'https://fr.countryeconomy.com/marche-du-travail/chomage'
    driver.get(url)
    
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    table_pays_tx_chom = soup.find('table', class_ = 'table tabledat table-striped table-condensed table-hover')
    L=[]
    for pays in table_pays_tx_chom.find_all('tbody'):
        lignes = pays.find_all('tr')
        nom_pays=[]
        taux_chom=[]
        for ligne in lignes: 
            noms_pays = ligne.find('td').text.strip('[+]')
            taux_chom = ligne.find('td', class_ = 'numero').text.strip('%')
            L.append(noms_pays)
            nom_pays.append(noms_pays)
            taux_chom.append(taux_chom)
        return nom_pays,taux_chom


# tous fonctione trés bien sauf que la langue source est le francais or nos autre dataset sont en anglais, donc on la traduit par reverso et on garde donc cette version la pour pouvoir avoir une clé commune au moment du merge 

# L1,L2 = get_tx_chom_from_country(L_pays_taux)
# data = {'nom pays':L1,'taux de chomage en %':L2}
# taux_chom_pays=pd.DataFrame(data)
# taux_chom_pays
# taux_chom_pays.to_csv(sep=';',path_or_buf='name_to_translate.csv',index=False,index_label=False,encoding='latin',decimal=',')


# Fonction qui récupère les taux de coût-de-vie par pays
country_col_index=[]
L_country_col_index=[]
def get_cost_of_living_index_by_country(country_col_index):
    '''
        Get cost-of-living index info par pays

        :param country_col_index: liste de pays
        :type country_col_index: liste de String
        :return: 
                - country_name: liste de pays
                - col_index: Taux du coût-de-vie
                - rent_index: Taux Loyer
                - col_plus_rent_index: Taux coût-de-vie + Loyer
                - groceries_index: indice courses
                - rp_index: indice de prix des restaurants
                - lpp_index: indice de pouvoir d'achat local
        :rtype: tuple(string, float, float, float, float, float, float)
    '''
    
    url = 'https://www.numbeo.com/cost-of-living/rankings_by_country.jsp'
    driver.get(url)
    
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    table_col = soup.find('table', id = 't2')

    for country in table_col.find_all('tbody'):
        rows = country.find_all('tr')
        country_nam = []
        col_inde= []
        rent_inde= []
        col_plus_rent_inde= []
        groceries_inde= []
        rp_inde= []
        lpp_inde= []

        for row in rows: 
            country_name = row.find('td', class_ = 'cityOrCountryInIndicesTable').text.strip() #nom pays
            col_index = row.find_all('td')[2].text #indice de cout de vie 
            col_plus_rent_index = row.find_all('td')[4].text #indice cout de vie + loyers
            groceries_index = row.find_all('td')[5].text #indice courses
            rp_index = row.find_all('td')[6].text #indice prix restaurant
            lpp_index = row.find_all('td')[7].text #indice de pouvoir d'achat local
            country_nam.append(country_name)
            col_inde.append(col_index)
            rent_inde.append(rent_inde)
            col_plus_rent_inde.append(col_plus_rent_index)
            groceries_inde.append(groceries_index)
            rp_inde.append(rp_index)
            lpp_inde.append(lpp_index)

        return country_nam,col_inde,rent_inde,col_plus_rent_inde,groceries_inde,rp_inde,lpp_inde
            
country_nam,col_inde,rent_inde,col_plus_rent_inde,groceries_inde,rp_inde,lpp_inde=get_cost_of_living_index_by_country(L_country_col_index)
data = {'Country_Name':country_nam,'cost of living index':col_inde,'cost of living plus rent index':col_plus_rent_inde,'Groceries index':groceries_inde,'restaurant price index':rp_inde,'local purchasing power index':lpp_inde}
cost_of_living_index = pd.DataFrame(data)
print(cost_of_living_index)


# Fonction qui récupère la liste de pays où les français peuvent entrer sans visas
list_vfc=[]
pays_vfc=[]
def get_visa_free_country_for_french(pays_vfc):
    '''
        Get pays où un français n'a pas besoin de visa pour entrer

        :param pays_vfc: liste de pays
        :type pays_vfc: liste de String
        :return: 
                - noms_pays: liste de pays 1/2
                - allowed_stay: durées maximales authorisées 1/2
                - noms_pays2: liste de pays 2/2
                - allowed_stay2: durées maximales authorisées 2/2
        :rtype: tuple(string, string, string, string)
    '''
    
    url = 'https://visaguide.world/visa-free-countries/french-passport/'
    driver.get(url)
    
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    table_pays_visa_free = soup.find('table', class_ = 'tablepress tablepress-id-71')

    for pays in table_pays_visa_free.find_all('tbody'):
        lignes = pays.find_all('tr')
        nom=[]
        stay=[]
        for ligne in lignes: 
            noms_pays = ligne.find('td', class_ = 'column-1').text.strip()
            allowed_stay = ligne.find('td', class_ = 'column-2').text.strip()
            noms_pays2 = ligne.find('td', class_ = 'column-3').text.strip()
            allowed_stay2 = ligne.find('td', class_ = 'column-4').text.strip()
            list_vfc.append(noms_pays)
            list_vfc.append(noms_pays2)
            nom.append(noms_pays)
            nom.append(noms_pays2)
            # nom2.append(noms_pays2)
            stay.append(allowed_stay)
            stay.append(allowed_stay2)
            # stay2.append(allowed_stay2)
            # print(noms_pays, allowed_stay)
            # print (noms_pays2, allowed_stay2)b
        return nom,stay

noms_pays,allowed_stay = get_visa_free_country_for_french(list_vfc)
data = {'Country_Name':noms_pays,'time_available_on_site':allowed_stay,'required visa for french citizen':'not required'}
df_visa_free_country_for_french=pd.DataFrame(data)
print(df_visa_free_country_for_french)


# Fonction qui récupère la liste des pays où un français à besoin d'un Evisa pour entrer
list_evisa=[]
pays_evisa=[]
def get_evisa_country_for_french(pays_evisa):
    '''
        Get pays où un français a besoin d'un evisa pour entrer

        :param pays_evisa: liste de pays
        :type pays_evisa: liste de String
        :return: 
                - noms_pays: liste de pays 
                - allowed_stay: durées maximales authorisées 
        :rtype: tuple(string, string)
    '''
    
    url = 'https://visaguide.world/visa-free-countries/french-passport/'
    driver.get(url)
    
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    
    table_pays_evisa_required = soup.find('table', class_ = 'tablepress tablepress-id-72')

    for pays in table_pays_evisa_required.find_all('tbody'):
        lignes = pays.find_all('tr')
        nom=[]
        stay=[]
        for ligne in lignes: 
            noms_pays = ligne.find('td', class_ = 'column-1').text.strip()
            allowed_stay = ligne.find('td', class_ = 'column-2').text.strip()
            list_evisa.append(noms_pays)
            nom.append(noms_pays)
            stay.append(allowed_stay)
            # print(noms_pays, allowed_stay)
        return nom,stay

noms_pays,allowed_stay = get_evisa_country_for_french(list_evisa)
data = {'Country_Name':noms_pays,'time_available_on_site':allowed_stay,'required visa for french citizen':'Evisa'}
df_evisa_country_for_french=pd.DataFrame(data)
print(df_evisa_country_for_french)


# Fonction qui récupère la liste des pays où un français peut entrer et demander un visa à l'arrivée
list_visa_oa=[]
pays_visa_oa=[]
def get_visa_on_arrival_country_for_french(pays_visa_oa):
    '''
        Get pays où un français a besoin d'un visa à son arrivée

        :param pays_visa_oa: liste de pays
        :type pays_visa_oa: liste de String
        :return: 
                - noms_pays: liste de pays 
                - allowed_stay: durées maximales authorisées 
        :rtype: tuple(string, string)
    '''
    
    url = 'https://visaguide.world/visa-free-countries/french-passport/'
    driver.get(url)
    
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    
    table_pays_visa_on_arrival_requirements = soup.find('table', class_ = 'tablepress tablepress-id-73')

    for pays in table_pays_visa_on_arrival_requirements.find_all('tbody'):
        lignes = pays.find_all('tr')
        nom=[]
        stay=[]
        for ligne in lignes: 
            noms_pays = ligne.find('td', class_ = 'column-1').text.strip()
            allowed_stay = ligne.find('td', class_ = 'column-2').text.strip()
            list_visa_oa.append(noms_pays)
            nom.append(noms_pays)
            stay.append(allowed_stay)
            # print(noms_pays, allowed_stay)
        return nom,stay

noms_pays,allowed_stay = get_visa_on_arrival_country_for_french(list_visa_oa)
allowed_stay = [a.replace('(renewable)','renewable')for a in allowed_stay]
allowed_stay = [a.replace('(with extension)','with extension')for a in allowed_stay]
data = {'Country_Name':noms_pays,'time_available_on_site':allowed_stay,'required visa for french citizen':'required to stay'}
df_visa_on_arrival_country_for_french=pd.DataFrame(data)
print(df_visa_on_arrival_country_for_french)


# Fonction qui récupère la liste des pays où un français n'a pas le droit d'entrer sans visa
list_visa_required=[]
pays_visa_required=[]
def get_visa_requirement_country_for_french(pays_visa_required):
    '''
        Get pays où un français a besoin d'un visa pour entrer dans le pays

        :param pays_visa_required: liste de pays
        :type pays_visa_required: liste de String
        :return: 
                - noms_pays: liste de pays 1/3 
                - noms_pays2: liste de pays 2/3
                - noms_pays3: liste de pays 3/3
        :rtype: tuple(string, string, string)
    '''
    
    url = 'https://visaguide.world/visa-free-countries/french-passport/'
    driver.get(url)
    
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    
    table_pays_visa_requirement_to_enter = soup.find('table', class_ = 'tablepress tablepress-id-74')

    for pays in table_pays_visa_requirement_to_enter.find_all('tbody'):
        lignes = pays.find_all('tr')
        for ligne in lignes: 
            noms_pays = ligne.find('td', class_ = 'column-1').text.strip()
            noms_pays2 = ligne.find('td', class_ = 'column-2').text.strip()
            noms_pays3 = ligne.find('td', class_ = 'column-3').text.strip()
            list_visa_required.append(noms_pays)
            list_visa_required.append(noms_pays2)
            list_visa_required.append(noms_pays3)
            # print(noms_pays)
            # print(noms_pays2)
            # print(noms_pays3)
        return list_visa_required

get_visa_requirement_country_for_french(list_visa_oa)

noms_pays= get_visa_requirement_country_for_french(list_visa_oa)
data = {'Country_Name':noms_pays,'time_available_on_site':'/','required visa for french citizen':'particular country information on embassy site'}
df_visa_requirement_country_for_french=pd.DataFrame(data)
print(df_visa_requirement_country_for_french)

print(cost_of_living_index.shape)

# Merge des 2 plus gros d'un coté
df_merge = df_world_happiness_report.merge(
    cost_of_living_index,how='inner',on='Country_Name'
)
france=df_merge.loc[df_merge["Country_Name"]=="France"]
df_merge_for_visa = pd.concat([df_evisa_country_for_french,df_visa_free_country_for_french,df_visa_on_arrival_country_for_french,df_visa_requirement_country_for_french])
df_merge_for_visa=df_merge_for_visa.drop_duplicates(keep='first',subset='Country_Name')

# Enfin on merge toute ces dataframe ensemble 
df_all = df_merge.merge(
    df_merge_for_visa,how='inner',on='Country_Name'
)
df_all=pd.concat([france,df_all])
print(df_all)



#Les googleapis sont utilisés sur des routes existantes mais il n'existe pas de mode de voyage par avion.
pays_ue=[]
List_pays_ue = ['Allemagne', 'Autriche', 'Belgique', 'Bulgarie', 'Croatie', 'Danemark', 'Espagne', 'Estonie', 'Finlande', 'Grèce', 'Hongrie', 'Irlande', 'Italie', 'Lettonie', 'Lituanie', 'Luxembourg', 'Malte', 'Pays-Bas', 'Pologne', 'Portugal', 'République-Tchèque', 'Roumanie', 'Slovaquie', 'Slovénie', 'Suède']
lenght=len(List_pays_ue)

def get_distance_and_duration_from_france_to_eu_country(pays_ue):
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

    for i in range(lenght):
    
        apikey = "AIzaSyCouNtR_wHK7g20CTnB5b6h6aMWdatk4q0"
        url1 = "https://maps.googleapis.com/maps/api/distancematrix/json?origins="
        origin = "France"
        url2 = "&destinations="
        destination = List_pays_ue[i]
        url3 = "&mode=car&key="

        url_full = url1+origin+url2+destination+url3+apikey
        output = requests.get(url_full).json()
        print(output)
        print(type(output))
        for obj in output['rows']:
            for data in obj['elements']:
                print(data['distance']['text'])
                print(data['duration']['text'])

get_distance_and_duration_from_france_to_eu_country(List_pays_ue)

df_all=df_all[['Country_Name', 'Regional indicator', 'Ladder score',
               'Social support', 'Healthy life expectancy',
       'Freedom to make life choices', 'Generosity',
       'Perceptions of corruption', 
        'cost of living index',
       'cost of living plus rent index', 'Groceries index',
       'restaurant price index', 'local purchasing power index',
       'time_available_on_site', 'required visa for french citizen']]
df_all.columns=df_all.columns.str.replace(" ", "_")
df_all=df_all.astype(str)
for col in df_all.columns:
    df_all[col]=df_all[col].str.replace(',','.')
df_all=df_all.astype(object)

df_all.to_csv(sep=';',path_or_buf='dataframe-expat-final.csv',index=True,encoding='latin',decimal=',')






