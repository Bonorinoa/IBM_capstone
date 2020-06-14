#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np # library to handle data in a vectorized manner

import pandas as pd # library for data analsysis
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

import json # library to handle JSON files

get_ipython().system('conda install -c conda-forge geopy --yes ')
from geopy.geocoders import Nominatim # convert an address into latitude and longitude values

import requests # library to handle requests
from pandas.io.json import json_normalize # tranform JSON file into a pandas dataframe

# Matplotlib and associated plotting modules
import matplotlib.cm as cm
import matplotlib.colors as colors


get_ipython().system('conda install -c conda-forge folium=0.5.0 --yes ')
import folium # map rendering library

print('Libraries imported.')


# In[2]:


CrimeSF = pd.read_csv('https://cocl.us/sanfran_crime_dataset')

print('Dataset downloaded and read into a pandas dataframe!')


# In[3]:


CrimeSF.head()


# In[4]:


CrimeSF.drop(['IncidntNum', 'Category', 'Descript','DayOfWeek','Date','Time','Resolution','Address','X','Y','Location','PdId'], axis=1, inplace=True)


# In[5]:


CrimeSF.rename(columns={'PdDistrict':'Neighborhood'}, inplace=True)
CrimeSF.head()


# In[6]:


CrimeSF.columns = list(map(str, CrimeSF.columns))


# In[7]:


CrimeSF['Counts'] = CrimeSF['Neighborhood'].value_counts()


# In[8]:


CrimeSF_sorted = CrimeSF.groupby(['Neighborhood']).Neighborhood.agg('count').to_frame('Count').reset_index()
CrimeSF_sorted.sort_values(['Neighborhood'], ascending =True, inplace=True)
CrimeSF_sorted


# In[9]:


get_ipython().system('wget --quiet https://cocl.us/sanfran_geojson')
    
print('GeoJSON file downloaded!')


# In[17]:


CLIENT_ID = 'RH1ASJPRDET3CU5Z44MQPBZ2A4H0LB2HPTD1B0BQZHK5COLZ' # your Foursquare ID
CLIENT_SECRET = 'GNOSURX3S1MPRQTBAKAWELXZT0ZLCE1RFW2YAJ1IEFZMCTO4' # your Foursquare Secret
VERSION = '20180604'
LIMIT = 30
print('Your credentails:')
print('CLIENT_ID: ' + CLIENT_ID)
print('CLIENT_SECRET:' + CLIENT_SECRET)


# In[18]:


address = 'San Francisco, CA, United States'

geolocator = Nominatim(user_agent="foursquare_agent")
location = geolocator.geocode(address)
latitude = location.latitude
longitude = location.longitude
print(latitude, longitude)


# In[127]:


search_query = 'Liquor Store'
radius = 10000
print(search_query + ' .... OK!')


# In[128]:


search_query1 = 'Food'
radius = 10000
print(search_query1 + ' .... OK!')


# In[129]:


search_query2 = 'Nightclub'
radius = 10000
print(search_query2 + ' .... OK!')


# In[130]:


search_query3 = 'Coffee'
radius = 10000
print(search_query3 + ' .... OK!')


# In[131]:


url = 'https://api.foursquare.com/v2/venues/search?client_id={}&client_secret={}&ll={},{}&v={}&query={}&radius={}&limit={}'.format(CLIENT_ID, CLIENT_SECRET, latitude, longitude, VERSION, search_query, radius, LIMIT)
url


# In[132]:


url1 = 'https://api.foursquare.com/v2/venues/search?client_id={}&client_secret={}&ll={},{}&v={}&query={}&radius={}&limit={}'.format(CLIENT_ID, CLIENT_SECRET, latitude, longitude, VERSION, search_query1, radius, LIMIT)
url1


# In[133]:


url2 = 'https://api.foursquare.com/v2/venues/search?client_id={}&client_secret={}&ll={},{}&v={}&query={}&radius={}&limit={}'.format(CLIENT_ID, CLIENT_SECRET, latitude, longitude, VERSION, search_query2, radius, LIMIT)
url2


# In[134]:


url3 = 'https://api.foursquare.com/v2/venues/search?client_id={}&client_secret={}&ll={},{}&v={}&query={}&radius={}&limit={}'.format(CLIENT_ID, CLIENT_SECRET, latitude, longitude, VERSION, search_query3, radius, LIMIT)
url3


# In[135]:


results = requests.get(url).json()


# In[136]:


results1 = requests.get(url1).json()


# In[137]:


results2 = requests.get(url2).json()


# In[138]:


results3 = requests.get(url3).json()


# In[139]:


venues = results['response']['venues']

# tranform venues into a dataframe
dataframe = json_normalize(venues)
dataframe.head()


# In[140]:


venues1 = results1['response']['venues']

# tranform venues into a dataframe
dataframe1 = json_normalize(venues1)
dataframe1.head()


# In[141]:


venues2 = results2['response']['venues']

# tranform venues into a dataframe
dataframe2 = json_normalize(venues2)
dataframe2.head()


# In[142]:


venues3 = results3['response']['venues']

# tranform venues into a dataframe
dataframe3 = json_normalize(venues3)
dataframe3.head()


# In[143]:


filtered_columns = ['name', 'categories'] + [col for col in dataframe.columns if col.startswith('location.')] + ['id']
dataframe_filtered = dataframe.loc[:, filtered_columns]

# function that extracts the category of the venue
def get_category_type(row):
    try:
        categories_list = row['categories']
    except:
        categories_list = row['venue.categories']
        
    if len(categories_list) == 0:
        return None
    else:
        return categories_list[0]['name']

