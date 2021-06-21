#!/usr/bin/env python
# coding: utf-8

# In[1]:


Analisis espacial por barrios en Bogotá
#Clase VII
get_ipython().system('pip3 install shapely')
get_ipython().system('pip3 install pyproj')
get_ipython().system('pip3 install folium')
get_ipython().system('pip3 install pandas')
get_ipython().system('pip3 install requests')
get_ipython().system('pip3 install geopy')
get_ipython().system('pip3 install geojson')
get_ipython().system('pip3 install xlrd')


# In[2]:


import pyproj
from functools import partial
import shapely.geometry
from shapely.ops import transform
from shapely.geometry import Point
import folium 
import geojson 
import json
import pandas as pd
import re
import geopy
import requests
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
import os


# In[3]:


os.chdir('C:\\Users\\isabe\\OneDrive\Escritorio\python')


# In[5]:


get_ipython().system('pip3 install openpyxl')


# In[6]:


Alojamientos_hospedaje=pd.read_excel('Direcciones.xlsx')


# In[7]:


Alojamientos_hospedaje 


# In[8]:


#Crear variables  para definir longitud y latitud
Alojamientos_hospedaje['Latitud'] = None
Alojamientos_hospedaje['Longitud'] = None 


# In[9]:


#Ver la abse de datos con las nuevas variables 
Alojamientos_hospedaje


# In[10]:


api_here='aAFNTc2BfTQV-2uFzqfGv_sKzzYEVfhnjmKlXS8kh9o'
#Forma manual


# In[11]:


Direccion = Alojamientos_hospedaje['Direccion'].loc[0]
busqueda = Direccion + 'Bogotá, Colombia'
PARAMS = {'apikey':api_here, 'q': busqueda}

#Construir solicitud
URL= 'http://geocode.search.hereapi.com/v1(geocode)'
r = requests.get(url = URL, params=PARAMS)
data= r.json()
latitude=data['items'][0]['position']['lat']
longitude=data['items'][0]['position']['lng']
#Saqueme el contenido que esta en la celda 0


# In[12]:


Direccion


# In[14]:


Direccion = Alojamientos_hospedaje['Direccion'].loc[0]
busqueda = Direccion + ', Bogotá, Colombia'
PARAMS = {'apikey':api_here, 'q': busqueda}
#Construir una solicitud
URL = 'https://geocode.search.hereapi.com/v1/geocode'
r = requests.get(url = URL, params=PARAMS)
data= r.json()
latitude=data['items'][0]['position']['lat']
longitude=data['items'][0]['position']['lng']


# In[15]:


data


# In[22]:


latitude


# In[24]:


#Alojamientos_hospedaje esta aun con none
#reemplazar la coordenada
Alojamientos_hospedaje['Latitud'].iloc[0]=latitude
Alojamientos_hospedaje['Longitud'].iloc[0]=longitude


# In[25]:


Alojamientos_hospedaje #Aca ya aparece la coordenada


# In[32]:


#Buscar coordenadas para las primeras 10 observaciones
for j in range(0,10):
    Direccion=Alojamientos_hospedaje['Direccion'].iloc[j]
    busqueda=Direccion + 'Bogotá, Colombia'
    PARAMS= {'apikey':api_here, 'q': busqueda}
    print('Geocoding de la dirección:'+ busqueda)
#Enviar la solicitud
URL = 'https://geocode.search.hereapi.com/v1/geocode'
r = requests.get(url = URL, params=PARAMS)
data= r.json()
latitude=data['items'][0]['position']['lat']
longitude=data['items'][0]['position']['lng']
Alojamientos_hospedaje['Latitud'].iloc[j]=latitude
Alojamientos_hospedaje['Longitud'].iloc[j]=longitude


# In[33]:


Alojamientos_hospedaje.head(10)


# In[34]:


#Forma automatica (Geopy)
#Para una direccion 
Direccion = 'Carrera 64 103C 16'
busqueda = Direccion + 'Bogotá, Colombia'
#"Definir el motor de geocoder que va a utilizar"
#"En este caso empleamos HERE"
motor_busqueda=geopy.geocoders.Here(app_id=None,app_code=None, apikey=api_here)
Resultado_busqueda=motor_busqueda.geocode(busqueda, timeout=10000)


# In[35]:


Resultado_busqueda


# In[36]:


#Para 10 direcciones
#El motor de busqueda se define una sola vez
motor_busqueda=geopy.geocoders.Here(app_id=None, app_code=None, apikey=api_here)
for j in range(0,10):
    Direccion = Alojamientos_hospedaje['Direccion'].iloc[j]
    busqueda = Direccion + 'Bogotá, Colombia'
    print(busqueda)
#Realizar busqueda
    Resultado_busqueda = motor_busqueda.geocode(busqueda, timeout=10000)
#Reemplazar coordenada
    Alojamientos_hospedaje['Latitud'].iloc[j]=Resultado_busqueda.latitude
    Alojamientos_hospedaje['Longitud'].iloc[j]=Resultado_busqueda.longitude


# In[37]:


#Nominatim (Open Street maps)
Direccion = 'Carrera 64 103C 16'
busqueda = Direccion + 'Bogotá, Colombia'
buscador_open = Nominatim(user_agent='correo@curso.com.co')
#Definir busqueda
Resultado = buscador_open.geocode(busqueda,timeout=10000)


# In[38]:


Resultado