# filter the category for each row
dataframe_filtered['categories'] = dataframe_filtered.apply(get_category_type, axis=1)

# clean column names by keeping only last term
dataframe_filtered.columns = [column.split('.')[-1] for column in dataframe_filtered.columns]

dataframe_filtered


# In[144]:


filtered_columns1 = ['name', 'categories'] + [col for col in dataframe1.columns if col.startswith('location.')] + ['id']
dataframe_filtered1 = dataframe1.loc[:, filtered_columns]

# function that extracts the category of the venue
def get_category_type(row):
    try:
        categories_list = row['categories']
    except:
        categories_list = row['venue.categories']
        
    if len(categories_list) == 0:
        return None
    else:
        return categories_list[0]['name']

# filter the category for each row
dataframe_filtered1['categories'] = dataframe_filtered1.apply(get_category_type, axis=1)

# clean column names by keeping only last term
dataframe_filtered1.columns = [column.split('.')[-1] for column in dataframe_filtered1.columns]

dataframe_filtered1


# In[145]:


filtered_columns2 = ['name', 'categories'] + [col for col in dataframe2.columns if col.startswith('location.')] + ['id']
dataframe_filtered2 = dataframe2.loc[:, filtered_columns]

# function that extracts the category of the venue
def get_category_type(row):
    try:
        categories_list = row['categories']
    except:
        categories_list = row['venue.categories']
        
    if len(categories_list) == 0:
        return None
    else:
        return categories_list[0]['name']

# filter the category for each row
dataframe_filtered2['categories'] = dataframe_filtered2.apply(get_category_type, axis=1)

# clean column names by keeping only last term
dataframe_filtered2.columns = [column.split('.')[-1] for column in dataframe_filtered2.columns]

dataframe_filtered2


# In[146]:


filtered_columns3 = ['name', 'categories'] + [col for col in dataframe3.columns if col.startswith('location.')] + ['id']
dataframe_filtered3 = dataframe3.loc[:, filtered_columns]

# function that extracts the category of the venue
def get_category_type(row):
    try:
        categories_list = row['categories']
    except:
        categories_list = row['venue.categories']
        
    if len(categories_list) == 0:
        return None
    else:
        return categories_list[0]['name']

# filter the category for each row
dataframe_filtered3['categories'] = dataframe_filtered3.apply(get_category_type, axis=1)

# clean column names by keeping only last term
dataframe_filtered3.columns = [column.split('.')[-1] for column in dataframe_filtered3.columns]

dataframe_filtered3


# In[147]:


dataframe_filtered.name


# In[148]:


dataframe_filtered1.name


# In[149]:


dataframe_filtered2.name


# In[150]:


dataframe_filtered3.name


# In[161]:


mapa = r'sanfran_geojson'
venues_map = folium.Map(location=[latitude, longitude], zoom_start=13) 

venues_map.choropleth(
    geo_data=mapa,
    data=CrimeSF_sorted,
    columns=['Neighborhood', 'Count'],
    key_on='feature.properties.DISTRICT',
    fill_color='YlOrRd', 
    fill_opacity=0.7, 
    line_opacity=0.2,
    legend_name='Crime San Francisco'
)

folium.features.CircleMarker(
    [latitude, longitude],
    radius=10,
    color='red',
    popup='San Francisco Downtown',
    fill = True,
    fill_color = 'red',
    fill_opacity = 0.6
).add_to(venues_map)


for lat, lng, label in zip(dataframe_filtered.lat, dataframe_filtered.lng, dataframe_filtered.categories):
    folium.features.CircleMarker(
        [lat, lng],
        radius=4,
        color='blue',
        popup=label,
        fill = True,
        fill_color='blue',
        fill_opacity=0.6
    ).add_to(venues_map)
    
for lat, lng, label in zip(dataframe_filtered1.lat, dataframe_filtered1.lng, dataframe_filtered1.categories):
    folium.features.CircleMarker(
        [lat, lng],
        radius=4,
        color='yellow',
        popup=label,
        fill = True,
        fill_color='yellow',
        fill_opacity=0.6
    ).add_to(venues_map)
    
for lat, lng, label in zip(dataframe_filtered2.lat, dataframe_filtered2.lng, dataframe_filtered2.categories):
    folium.features.CircleMarker(
        [lat, lng],
        radius=4,
        color='green',
        popup=label,
        fill = True,
        fill_color='green',
        fill_opacity=0.6
    ).add_to(venues_map)
    
for lat, lng, label in zip(dataframe_filtered3.lat, dataframe_filtered3.lng, dataframe_filtered3.categories):
    folium.features.CircleMarker(
        [lat, lng],
        radius=4,
        color='brown',
        popup=label,
        fill = True,
        fill_color='brown',
        fill_opacity=0.6
    ).add_to(venues_map)

legend_html =   '''
                <div style="position: fixed; 
                            bottom: 30px; left: 40px; width: 130px; height: 130px; 
                            border:2px solid grey; z-index:9999; font-size:12px;
                            ">&nbsp; Businesses <br>
                              &nbsp; Nightclub &nbsp; <i class="fa fa-map-marker fa-2x" style="color:green"></i><br>
                              &nbsp; Food &nbsp; <i class="fa fa-map-marker fa-2x" style="color:blue"></i><br>
                              &nbsp; Coffee &nbsp; <i class="fa fa-map-marker fa-2x" style="color:brown"></i><br>
                              &nbsp; Liquor Store &nbsp; <i class="fa fa-map-marker fa-2x" style="color:yellow"></i>
                </div>
                '''
venues_map.get_root().html.add_child(folium.Element(legend_html))
# display map
venues_map


# In[ ]:




